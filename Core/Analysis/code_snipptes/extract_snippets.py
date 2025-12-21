#!/usr/bin/env python3

import os
import json
import re
import sys
import hashlib
import multiprocessing
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Utils.llm_client import LLMClient

SOURCE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/tool_detect/tool_output/guarddog/malware"
TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/malware_snippets"
PROMPT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Resource/Prompts/single_snippets_prompt.txt"

NUM_PROCESSES = 24


def normalize_code(code_snippet):
    normalized = re.sub(r'\s+', '', code_snippet)
    normalized = normalized.lower()
    return normalized


def hash_code(code_snippet):
    normalized = normalize_code(code_snippet)
    return hashlib.md5(normalized.encode()).hexdigest()


def is_benign(txt_content):
    if "Found 0 potentially malicious indicators" in txt_content or "benign" in txt_content.lower():
        return True
    return False


def read_source_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def extract_malicious_locations(txt_content):
    archive_pattern = r'Found \d+ potentially malicious indicators in (.*?)(\.tar\.gz|\.zip|\.tgz|\.whl)'
    archive_match = re.search(archive_pattern, txt_content)

    if not archive_match:
        print("Warning: Cannot extract archive path")
        return None, 0, None

    zip_path = archive_match.group(1) + archive_match.group(2)
    print(f"Extracted archive path: {zip_path}")

    unzip_base_path = zip_path.replace('zip_malware', 'unzip_malware')
    unzip_dir = os.path.dirname(unzip_base_path)
    print(f"Unzipped directory path: {unzip_dir}")

    lines = txt_content.split('\n')
    malicious_locations = {}
    current_type = ""
    match_count = 0

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        type_match = re.match(r'^([\w\-]+): found (\d+) .* matches', line)
        if type_match:
            current_type = type_match.group(1)
            match_count_str = type_match.group(2)
            try:
                match_count += int(match_count_str)
            except ValueError:
                pass
            print(f"Found type: {current_type}")
            i += 1
            continue

        location_match = re.search(r'\*.*?\s+at\s+([\w\-\.\/]+(?:\.js|\.json|\.py|\.ts)):(\d+)', line)
        if location_match and current_type:
            relative_path = location_match.group(1)
            line_number = location_match.group(2)

            print(f"Found file location: {relative_path}:{line_number}")

            full_path = os.path.join(unzip_dir, relative_path)

            code_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line or next_line.startswith('*') or re.match(r'^[\w\-]+: found \d+ .* matches', next_line):
                    break
                code_lines.append(next_line)
                j += 1

            code_snippet = '\n'.join(code_lines)

            location_info = {
                'line_number': line_number,
                'type': current_type,
                'code_snippet': code_snippet,
                'full_match': line,
                'full_path': full_path,
                'relative_path': relative_path
            }

            if full_path not in malicious_locations:
                malicious_locations[full_path] = []
                print(f"Added new file path: {full_path}")

            malicious_locations[full_path].append(location_info)
            i = j
            continue

        i += 1

    if not malicious_locations:
        print("Warning: No malicious code locations found")
    else:
        print(f"Found {len(malicious_locations)} files with malicious code")

    return malicious_locations, match_count, unzip_dir


def process_with_llm(code_content, detection_info, prompt_template):
    try:
        with open(prompt_template, 'r', encoding='utf-8') as f:
            prompt = f.read()

        detection_context = "Detection information:\n"
        detection_context += f"- Line {detection_info['line_number']}: {detection_info['type']} found in file {detection_info['relative_path']}\n"
        detection_context += f"  Flagged code: {detection_info['code_snippet']}\n"

        code_with_context = f"{detection_context}\nSource code:\n{code_content}"
        prompt = prompt.replace("{CODE}", code_with_context)

        llm_client = LLMClient()

        messages = [
            {"role": "system", "content": "You are an expert malware code analyst."},
            {"role": "user", "content": prompt}
        ]

        response = llm_client.perform_query(messages)

        try:
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                extracted_context = json.loads(json_match.group(1))
            else:
                extracted_context = json.loads(response)

            return extracted_context
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Original response: {response}")
            return None

    except Exception as e:
        print(f"LLM processing failed: {e}")
        return None


def process_package(package_name, version, txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            txt_content = f.read()

        if is_benign(txt_content):
            print(f"{package_name}/{version} is benign, skipping")
            return None

        malicious_locations, match_count, unzip_dir = extract_malicious_locations(txt_content)

        if not malicious_locations or match_count == 0:
            print(f"{package_name}/{version} no malicious locations found, skipping")
            return None

        print(f"{package_name}/{version} found {match_count} malicious matches")

        result = []

        for file_path, locations in malicious_locations.items():
            code_content = read_source_code(file_path)
            if not code_content:
                print(f"Cannot read source code: {file_path}")
                continue

            for location in locations:
                print(f"Analyzing with LLM: {file_path}, line {location['line_number']}, type {location['type']}")
                llm_result = process_with_llm(code_content, location, PROMPT_PATH)

                if not llm_result:
                    print(f"LLM processing failed: {file_path}")
                    continue

                malicious_code = llm_result.get("malicious_code", "")
                behavior_summary = llm_result.get("behavior_summary", "")
                evasion_techniques = llm_result.get("evasion_techniques", "")

                if not malicious_code.strip():
                    print(f"LLM determined {file_path} line {location['line_number']} is not malicious, skipping")
                    continue

                malicious_entry = {
                    "file": location['relative_path'],
                    "line_number": location['line_number'],
                    "type": location['type'],
                    "malicious_code": malicious_code,
                    "behavior_summary": behavior_summary,
                    "evasion_techniques": evasion_techniques,
                    "hash_value": hash_code(malicious_code)
                }

                result.append(malicious_entry)

        if not result:
            print(f"{package_name}/{version} no valid malicious code found, skipping")
            return None

        metadata = {
            "package_name": package_name,
            "version": version,
            "report_path": txt_path,
            "match_count": match_count,
            "unzip_dir": unzip_dir
        }

        final_result = {
            "metadata": metadata,
            "malicious_snippets": result
        }

        target_package_dir = os.path.join(TARGET_DIR, package_name)
        target_version_dir = os.path.join(target_package_dir, version)
        os.makedirs(target_version_dir, exist_ok=True)

        json_path = os.path.join(target_version_dir, "result.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(final_result, f, ensure_ascii=False, indent=2)

        print(f"Saved result: {json_path}")
        return True

    except Exception as e:
        print(f"Error processing package {package_name}/{version}: {e}")
        return None


def process_single_package(package_info):
    package_name, version, txt_path = package_info
    print(f"\nProcess {os.getpid()} handling: {package_name}/{version}")
    return process_package(package_name, version, txt_path)


def collect_package_info():
    package_info_list = []

    for package_name in os.listdir(SOURCE_DIR):
        package_dir = os.path.join(SOURCE_DIR, package_name)
        if not os.path.isdir(package_dir):
            continue

        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            if not os.path.isdir(version_dir):
                continue

            txt_path = os.path.join(version_dir, "result.txt")
            if not os.path.exists(txt_path):
                continue

            target_package_dir = os.path.join(TARGET_DIR, package_name)
            target_version_dir = os.path.join(target_package_dir, version)
            json_path = os.path.join(target_version_dir, "result.json")

            if os.path.exists(json_path):
                print(f"Skipping already processed: {package_name}/{version}")
                continue

            package_info_list.append((package_name, version, txt_path))

    return package_info_list


def main():
    start_time = time.time()

    os.makedirs(TARGET_DIR, exist_ok=True)

    package_info_list = collect_package_info()
    print(f"Found {len(package_info_list)} packages to process")

    if not package_info_list:
        print("No packages to process, exiting")
        return

    print(f"Creating process pool with {NUM_PROCESSES} processes")
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        results = pool.map(process_single_package, package_info_list)

    processed = sum(1 for r in results if r is not None)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"\nProcessing complete: {processed}/{len(package_info_list)} packages succeeded")
    print(f"Total time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
