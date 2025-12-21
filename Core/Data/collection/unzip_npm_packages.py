#!/usr/bin/env python3

import os
import tarfile
import zipfile


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def untar_file(raw_filepath, unzip_filepath):
    with tarfile.open(raw_filepath) as tf:
        tf.extractall(unzip_filepath)
    return unzip_filepath


def unzip_file(raw_filepath, unzip_filepath):
    with zipfile.ZipFile(raw_filepath, "r") as zf:
        for member in zf.namelist():
            zf.extract(member, unzip_filepath)
    return unzip_filepath


def decompress_package(filepath, unzip_filepath):
    mkdir(unzip_filepath)

    try:
        if filepath.endswith(".tar.gz") or filepath.endswith(".tgz"):
            return untar_file(filepath, unzip_filepath)
        elif filepath.endswith(".zip") or filepath.endswith(".whl"):
            return unzip_file(filepath, unzip_filepath)
        else:
            print(f"Unsupported file format: {filepath}")
            return filepath
    except Exception as e:
        print(f"Failed to decompress {filepath}: {e}")
        return filepath


def process_npm_packages(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print(f"Input directory does not exist: {input_dir}")
        return

    mkdir(output_dir)

    total_packages = 0
    successful_unzips = 0
    failed_unzips = 0

    print(f"Processing directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    for pkg_name in os.listdir(input_dir):
        pkg_path = os.path.join(input_dir, pkg_name)
        if not os.path.isdir(pkg_path):
            continue

        for version in os.listdir(pkg_path):
            version_path = os.path.join(pkg_path, version)
            if not os.path.isdir(version_path):
                continue

            for filename in os.listdir(version_path):
                file_path = os.path.join(version_path, filename)
                if not os.path.isfile(file_path):
                    continue

                output_pkg_dir = os.path.join(output_dir, pkg_name)
                output_version_dir = os.path.join(output_pkg_dir, version)

                total_packages += 1
                try:
                    decompress_package(file_path, output_version_dir)
                    print(f"Success: {pkg_name}/{version}/{filename}")
                    successful_unzips += 1
                except Exception as e:
                    print(f"Failed: {pkg_name}/{version}/{filename} - Error: {str(e)}")
                    failed_unzips += 1

    print("\nDecompression Summary:")
    print(f"Total packages: {total_packages}")
    print(f"Successful: {successful_unzips}")
    print(f"Failed: {failed_unzips}")


if __name__ == "__main__":
    benign_input_dir = "/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_benign"
    benign_output_dir = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign"
    malware_input_dir = "/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware"
    malware_output_dir = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"

    print("==== Decompressing benign NPM packages ====")
    process_npm_packages(benign_input_dir, benign_output_dir)

    print("\n==== Decompressing malware NPM packages ====")
    process_npm_packages(malware_input_dir, malware_output_dir)

    print("\nAll decompression tasks completed!")
