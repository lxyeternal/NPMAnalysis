#!/usr/bin/env python3

import os
import json
import re

SNIPPETS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/malware_snippets"
OUTPUT_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes"


def analyze_install_scripts():
    preinstall_packages = []
    postinstall_packages = []
    install_packages = []
    combined_packages = []

    preinstall_pattern = re.compile(r'["\']preinstall["\']:\s*["\']')
    postinstall_pattern = re.compile(r'["\']postinstall["\']:\s*["\']')
    install_pattern = re.compile(r'["\']install["\']:\s*["\']')

    for root, dirs, files in os.walk(SNIPPETS_DIR):
        for file in files:
            if file == "result.json":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    package_name = data.get("metadata", {}).get("package_name", "unknown")
                    version = data.get("metadata", {}).get("version", "unknown")
                    package_info = f"{package_name}@{version} - {file_path}"

                    package_json_codes = set()

                    for snippet in data.get("malicious_snippets", []):
                        if snippet.get("file") == "package/package.json":
                            malicious_code = snippet.get("malicious_code", "")
                            package_json_codes.add(malicious_code)

                    has_preinstall = False
                    has_postinstall = False
                    has_install = False

                    for malicious_code in package_json_codes:
                        if preinstall_pattern.search(malicious_code) or "preinstall" in malicious_code:
                            has_preinstall = True

                        if postinstall_pattern.search(malicious_code) or "postinstall" in malicious_code:
                            has_postinstall = True

                        if install_pattern.search(malicious_code):
                            has_install = True

                    script_types = []

                    if has_preinstall:
                        preinstall_packages.append(package_info)
                        script_types.append("preinstall")

                    if has_postinstall:
                        postinstall_packages.append(package_info)
                        script_types.append("postinstall")

                    if has_install:
                        install_packages.append(package_info)
                        script_types.append("install")

                    if len(script_types) > 1:
                        combined_packages.append(f"{package_info} - script types: {', '.join(script_types)}")

                except Exception:
                    pass

    output_file = os.path.join(OUTPUT_DIR, "malicious_install_scripts_analysis.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Malicious Package Install Scripts Analysis\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"1. preinstall scripts (total: {len(preinstall_packages)})\n")
        f.write("-" * 80 + "\n")
        for pkg in preinstall_packages:
            f.write(f"  - {pkg}\n")
        f.write("\n\n")

        f.write(f"2. postinstall scripts (total: {len(postinstall_packages)})\n")
        f.write("-" * 80 + "\n")
        for pkg in postinstall_packages:
            f.write(f"  - {pkg}\n")
        f.write("\n\n")

        f.write(f"3. install scripts (total: {len(install_packages)})\n")
        f.write("-" * 80 + "\n")
        for pkg in install_packages:
            f.write(f"  - {pkg}\n")
        f.write("\n\n")

        f.write(f"4. Packages with multiple script types (total: {len(combined_packages)})\n")
        f.write("-" * 80 + "\n")
        for pkg in combined_packages:
            f.write(f"  - {pkg}\n")

    print(f"Analysis complete. Results saved to: {output_file}")
    print(f"preinstall: {len(preinstall_packages)}")
    print(f"postinstall: {len(postinstall_packages)}")
    print(f"install: {len(install_packages)}")
    print(f"multiple types: {len(combined_packages)}")


if __name__ == "__main__":
    analyze_install_scripts()
