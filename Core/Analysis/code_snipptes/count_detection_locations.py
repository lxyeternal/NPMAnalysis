#!/usr/bin/env python3
"""
Count unique detection locations for GuardDog and OSSGadget.
Each file is counted only once per package version.
"""

import os
import re

RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"


def extract_guarddog_files(content):
    """Extract unique file paths from GuardDog result."""
    stripped = content.strip()
    if ("Found 0 potentially malicious indicators" in content or
            stripped == "TIMEOUT" or stripped == "benign"):
        return set()
    # Match paths like "at package/xxx", "at tmp/xxx/package/xxx", or "at package.json"
    pattern = r' at (?:[^\s]*/)?([^\s:]+\.[a-zA-Z]+)'
    matches = re.findall(pattern, content)
    return set(matches)


def extract_ossgadget_files(content):
    """Extract unique file paths from OSSGadget result."""
    stripped = content.strip()
    if ("0 matches found." in content or stripped == "TIMEOUT" or
            stripped == "benign"):
        return set()
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    clean_content = ansi_escape.sub('', content)
    # Match file path after "Filename:", extract the part starting from /package/
    pattern = r'Filename:\s*[^\s]*(package/[^\s]+)'
    matches = re.findall(pattern, clean_content)
    return set(matches)


def count_tool_locations(tool_name, extract_func):
    """Count total unique file locations for a tool across all malware packages."""
    base_path = os.path.join(RESULTS_DIR, tool_name, "malware")
    total_files = 0
    total_versions = 0
    versions_with_detection = 0

    for package_name in os.listdir(base_path):
        package_dir = os.path.join(base_path, package_name)
        if not os.path.isdir(package_dir):
            continue
        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            result_file = os.path.join(version_dir, "result.txt")
            if not os.path.isfile(result_file):
                continue
            total_versions += 1
            with open(result_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            files = extract_func(content)
            if files:
                versions_with_detection += 1
                total_files += len(files)

    return total_versions, versions_with_detection, total_files


def main():
    print("=" * 60)
    print("Detection Location Statistics")
    print("=" * 60)

    gd_total, gd_detected, gd_files = count_tool_locations("guarddog", extract_guarddog_files)
    print(f"\nGuardDog:")
    print(f"  Total malware versions: {gd_total}")
    print(f"  Versions detected as malware: {gd_detected}")
    print(f"  Total unique file locations: {gd_files}")
    print(f"  Avg files per detected version: {gd_files/gd_detected:.2f}")

    oss_total, oss_detected, oss_files = count_tool_locations("ossgadget", extract_ossgadget_files)
    print(f"\nOSSGadget:")
    print(f"  Total malware versions: {oss_total}")
    print(f"  Versions detected as malware: {oss_detected}")
    print(f"  Total unique file locations: {oss_files}")
    print(f"  Avg files per detected version: {oss_files/oss_detected:.2f}")


if __name__ == "__main__":
    main()
