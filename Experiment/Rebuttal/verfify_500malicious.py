#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
process_malware_snippets.py

功能：
- 递归读取指定目录下所有 JSON 文件（malware_snippets 目录）
- 随机选择最多 500 个文件
- 对每个文件内 malicious_snippets[*].malicious_code 调用 LLM 进行“是否为核心恶意代码”的判断
- 将结果存放到 rebuttal/malicious_code_check_results.json（每处理一个文件即时写回）
- 直接使用 OpenAI Python SDK（从 rebuttal/llm_config.json 读取 openai_api_key / openai_api_model）
"""

import os
import sys
import json
import random
import time
import traceback

from typing import Any, Dict

# ==== 配置（可按需修改） ====
FOLDER_PATH = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/code_snipptes/malware_snippets"
OUTPUT_DIR = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/rebuttal"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "malicious_code_check_results.json")
MAX_FILES = 500
# ============================

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- 读取 OpenAI 配置，初始化 SDK ----
_openai_client = None
_openai_model = None


def _init_openai_from_config() -> None:
    global _openai_client, _openai_model
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm_config.json")
    cfg: Dict[str, Any] = {}
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

    api_key = cfg.get("openai_api_key")
    model = cfg.get("openai_api_model", "gpt-4.1")
    if not api_key:
        raise RuntimeError("openai_api_key missing in rebuttal/llm_config.json")

    try:
        from openai import OpenAI  # type: ignore
    except Exception as e:
        raise RuntimeError("OpenAI SDK not installed. Please run: pip install openai") from e

    _openai_client = OpenAI(api_key=api_key)
    _openai_model = model


def _call_llm_openai_sdk(prompt: str, timeout: int = 60) -> Dict[str, Any]:
    if _openai_client is None or _openai_model is None:
        _init_openai_from_config()

    params = {
        "model": _openai_model,
        "messages": [
            {"role": "system", "content": "你是一个安全分析助手。请严格按 JSON 对象回答，不要输出多余文本。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "top_p": 0.3,
        "max_tokens": 1600,
        "timeout": timeout,
    }

    try:
        resp = _openai_client.chat.completions.create(**params)
        content = resp.choices[0].message.content if resp and resp.choices else ""
        if not content:
            return {"llm_result": ""}
        try:
            parsed = json.loads(content)
            return {"llm_result": parsed}
        except Exception:
            return {"llm_result": content}
    except Exception as e:
        return {"error": f"openai_sdk_error: {str(e)}"}


# ---- 收集 JSON 文件 ----

def collect_json_files(folder_path: str):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for fn in filenames:
            if fn.lower().endswith(".json"):
                files.append(os.path.join(root, fn))
    return files


def safe_preview(s: str, n: int = 200):
    s = s or ""
    return s[:n] + ("..." if len(s) > n else "")


# ---- 主流程 ----

def main():
    print("递归查找所有 json 文件...")
    json_files = collect_json_files(FOLDER_PATH)
    total = len(json_files)
    print(f"共找到 {total} 个 json 文件。")
    if total == 0:
        print("没有找到任何 json 文件，退出。")
        return

    take = min(MAX_FILES, total)
    selected = random.sample(json_files, take)
    print(f"已随机选取 {take} 个文件，开始逐个处理...")

    # 若已有输出文件则加载已存在进度，便于断点续传
    results = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as rf:
                existing = json.load(rf)
                if isinstance(existing, list):
                    results = existing
                    print(f"检测到已有结果文件（{OUTPUT_FILE}），已加载 {len(results)} 条记录，将在其基础上追加。")
        except Exception:
            print("警告：读取已存在输出文件失败，将重新开始写入。")
            traceback.print_exc()
            results = []

    # 为避免重复处理，记录已经处理过的文件+snippet hash（可用 file path + snippet preview 来判断）
    seen = set()
    for r in results:
        key = (r.get("file"), r.get("malicious_code_preview"))
        seen.add(key)

    # 预先初始化 OpenAI SDK（便于尽早发现配置/依赖问题）
    try:
        _init_openai_from_config()
    except Exception as e:
        print(f"[初始化失败] {e}")
        return

    for idx, file_path in enumerate(selected, start=1):
        print(f"[{idx}/{take}] 处理: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [JSON 读取失败] {file_path}: {e}")
            # 将错误记录到结果文件以便后续分析
            results.append({
                "file": file_path,
                "error": f"json_read_error: {str(e)}"
            })
            with open(OUTPUT_FILE, "w", encoding="utf-8") as of:
                json.dump(results, of, indent=2, ensure_ascii=False)
            continue

        snippets = data.get("malicious_snippets", [])
        if not isinstance(snippets, list):
            snippets = []

        for sn in snippets:
            code = sn.get("malicious_code", "") if isinstance(sn, dict) else ""
            if not code or not str(code).strip():
                continue

            preview = safe_preview(code, n=200)
            key = (file_path, preview)
            if key in seen:
                print("    - 已存在记录，跳过。")
                continue

            # 构造提问 prompt：指示 LLM 仅判断核心恶意逻辑是否存在，行数可多可少
            prompt = (
                "你是一个安全分析助手。下面给出一段 JavaScript/Node.js 代码片段（可能包含被截断或被省略的上下文）。\n"
                "请分析并回答：该片段是否包含**核心恶意逻辑**（例如：远程命令执行、下载并执行二进制、数据/凭证外泄、滥用内置模块进行任意命令执行、动态代码执行、反静态分析绕过等）？\n"
                "只有明确一定不是恶意代码的片段才认定为良性，除此之外请全部认定为恶意\n"
                "只需给出一段简短的 JSON 风格回答（不要多余废话），字段包括：\n"
                "  - verdict: \"malicious\" / \"benign\" / \n"
                # "  - verdict: \"malicious\" / \"benign\" / \"uncertain\"\n"
                "  - reason: 用一句话说明判定依据（核心恶意行为是什么）\n"
                "  - confidence: 0-1 之间的估计分数（可选）\n\n"
                "注意：我们只关心“核心恶意逻辑”是否存在，代码行数多或少并不重要。下面是代码：\n\n"
                "-----BEGIN CODE-----\n"
                f"{code}\n"
                "-----END CODE-----\n"
            )

            print(f"    - 调用 LLM（预览：{preview[:80]}） ...")
            llm_resp = _call_llm_openai_sdk(prompt, timeout=60)

            entry = {
                "file": file_path,
                "malicious_code_preview": preview,
                "llm_response": llm_resp,
                "timestamp": int(time.time())
            }
            results.append(entry)
            seen.add(key)

            # 每个 snippet 之间短暂睡眠以避免速率问题（可根据需要调整或注释）
            time.sleep(0.2)

        # 每处理完一个文件就写回一次，便于断点续传
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as of:
                json.dump(results, of, indent=2, ensure_ascii=False)
            print(f"  - 当前进度已写入 {OUTPUT_FILE}（总记录 {len(results)}）")
        except Exception as e:
            print(f"  [写入结果失败] {e}")
            traceback.print_exc()

    print("全部完成。最终结果保存在:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
