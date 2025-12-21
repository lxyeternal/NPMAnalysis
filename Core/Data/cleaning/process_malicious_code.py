#!/usr/bin/env python3

import os
import json
import hashlib
import sys

SOURCE_DIR = '/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/package_label'
TARGET_DIR = '/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/malware_snippets'
UNZIP_MALWARE_PATH = '/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware'


def calculate_hash(code_string):
    return hashlib.md5(code_string.encode('utf-8')).hexdigest()


def process_package_file(package_path):
    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data.get('malicious_code'):
            return None

        package_name = data.get('package_name')
        version = data.get('version')

        if not package_name or not version:
            print(f"Missing package_name or version in {package_path}")
            return None

        result = {
            "metadata": {
                "package_name": package_name,
                "version": version,
                "report_path": "",
                "match_count": len(data.get('malicious_code', {})),
                "unzip_dir": f"{UNZIP_MALWARE_PATH}/{package_name}/{version}"
            },
            "malicious_snippets": []
        }

        attack_types = data.get('attack_types', {})

        for file_path, code in data.get('malicious_code', {}).items():
            file_name = os.path.basename(file_path)
            behavior_summary = data.get('behavior_summaries', {}).get(file_path, "Unknown behavior")

            evasion_techniques = ""
            if file_path in attack_types:
                evasion_techniques = attack_types[file_path]

            hash_value = calculate_hash(code)

            snippet = {
                "file": f"package/{file_name}",
                "line_number": "",
                "type": "",
                "malicious_code": code,
                "behavior_summary": behavior_summary,
                "evasion_techniques": evasion_techniques,
                "hash_value": hash_value
            }

            result["malicious_snippets"].append(snippet)

        return result
    except Exception as e:
        print(f"Error processing {package_path}: {e}")
        return None


def process_single_package(package_name, version):
    package_dir = os.path.join(SOURCE_DIR, package_name, version)
    if not os.path.exists(package_dir):
        print(f"Package directory not found: {package_dir}")
        return False

    analysis_file = f"{package_name}-{version}-analysis.json"
    file_path = os.path.join(package_dir, analysis_file)

    if not os.path.exists(file_path):
        print(f"Analysis file not found: {file_path}")
        return False

    result = process_package_file(file_path)

    if result and result["malicious_snippets"]:
        target_package_dir = os.path.join(TARGET_DIR, package_name, version)
        os.makedirs(target_package_dir, exist_ok=True)

        output_path = os.path.join(target_package_dir, 'result.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)

        print(f"{os.path.abspath(output_path)}")
        return True
    else:
        print(f"No malicious code found in {package_name}@{version}")
        return False


def main():
    if len(sys.argv) > 2:
        package_name = sys.argv[1]
        version = sys.argv[2]
        print(f"Processing single package: {package_name}@{version}")
        process_single_package(package_name, version)
        return

    os.makedirs(TARGET_DIR, exist_ok=True)

    processed_count = 0
    error_count = 0

    for package_name in os.listdir(SOURCE_DIR):
        package_dir = os.path.join(SOURCE_DIR, package_name)

        if not os.path.isdir(package_dir):
            continue

        try:
            for version in os.listdir(package_dir):
                version_path = os.path.join(package_dir, version)

                if not os.path.isdir(version_path):
                    continue

                analysis_files = [f for f in os.listdir(version_path) if f.endswith('-analysis.json')]

                for analysis_file in analysis_files:
                    file_path = os.path.join(version_path, analysis_file)

                    result = process_package_file(file_path)

                    if result and result["malicious_snippets"]:
                        pkg_name = result["metadata"]["package_name"]
                        ver = result["metadata"]["version"]
                        target_package_dir = os.path.join(TARGET_DIR, pkg_name, ver)
                        os.makedirs(target_package_dir, exist_ok=True)

                        output_path = os.path.join(target_package_dir, 'result.json')
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2)

                        print(f"{os.path.abspath(output_path)}")
                        processed_count += 1
        except Exception as e:
            error_count += 1
            print(f"Error processing directory {package_dir}: {e}")

    print(f"\nProcessing complete. Processed {processed_count} packages with {error_count} errors.")


if __name__ == "__main__":
    main()
