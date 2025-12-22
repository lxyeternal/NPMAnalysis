#!/usr/bin/env python3
"""
Clean Packj trace results that contain error patterns.
Identifies and optionally removes failed analysis results.
"""

import os
import re
import glob
import shutil
from collections import Counter


TRACE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/packj/result_trace/malware"


def find_error_files():
    """
    Find all result files containing error patterns.
    Returns list of file paths with errors.
    """
    total_files = 0
    error_files = []
    error_counter = Counter()
    all_patterns = set()

    result_files = glob.glob(f"{TRACE_DIR}/*/*/result.txt", recursive=True)
    code_pattern = re.compile(r'\[code\s+([^\]]+)\]')

    for file_path in result_files:
        total_files += 1
        has_error = False

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Check [code X] patterns
                matches = code_pattern.findall(content)
                if matches:
                    has_error = True
                    for match in matches:
                        code_value = match.strip()
                        error_counter[code_value] += 1
                        all_patterns.add(f"[code {code_value}]")

                # Check "list index out of range"
                if "list index out of range" in content:
                    has_error = True
                    error_counter["list index out of range"] += 1
                    all_patterns.add("[list index out of range]")

                # Check "KeyboardInterrupt"
                if "KeyboardInterrupt" in content:
                    has_error = True
                    error_counter["KeyboardInterrupt"] += 1
                    all_patterns.add("[KeyboardInterrupt]")

                if has_error:
                    error_files.append(file_path)

        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Print summary
    print(f"Total files checked: {total_files}")
    print(f"Files with errors: {len(error_files)}")
    if total_files > 0:
        print(f"Error rate: {len(error_files)/total_files:.2%}")

    print("\nError type statistics:")
    for error_type, count in sorted(error_counter.items(), key=lambda x: x[1], reverse=True):
        print(f"  [code {error_type}]: {count}")

    print("\nAll error patterns found:")
    for pattern in sorted(all_patterns):
        print(f"  {pattern}")

    return error_files


def delete_error_folders(files_list):
    """Delete version folders containing error files."""
    removed_versions = []
    removed_packages = []

    versions_to_remove = []
    packages_to_check = set()

    for file_path in files_list:
        version_dir = os.path.dirname(file_path)
        package_dir = os.path.dirname(version_dir)
        versions_to_remove.append(version_dir)
        packages_to_check.add(package_dir)

    # Remove version folders
    for version_dir in versions_to_remove:
        if os.path.exists(version_dir):
            shutil.rmtree(version_dir)
            removed_versions.append(version_dir)
            print(f"Removed version folder: {version_dir}")

    # Remove empty package folders
    for package_dir in packages_to_check:
        if os.path.exists(package_dir):
            remaining = [d for d in os.listdir(package_dir) if os.path.isdir(os.path.join(package_dir, d))]
            if not remaining:
                shutil.rmtree(package_dir)
                removed_packages.append(package_dir)
                print(f"Removed empty package folder: {package_dir}")

    print(f"\nRemoved {len(removed_versions)} version folders")
    print(f"Removed {len(removed_packages)} empty package folders")


def main():
    """Main function to find and clean error files."""
    print("Scanning for Packj trace error files...\n")
    error_files = find_error_files()

    if error_files:
        user_input = input("\nDelete version folders with errors? (yes/no): ")
        if user_input.lower() == "yes":
            print("\nDeleting folders...\n")
            delete_error_folders(error_files)
        else:
            print("Operation cancelled.")
    else:
        print("No error files found.")


if __name__ == "__main__":
    main()
