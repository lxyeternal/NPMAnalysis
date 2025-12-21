#!/usr/bin/env python3

import os
import json
import requests
import time
import multiprocessing
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

BASE_DIR = Path("/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_benign")
BASE_DIR.mkdir(exist_ok=True, parents=True)

TOTAL_PACKAGES = 15000
NUM_PROCESSES = 20
results_queue = multiprocessing.Manager().Queue()


def normalize_package_name(package_name):
    if package_name.startswith('@'):
        return package_name.replace('/', '##')
    return package_name


def fetch_popular_packages():
    url = "https://registry.npmjs.org/-/v1/search?text=popularity:>0.3&size=10000"

    try:
        packages = set()
        offset = 0

        while len(packages) < TOTAL_PACKAGES:
            print(f"Fetching package list, got {len(packages)} packages...")
            response = requests.get(f"{url}&from={offset}", timeout=30)
            response.raise_for_status()
            data = response.json()

            if "objects" not in data or not data["objects"]:
                break

            batch_packages = [obj["package"]["name"] for obj in data["objects"]]
            packages.update(batch_packages)
            offset += len(batch_packages)
            time.sleep(1)

        return list(packages)[:TOTAL_PACKAGES]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching package list: {e}")
        return []


def download_package_tarball(package_info):
    package_name, index = package_info
    normalized_name = normalize_package_name(package_name)
    package_dir = BASE_DIR / normalized_name

    tarball_files = list(package_dir.glob("*.tgz"))
    if package_dir.exists() and tarball_files:
        print(f"[{index}/{TOTAL_PACKAGES}] Package {package_name} already downloaded, skipping")
        results_queue.put((package_name, True, "skipped"))
        return True

    try:
        registry_url = f"https://registry.npmjs.org/{package_name}"
        response = requests.get(registry_url, timeout=30)
        response.raise_for_status()

        package_data = response.json()

        latest_version = package_data.get('dist-tags', {}).get('latest')
        if not latest_version and 'versions' in package_data:
            latest_version = list(package_data['versions'].keys())[-1]

        if not latest_version:
            print(f"[{index}/{TOTAL_PACKAGES}] Cannot determine latest version for {package_name}")
            results_queue.put((package_name, False, "version fetch failed"))
            return False

        tarball_url = package_data.get('versions', {}).get(latest_version, {}).get('dist', {}).get('tarball')

        if not tarball_url:
            print(f"[{index}/{TOTAL_PACKAGES}] Cannot get tarball URL for {package_name}")
            results_queue.put((package_name, False, "tarball URL fetch failed"))
            return False

        print(f"[{index}/{TOTAL_PACKAGES}] Downloading: {package_name}@{latest_version}")

        tarball_response = requests.get(tarball_url, timeout=60)
        tarball_response.raise_for_status()

        version_dir = package_dir / latest_version
        version_dir.mkdir(exist_ok=True, parents=True)

        tarball_path = version_dir / f"{normalized_name}-{latest_version}.tgz"
        with open(tarball_path, 'wb') as f:
            f.write(tarball_response.content)

        print(f"[{index}/{TOTAL_PACKAGES}] Successfully downloaded: {package_name}")
        results_queue.put((package_name, True, "success"))
        return True
    except requests.exceptions.RequestException as e:
        print(f"[{index}/{TOTAL_PACKAGES}] Network error downloading {package_name}: {e}")
        results_queue.put((package_name, False, f"network error: {str(e)[:100]}"))
        return False
    except Exception as e:
        print(f"[{index}/{TOTAL_PACKAGES}] Error downloading {package_name}: {e}")
        results_queue.put((package_name, False, f"other error: {str(e)[:100]}"))
        return False


def process_batch(batch_packages):
    for package_info in batch_packages:
        download_package_tarball(package_info)


def main():
    print("Fetching NPM popular package list...")
    packages = fetch_popular_packages()

    if not packages:
        print("Cannot get package list. Exiting.")
        return

    print(f"Found {len(packages)} packages. Starting download...")

    package_infos = [(pkg, i+1) for i, pkg in enumerate(packages)]

    batch_size = max(1, len(package_infos) // NUM_PROCESSES)
    batches = [package_infos[i:i+batch_size] for i in range(0, len(package_infos), batch_size)]

    with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        executor.map(process_batch, batches)

    successful = 0
    failed = 0
    skipped = 0
    failed_packages = []

    while not results_queue.empty():
        package_name, success, reason = results_queue.get()
        if success:
            if reason == "skipped":
                skipped += 1
            else:
                successful += 1
        else:
            failed += 1
            failed_packages.append((package_name, reason))

    print(f"\nDownload completed! Success: {successful}, Skipped: {skipped}, Failed: {failed}")

    if failed > 0:
        print("Failed packages:")
        for pkg, reason in failed_packages:
            print(f"  - {pkg}: {reason}")

        with open("failed_packages.txt", "w") as f:
            for pkg, reason in failed_packages:
                f.write(f"{pkg}: {reason}\n")


if __name__ == "__main__":
    main()
