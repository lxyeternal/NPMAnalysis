#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from typing import Dict, Any, Tuple

RESULTS_PATH = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/rebuttal/taxonomy_check_results.json"

# 从 file 路径中提取 version key，例如
# /.../malware_snippets/fe-commons/12.1.11/result.json -> fe-commons/12.1.11
_VERSION_RE = re.compile(r"/malware_snippets/([^/]+)/([^/]+)/result\.json$")


def extract_version_key(file_path: str) -> str:
    m = _VERSION_RE.search(file_path)
    if not m:
        return ""
    return f"{m.group(1)}/{m.group(2)}"


def extract_verdict(entry: Dict[str, Any]) -> str:
    """从单条结果中尽力解析 verdict，返回 'correct'/'incorrect'/''（未知或无法解析）。"""
    resp = entry.get("llm_response")
    if not isinstance(resp, dict):
        return ""

    # 常见结构：{"llm_result": {"verdict": "correct", ...}}
    payload = resp.get("llm_result")
    if isinstance(payload, dict):
        verdict = payload.get("verdict")
        if isinstance(verdict, str):
            v = verdict.strip().lower()
            if v in ("correct", "incorrect"):
                return v
            # 兼容旧值
            if v == "uncertain":
                return ""
        return ""

    # 若 llm_result 是字符串，尝试解析 JSON
    if isinstance(payload, str):
        try:
            obj = json.loads(payload)
            if isinstance(obj, dict):
                verdict = obj.get("verdict")
                if isinstance(verdict, str):
                    v = verdict.strip().lower()
                    if v in ("correct", "incorrect"):
                        return v
        except Exception:
            return ""

    return ""


def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"结果文件不存在: {RESULTS_PATH}")
        return

    try:
        with open(RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取结果文件失败: {e}")
        return

    if not isinstance(data, list):
        print("结果文件格式错误：应为列表(list)")
        return

    # 统计（summary 级别即逐条统计）
    summary_correct = 0
    summary_incorrect = 0

    # 统计（version 级别）
    # 采用聚合规则：只要该 version 下任一条为 incorrect，则该 version 计为 incorrect；
    # 否则若存在 correct 且没有 incorrect，则该 version 计为 correct；
    # 若该 version 都无法解析 verdict，则忽略。
    version_to_flags: Dict[str, Tuple[bool, bool]] = {}

    for entry in data:
        file_path = entry.get("file", "")
        verdict = extract_verdict(entry)

        # summary 级别（逐条）
        if verdict == "correct":
            summary_correct += 1
        elif verdict == "incorrect":
            summary_incorrect += 1
        # 其它（空/未知）不计入

        # version 聚合
        version_key = extract_version_key(file_path)
        if not version_key:
            continue
        had_inc, had_cor = version_to_flags.get(version_key, (False, False))
        if verdict == "incorrect":
            had_inc = True
        elif verdict == "correct":
            had_cor = True
        version_to_flags[version_key] = (had_inc, had_cor)

    # 根据规则汇总 version 级别
    version_incorrect = 0
    version_correct = 0
    for version_key, (had_inc, had_cor) in version_to_flags.items():
        if had_inc:
            version_incorrect += 1
        elif had_cor:
            version_correct += 1
        # 两者皆否（全未解析）则忽略

    print("=== 按 summary（逐条）统计 ===")
    print(f"correct:   {summary_correct}")
    print(f"incorrect: {summary_incorrect}")

    print("\n=== 按 version（fe-commons/12.1.11 这种目录对）统计 ===")
    print(f"correct:   {version_correct}")
    print(f"incorrect: {version_incorrect}")


if __name__ == "__main__":
    main()