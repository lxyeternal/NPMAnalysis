#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
verify_taxonomy.py

功能：
- 递归读取指定目录下所有 JSON 文件（malware_snippets 目录）
- 随机选择最多 500 个文件
- 对每个文件，读取 package_id，并查找 package_all_classifications.csv 中的分类
- 对每个文件内 malicious_snippets[*].malicious_code，调用 LLM 判断“该包的分类是否与代码片段相符”
- 将结果存放到 rebuttal/malicious_code_check_results.json（每处理一个文件即时写回）
- 直接使用 OpenAI Python SDK（从 rebuttal/llm_config.json 读取 openai_api_key / openai_api_model）
"""

import os
import sys
import json
import random
import time
import traceback
import csv

from typing import Any, Dict

# ==== 配置（可按需修改） ====
FOLDER_PATH = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/code_snipptes/malware_snippets"
CSV_PATH = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/behavior_annoation/key_results/summary_classifications.csv"
OUTPUT_DIR = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/rebuttal"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "taxonomy_check_results.json")
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

def load_package_classifications(csv_path):
    mapping = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[row["package_id"]] = row["classifications"]
    return mapping

def extract_package_id_from_json(json_path):
    # 期望路径格式：.../malware_snippets/{package_name}/{version}/result.json
    parts = os.path.normpath(json_path).split(os.sep)
    if len(parts) < 3:
        return os.path.splitext(os.path.basename(json_path))[0]
    # 倒数第三个是包名，倒数第二个是版本
    package_name = parts[-3]
    version = parts[-2]
    return f"{package_name}-{version}"

def main():
    print("加载包分类信息...")
    pkg_cls_map = load_package_classifications(CSV_PATH)
    print(f"共加载 {len(pkg_cls_map)} 个包的分类。")

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

    # 为避免重复处理，记录已经处理过的文件
    seen = set()
    for r in results:
        key = (r.get("file"))
        seen.add(key)

    # 预先初始化 OpenAI SDK（便于尽早发现配置/依赖问题）
    try:
        _init_openai_from_config()
    except Exception as e:
        print(f"[初始化失败] {e}")
        return

    for idx, file_path in enumerate(selected, start=1):
        print(f"[{idx}/{take}] 处理: {file_path}")
        pkg_id = extract_package_id_from_json(file_path)
        classifications = pkg_cls_map.get(pkg_id)
        if not classifications:
            print(f"  [未找到分类] {pkg_id}")
            continue

        if file_path in seen:
            print("    - 已存在记录，跳过。")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [JSON 读取失败] {file_path}: {e}")
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

            code_preview = safe_preview(code, n=200)
            key = (file_path, code_preview)
            # 只按文件去重，允许同文件多个片段
            if key in seen:
                print("    - 已存在记录，跳过。")
                continue

            prompt = (
                "你是一个安全分析助手。下面给出某个 npm 包的恶意代码片段和该包的行为分类，请判断这些分类是否合理、是否与代码片段内容相符。\n"
                "只有分类完全不一致的才认定为不正确，除此之外请全部认定为分类正确\n"
                "如果存在无法判断的情况，有可能的情况算作分类正确,完全没有关系的或者几乎非常没有关系的算作分类错误\n"
                "请严格用 JSON 格式回答：\n"
                "  - verdict: \"correct\" / \"incorrect\" \n"
                # "  - verdict: \"correct\" / \"incorrect\" / \"uncertain\"\n"
                "  - reason: 简要说明判断理由\n"
                "  - confidence: 0-1 之间的分数（可选）\n"
                "分类如下：\n"
                f"{classifications}\n"
                "代码片段如下：\n"
                f"{code_preview}\n"
            )

            print(f"    - 调用 LLM ...")
            llm_resp = _call_llm_openai_sdk(prompt, timeout=60)

            entry = {
                "file": file_path,
                "package_id": pkg_id,
                "classifications": classifications,
                "code_preview": code_preview,
                "llm_response": llm_resp,
                "timestamp": int(time.time())
            }
            results.append(entry)
            seen.add(key)

            # 每个 snippet 之间短暂睡眠以避免速率问题
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