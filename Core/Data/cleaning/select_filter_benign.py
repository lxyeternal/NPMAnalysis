#!/usr/bin/env python3

import os
import random
import glob

BENIGN_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_benign"
OUTPUT_FILE = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/selected_benign_packages.txt"


def get_all_package_versions():
    package_versions = []

    for package_dir in glob.glob(os.path.join(BENIGN_PATH, "*")):
        if not os.path.isdir(package_dir):
            continue

        package_name = os.path.basename(package_dir)

        for version_dir in glob.glob(os.path.join(package_dir, "*")):
            if not os.path.isdir(version_dir):
                continue

            version = os.path.basename(version_dir)

            tgz_file = os.path.join(version_dir, f"{package_name}-{version}.tgz")
            if os.path.exists(tgz_file):
                package_versions.append((package_name, version))

    return package_versions


def main():
    print("Collecting all package versions...")
    all_versions = get_all_package_versions()
    total_versions = len(all_versions)
    print(f"Found {total_versions} package versions")

    num_to_select = min(1000, total_versions)
    selected_versions = random.sample(all_versions, num_to_select)

    with open(OUTPUT_FILE, "w") as f:
        for package_name, version in selected_versions:
            f.write(f"{package_name}/{version}\n")

    print(f"Successfully selected {num_to_select} package versions and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
