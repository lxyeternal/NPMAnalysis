#!/usr/bin/env python3

import os
import shutil
import multiprocessing
import glob
from collections import defaultdict

GUARDDOG_MALWARE_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/tool_detect/tool_output/guarddog/malware"
UNZIP_MALWARE_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
DEST_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/false_negative"

NUM_PROCESSES = 24


def is_false_negative(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "Found 0 potentially malicious indicators" in content or content.strip() == "benign":
                return True
        return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False


def copy_package(package_info):
    package_name, version, guarddog_file_path, index, total = package_info

    if version:
        print(f"[{index}/{total}] Processing: {package_name}@{version}")
        src_package_path = os.path.join(UNZIP_MALWARE_PATH, package_name, version)
        dest_package_path = os.path.join(DEST_PATH, package_name, version)
    else:
        print(f"[{index}/{total}] Processing: {package_name} (no version)")
        src_package_path = os.path.join(UNZIP_MALWARE_PATH, package_name)
        dest_package_path = os.path.join(DEST_PATH, package_name)

    if not os.path.exists(src_package_path):
        print(f"  Source package path does not exist: {src_package_path}")
        return False

    if os.path.exists(dest_package_path):
        try:
            shutil.rmtree(dest_package_path)
        except Exception as e:
            print(f"  Error removing existing directory {dest_package_path}: {e}")
            return False

    try:
        os.makedirs(os.path.dirname(dest_package_path), exist_ok=True)
    except Exception as e:
        print(f"  Error creating directory {os.path.dirname(dest_package_path)}: {e}")
        return False

    try:
        shutil.copytree(src_package_path, dest_package_path)
        if version:
            print(f"  Successfully copied {package_name}@{version}")
        else:
            print(f"  Successfully copied {package_name}")
        return True
    except Exception as e:
        print(f"  Error copying package: {e}")
        return False


def count_existing_false_negatives():
    if not os.path.exists(DEST_PATH):
        return 0, 0, {}

    package_versions = defaultdict(list)
    package_count = 0
    version_count = 0

    for item in os.listdir(DEST_PATH):
        item_path = os.path.join(DEST_PATH, item)
        if os.path.isdir(item_path):
            package_count += 1

            sub_items = os.listdir(item_path)
            has_version_dirs = False

            for sub_item in sub_items:
                sub_item_path = os.path.join(item_path, sub_item)
                if os.path.isdir(sub_item_path):
                    has_version_dirs = True
                    package_versions[item].append(sub_item)
                    version_count += 1

            if not has_version_dirs:
                package_versions[item].append("(no version)")
                version_count += 1

    return package_count, version_count, package_versions


def main():
    os.makedirs(DEST_PATH, exist_ok=True)

    existing_packages, existing_versions, _ = count_existing_false_negatives()
    print(f"\n======= Existing false negatives =======")
    print(f"Found {existing_packages} packages, {existing_versions} versions missed by GuardDog")

    print("\nDetecting GuardDog false negatives...")

    false_negatives = []
    total_malware = 0
    packages_with_versions = defaultdict(list)

    for file_path in glob.glob(os.path.join(GUARDDOG_MALWARE_PATH, "**", "*.txt"), recursive=True):
        total_malware += 1

        if is_false_negative(file_path):
            rel_path = os.path.relpath(file_path, GUARDDOG_MALWARE_PATH)
            parts = rel_path.split(os.sep)

            if len(parts) >= 3:
                package_name = parts[0]
                version = parts[1]
                false_negatives.append((package_name, version, file_path))
                packages_with_versions[package_name].append(version)
            elif len(parts) == 2:
                package_name = parts[0]
                version = None
                false_negatives.append((package_name, version, file_path))
                packages_with_versions[package_name].append("(no version)")

    unique_packages = len(packages_with_versions)
    total_versions = len(false_negatives)

    print(f"Analyzed {total_malware} malware samples")
    print(f"Found {unique_packages} packages, {total_versions} versions missed by GuardDog")

    multiple_versions = {pkg: vers for pkg, vers in packages_with_versions.items() if len(vers) > 1}
    if multiple_versions:
        print("\nPackages with multiple missed versions (top 10):")
        for pkg, versions in sorted(multiple_versions.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"  {pkg}: {len(versions)} versions")

    if not false_negatives:
        print("No false negatives found.")
        return

    package_infos = []
    for i, (package_name, version, file_path) in enumerate(false_negatives, 1):
        package_infos.append((package_name, version, file_path, i, len(false_negatives)))

    success_count = 0
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        for result in pool.imap_unordered(copy_package, package_infos):
            if result:
                success_count += 1

    print(f"\nCopy completed! Successfully copied {success_count} false negative samples")
    print(f"All packages copied to: {os.path.abspath(DEST_PATH)}")

    print(f"\n======= Final statistics =======")
    final_packages, final_versions, _ = count_existing_false_negatives()
    print(f"Total {final_packages} packages, {final_versions} versions missed by GuardDog")


if __name__ == "__main__":
    main()
