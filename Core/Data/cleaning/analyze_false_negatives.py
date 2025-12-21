#!/usr/bin/env python3

import os
import glob
import json
import sys
import multiprocessing

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Utils.llm_client import LLMClient

OUTPUT_TXT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/false_negatives.txt"
UNZIP_MALWARE_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
OUTPUT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/package_label"
PROMPTS_PATH = "/home2/wenbo/Documents/NPMAnalysis/Resource/Prompts"

os.makedirs(OUTPUT_PATH, exist_ok=True)

NUM_PROCESSES = 24


def load_prompt_template(prompt_file):
    prompt_path = os.path.join(PROMPTS_PATH, prompt_file)
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Failed to load prompt template {prompt_path}: {e}")
        return None


PACKAGE_JSON_PROMPT_TEMPLATE = load_prompt_template("package_json_analysis_prompt.txt")
JS_CODE_PROMPT_TEMPLATE = load_prompt_template("js_code_analysis_prompt.txt")


def get_source_files(package_path):
    result = {}
    file_paths = {}

    package_json_path = None
    for path in glob.glob(os.path.join(package_path, "**/package.json"), recursive=True):
        if os.path.dirname(path) == package_path:
            package_json_path = path
            break
        elif package_json_path is None:
            package_json_path = path

    if package_json_path:
        try:
            with open(package_json_path, 'r', encoding='utf-8', errors='ignore') as f:
                result['package.json'] = f.read()
                file_paths['package.json'] = os.path.abspath(package_json_path)
        except Exception as e:
            print(f"Failed to read package.json: {e}")

    js_files = {}
    js_file_paths = {}
    for path in glob.glob(os.path.join(package_path, "**/*.js"), recursive=True):
        rel_path = os.path.relpath(path, package_path)
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                js_files[rel_path] = f.read()
                js_file_paths[rel_path] = os.path.abspath(path)
        except Exception as e:
            print(f"Failed to read {path}: {e}")

    result['js_files'] = js_files
    file_paths['js_files'] = js_file_paths
    return result, file_paths


def get_npm_prompt(file_content, is_package_json=False):
    if is_package_json:
        return PACKAGE_JSON_PROMPT_TEMPLATE.replace("{CODE}", file_content)
    else:
        return JS_CODE_PROMPT_TEMPLATE.replace("{CODE}", file_content)


def query_llm(llm_agent, prompt, is_package_json=False):
    try:
        messages = [
            {"role": "system", "content": "You are an expert malware code analyst."},
            {"role": "user", "content": prompt}
        ]

        content = llm_agent.perform_query(
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"}
        )

        try:
            analysis = json.loads(content)
            is_malicious = analysis.get("is_malicious", False)
            malicious_code = analysis.get("malicious_code", "")
            behavior_summary = analysis.get("behavior_summary", "")
            attack_type = analysis.get("attack_type", "") if is_package_json else None
            return is_malicious, malicious_code, behavior_summary, attack_type
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Original response: {content}")
            return False, "", "", None if not is_package_json else ""
    except Exception as e:
        error_str = str(e)
        if "context_length_exceeded" in error_str or "maximum context length" in error_str:
            print(f"File too large, exceeding model context length limit: {error_str}")
            attack_type = "other" if is_package_json else None
            return True, "File too large, automatically classified as potentially malicious.", "Large obfuscated file, likely malicious", attack_type

        print(f"Error querying LLM: {e}")
        return False, "", "", None if not is_package_json else ""


def analyze_file(file_content, is_package_json=False):
    llm_agent = LLMClient()

    if len(file_content) > 1024 * 1024:
        print(f"  File size exceeds 1MB ({len(file_content)/1024/1024:.2f}MB), automatically classified as malicious")
        attack_type = "other" if is_package_json else None
        return True, "File too large (over 1MB), automatically classified as potentially malicious.", "Large obfuscated file, likely malicious", attack_type

    prompt = get_npm_prompt(file_content, is_package_json)
    is_malicious, code, behavior, attack_type = query_llm(llm_agent, prompt, is_package_json)
    print(f"  LLM analysis result: {'Malicious' if is_malicious else 'Not malicious'}")

    return is_malicious, code, behavior, attack_type


def analyze_package(package_info):
    package_name, version, index, total = package_info

    print(f"\n[{index}/{total}] Starting analysis: {package_name}@{version}")

    unzip_package_path = os.path.join(UNZIP_MALWARE_PATH, package_name, version)
    if not os.path.exists(unzip_package_path):
        print(f"Unzipped package path does not exist: {unzip_package_path}")
        return None

    try:
        source_files, file_paths = get_source_files(unzip_package_path)
    except Exception as e:
        print(f"Error getting source files: {e}")
        return None

    if not source_files.get('package.json') and not source_files.get('js_files'):
        print(f"No files found to analyze: {package_name}@{version}")
        return None

    analysis_results = {
        "package_name": package_name,
        "version": version,
        "malicious_files": [],
        "malicious_code": {},
        "behavior_summaries": {},
        "attack_types": {}
    }

    if source_files.get('package.json'):
        package_json_path = file_paths['package.json']
        print(f"Analyzing package.json: {package_json_path}")
        is_malicious, malicious_code, behavior_summary, attack_type = analyze_file(source_files['package.json'], is_package_json=True)

        if is_malicious:
            analysis_results["malicious_files"].append(package_json_path)
            analysis_results["malicious_code"][package_json_path] = malicious_code
            analysis_results["behavior_summaries"][package_json_path] = behavior_summary
            analysis_results["attack_types"][package_json_path] = attack_type
            print(f"Malicious code found in package.json")
            print(f"Behavior: {behavior_summary}")
            print(f"Attack type: {attack_type}")

    js_files_list = list(source_files.get('js_files', {}).items())
    print(f"Found {len(js_files_list)} JS files")

    for i, (js_file, content) in enumerate(js_files_list):
        if len(content) < 100:
            continue

        js_file_path = file_paths['js_files'][js_file]
        file_size_mb = len(content) / 1024 / 1024
        print(f"Analyzing JS file [{i+1}/{len(js_files_list)}]: {js_file_path} (Size: {file_size_mb:.2f}MB)")

        is_malicious, malicious_code, behavior_summary, _ = analyze_file(content, is_package_json=False)

        if is_malicious:
            analysis_results["malicious_files"].append(js_file_path)
            analysis_results["malicious_code"][js_file_path] = malicious_code
            analysis_results["behavior_summaries"][js_file_path] = behavior_summary
            print(f"Malicious code found in {js_file}")
            print(f"Behavior: {behavior_summary}")

    output_package_dir = os.path.join(OUTPUT_PATH, package_name)
    output_version_dir = os.path.join(output_package_dir, version)
    os.makedirs(output_version_dir, exist_ok=True)

    output_file = os.path.join(output_version_dir, f"{package_name}-{version}-analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)

    print(f"[{index}/{total}] Analysis completed: {package_name}@{version}")
    print(f"Results saved to: {os.path.abspath(output_file)}")

    if analysis_results["malicious_files"]:
        print(f"Found {len(analysis_results['malicious_files'])} malicious files")
    else:
        print("No malicious code found")

    return analysis_results


def parse_output_txt():
    packages = []
    try:
        with open(OUTPUT_TXT_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('/')
                if len(parts) >= 2:
                    package_name = parts[0]
                    version = parts[1]
                    packages.append((package_name, version))
    except Exception as e:
        print(f"Error parsing output.txt: {e}")

    return packages


def save_summary(results, total_packages, summary_file):
    malicious_packages = []
    packages_with_detected_malicious_code = 0

    for result in results:
        if result["malicious_files"]:
            packages_with_detected_malicious_code += 1
            package_info = {
                "package_name": result["package_name"],
                "version": result["version"],
                "malicious_files": result["malicious_files"],
                "result_file": os.path.abspath(os.path.join(
                    OUTPUT_PATH,
                    result["package_name"],
                    result["version"],
                    f"{result['package_name']}-{result['version']}-analysis.json"
                ))
            }

            if result["malicious_files"] and result["behavior_summaries"]:
                first_file = result["malicious_files"][0]
                package_info["behavior_summary"] = result["behavior_summaries"].get(first_file, "")

                for file_path in result["malicious_files"]:
                    if file_path.endswith("package.json") and file_path in result["attack_types"]:
                        package_info["attack_type"] = result["attack_types"].get(file_path, "")
                        break

            malicious_packages.append(package_info)

    summary_results = {
        "total_packages": total_packages,
        "packages_with_detected_malicious_code": packages_with_detected_malicious_code,
        "packages_with_no_detected_malicious_code": len(results) - packages_with_detected_malicious_code,
        "progress": f"{len(results)}/{total_packages}",
        "output_directory": os.path.abspath(OUTPUT_PATH),
        "malicious_packages": malicious_packages
    }

    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_results, f, ensure_ascii=False, indent=2)


def main():
    print("Starting analysis of packages from false_negatives.txt...")

    packages = parse_output_txt()

    if not packages:
        print("No packages found in false_negatives.txt file")
        return

    print(f"Found {len(packages)} packages to analyze")

    summary_file = os.path.join(OUTPUT_PATH, "analysis_summary.json")
    print(f"Summary file will be saved to: {os.path.abspath(summary_file)}")

    package_infos = []
    for i, (package_name, version) in enumerate(packages, 1):
        package_infos.append((package_name, version, i, len(packages)))

    results = []
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        for result in pool.imap_unordered(analyze_package, package_infos):
            if result:
                results.append(result)
                save_summary(results, len(packages), summary_file)

    save_summary(results, len(packages), summary_file)

    print(f"\nAnalysis completed! Analyzed {len(packages)} packages")
    print(f"Found {len([r for r in results if r['malicious_files']])} packages containing malicious code")
    print(f"All results have been saved to: {os.path.abspath(OUTPUT_PATH)}")
    print(f"Summary information saved to: {os.path.abspath(summary_file)}")


if __name__ == "__main__":
    if sys.platform == 'darwin':
        multiprocessing.set_start_method('spawn')
    main()
