#!/usr/bin/env python3

import os
import re
from collections import defaultdict

GUARDDOG_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/tool_detect/tool_output/guarddog/malware"
OUTPUT_FILE = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/npm_install_script_stats.txt"


def analyze_txt_file(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if "Found 0 potentially malicious indicators" in content or "benign" in content.lower():
            return "benign", []

        behavior_types = []
        matches = re.findall(r'^([\w\-]+): found (\d+) .* matches', content, re.MULTILINE)

        for behavior_type, count_str in matches:
            behavior_types.append(behavior_type)

        if len(behavior_types) == 1 and behavior_types[0] == "npm-install-script":
            file_matches = re.findall(r'\*.*?\s+at\s+([\w\-\.\/]+(?:\.js|\.json|\.py|\.ts)):(\d+)', content)
            json_only = all(path.endswith('package.json') for path, _ in file_matches)

            if json_only:
                return "npm-install-script-only", file_matches
            else:
                return "npm-install-script-mixed", file_matches

        return "mixed", behavior_types

    except Exception as e:
        print(f"Error analyzing file {txt_path}: {e}")
        return "error", []


def main():
    stats = {
        "total": 0,
        "benign": 0,
        "npm-install-script-only": 0,
        "npm-install-script-mixed": 0,
        "mixed": 0,
        "error": 0
    }

    packages_by_type = defaultdict(list)

    for root, dirs, files in os.walk(GUARDDOG_DIR):
        for file in files:
            if file.endswith('.txt'):
                stats["total"] += 1
                txt_path = os.path.join(root, file)

                parts = txt_path.split('/')
                if len(parts) >= 3:
                    package_name = parts[-3]
                    version = parts[-2]
                    package_info = f"{package_name}@{version}"
                else:
                    package_info = txt_path

                result_type, details = analyze_txt_file(txt_path)
                stats[result_type] += 1
                packages_by_type[result_type].append(package_info)

                if stats["total"] % 100 == 0:
                    print(f"Processed {stats['total']} files...")

    print("\n=== Statistics ===")
    print(f"Total files: {stats['total']}")
    print(f"Benign files: {stats['benign']}")
    print(f"npm-install-script only (package.json): {stats['npm-install-script-only']}")
    print(f"npm-install-script only (mixed files): {stats['npm-install-script-mixed']}")
    print(f"Multiple behavior types: {stats['mixed']}")
    print(f"Error files: {stats['error']}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("=== Statistics ===\n")
        f.write(f"Total files: {stats['total']}\n")
        f.write(f"Benign files: {stats['benign']}\n")
        f.write(f"npm-install-script only (package.json): {stats['npm-install-script-only']}\n")
        f.write(f"npm-install-script only (mixed files): {stats['npm-install-script-mixed']}\n")
        f.write(f"Multiple behavior types: {stats['mixed']}\n")
        f.write(f"Error files: {stats['error']}\n\n")

        f.write("=== Packages with npm-install-script only (package.json) ===\n")
        for package in sorted(packages_by_type["npm-install-script-only"]):
            f.write(f"{package}\n")

        f.write("\n=== Packages with npm-install-script only (mixed files) ===\n")
        for package in sorted(packages_by_type["npm-install-script-mixed"]):
            f.write(f"{package}\n")

    print(f"\nDetailed results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
