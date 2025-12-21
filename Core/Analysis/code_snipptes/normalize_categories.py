#!/usr/bin/env python3

import sys
import os
import json
import hashlib
from typing import List, Dict, Set, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Utils.llm_client import LLMClient

SNIPPETS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/malware_snippets"

COMMON_BEHAVIORS = [
    "data_exfiltration",
    "sensitive_data_collection",
    "credential_theft",
    "remote_code_execution",
    "arbitrary_command_execution",
    "malicious_download",
    "persistence_installation",
    "backdoor_installation",
    "command_and_control",
    "botnet_activity",
    "privilege_escalation",
    "unauthorized_access",
    "cryptocurrency_mining",
    "denial_of_service",
]

COMMON_EVASIONS = [
    "string_obfuscation",
    "base64_encoding",
    "hex_encoding",
    "code_splitting",
    "dynamic_evaluation",
    "sandbox_detection",
    "environment_detection",
    "timing_based_evasion",
    "conditional_execution",
    "dependency_confusion",
    "typosquatting",
    "install_script_abuse",
    "postinstall_hook_abuse",
    "preinstall_hook_abuse",
    "legitimate_api_abuse",
    "built_in_module_abuse",
    "native_code_execution",
    "silent_error_handling",
    "error_suppression",
    "domain_generation",
    "network_traffic_blending",
    "encrypted_communication",
]


class CategoryNormalizer:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.llm_client = LLMClient()
        self.known_behaviors: Set[str] = set(COMMON_BEHAVIORS)
        self.known_evasions: Set[str] = set(COMMON_EVASIONS)
        self.analyzed_code_cache: Dict[str, Tuple[List[str], List[str]]] = {}

        self.total_snippets = 0
        self.analyzed_snippets = 0
        self.cached_snippets = 0
        self.skipped_snippets = 0

        self._prescan_all_json_files()


    def _prescan_all_json_files(self):
        print("Pre-scanning all JSON files to collect existing categories...")

        total_packages = 0
        scanned_packages = 0
        scanned_files = 0
        found_behaviors = 0
        found_evasions = 0

        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if os.path.isdir(package_path):
                total_packages += 1

        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if not os.path.isdir(package_path):
                continue

            scanned_packages += 1
            print(f"\rPre-scan progress: [{scanned_packages}/{total_packages}] packages", end="")

            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                if not os.path.isdir(version_path):
                    continue

                json_path = os.path.join(version_path, "result.json")
                if not os.path.exists(json_path):
                    continue

                scanned_files += 1

                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    if "malicious_snippets" not in data:
                        continue

                    for snippet in data["malicious_snippets"]:
                        if "behavior_formal" in snippet and "evasion_formal" in snippet:
                            if snippet["behavior_formal"]:
                                if isinstance(snippet["behavior_formal"], list):
                                    for behavior in snippet["behavior_formal"]:
                                        self.known_behaviors.add(behavior)
                                        found_behaviors += 1
                                else:
                                    self.known_behaviors.add(snippet["behavior_formal"])
                                    found_behaviors += 1

                            if snippet["evasion_formal"]:
                                if isinstance(snippet["evasion_formal"], list):
                                    for evasion in snippet["evasion_formal"]:
                                        self.known_evasions.add(evasion)
                                        found_evasions += 1
                                else:
                                    self.known_evasions.add(snippet["evasion_formal"])
                                    found_evasions += 1

                            if "malicious_code" in snippet:
                                code_hash = self._get_code_hash(snippet["malicious_code"])
                                if code_hash not in self.analyzed_code_cache:
                                    bf = snippet["behavior_formal"] if isinstance(snippet["behavior_formal"], list) else [snippet["behavior_formal"]]
                                    ef = snippet["evasion_formal"] if isinstance(snippet["evasion_formal"], list) else [snippet["evasion_formal"]]
                                    self.analyzed_code_cache[code_hash] = (bf, ef)

                except Exception as e:
                    print(f"\nError pre-scanning file {json_path}: {e}")

        print(f"\nPre-scan complete! Scanned {scanned_files} files")
        print(f"Found {found_behaviors} behavior categories, {found_evasions} evasion techniques")
        print(f"Known behaviors: {len(self.known_behaviors)}")
        print(f"Known evasions: {len(self.known_evasions)}")
        print(f"Cache size: {len(self.analyzed_code_cache)} code hashes")
        print("")


    def _get_code_hash(self, code: str) -> str:
        return hashlib.md5(code.encode('utf-8')).hexdigest()


    def analyze_all_packages(self):
        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if not os.path.isdir(package_path):
                continue

            print(f"Analyzing package: {package_name}")
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                if not os.path.isdir(version_path):
                    continue

                json_path = os.path.join(version_path, "result.json")
                if os.path.exists(json_path):
                    self.analyze_package_json(json_path)

        print("\nAnalysis statistics:")
        print(f"Total snippets: {self.total_snippets}")
        print(f"Actually analyzed: {self.analyzed_snippets}")
        print(f"Cache reused: {self.cached_snippets}")
        print(f"Skipped (already analyzed): {self.skipped_snippets}")
        if (self.analyzed_snippets + self.cached_snippets) > 0:
            cache_hit_rate = self.cached_snippets / (self.analyzed_snippets + self.cached_snippets) * 100
            print(f"Cache hit rate: {cache_hit_rate:.2f}%")


    def analyze_package_json(self, json_path: str):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "malicious_snippets" not in data:
                print(f"Warning: {json_path} has no malicious_snippets field")
                return

            modified = False
            for snippet in data["malicious_snippets"]:
                self.total_snippets += 1

                if "malicious_code" not in snippet or "behavior_summary" not in snippet or "evasion_techniques" not in snippet:
                    continue

                if "behavior_formal" in snippet and "evasion_formal" in snippet:
                    self.skipped_snippets += 1
                    continue

                code_hash = self._get_code_hash(snippet["malicious_code"])
                if code_hash in self.analyzed_code_cache:
                    behavior_formal, evasion_formal = self.analyzed_code_cache[code_hash]
                    self.cached_snippets += 1
                    print(f"  Using cached result (hash: {code_hash[:8]}...)")
                else:
                    behavior_formal, evasion_formal = self.analyze_snippet(
                        snippet["malicious_code"],
                        snippet["behavior_summary"],
                        snippet["evasion_techniques"]
                    )
                    self.analyzed_snippets += 1
                    self.analyzed_code_cache[code_hash] = (behavior_formal, evasion_formal)

                snippet["behavior_formal"] = behavior_formal
                snippet["evasion_formal"] = evasion_formal
                modified = True

                for behavior in behavior_formal:
                    self.known_behaviors.add(behavior)
                for evasion in evasion_formal:
                    self.known_evasions.add(evasion)

            if modified:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"Updated: {json_path}")

        except Exception as e:
            print(f"Error processing {json_path}: {e}")


    def analyze_snippet(self, code: str, behavior_summary: str, evasion_techniques: str) -> Tuple[List[str], List[str]]:
        prompt = self._build_prompt(code, behavior_summary, evasion_techniques)

        messages = [
            {"role": "system", "content": "You are a security expert specializing in malware analysis, particularly focusing on NPM package malware."},
            {"role": "user", "content": prompt}
        ]

        response = self.llm_client.perform_query(
            messages=messages,
            temperature=0,
            seed=42,
            response_format={"type": "json_object"}
        )

        try:
            result = json.loads(response)
            behavior_formal = result.get("behavior_formal", [])
            evasion_formal = result.get("evasion_formal", [])

            if isinstance(behavior_formal, str):
                behavior_formal = [behavior_formal]
            if isinstance(evasion_formal, str):
                evasion_formal = [evasion_formal]

            return behavior_formal, evasion_formal

        except json.JSONDecodeError:
            print(f"LLM returned invalid JSON: {response}")
            return ["unknown"], ["unknown"]


    def _build_prompt(self, code: str, behavior_summary: str, evasion_techniques: str) -> str:
        known_behaviors_list = sorted(list(self.known_behaviors))
        known_evasions_list = sorted(list(self.known_evasions))

        behaviors_display = "Known behavior categories:\n"
        for behavior in known_behaviors_list:
            behaviors_display += f"- {behavior}\n"

        evasions_display = "Known evasion techniques:\n"
        for evasion in known_evasions_list:
            evasions_display += f"- {evasion}\n"

        prompt = f"""
Please analyze the following malicious code snippet from an NPM package, its behavior summary, and evasion techniques.

## Malicious Code:
```javascript
{code}
```

## Behavior Summary:
{behavior_summary}

## Evasion Techniques:
{evasion_techniques}

## Important Note:
If the Behavior Summary or Evasion Techniques sections above are empty, please analyze the code directly to determine:
- The malware's behavior and purpose (what it does)
- Any evasion techniques used (how it tries to hide or avoid detection)

Note that not all malicious code uses evasion techniques. If the code doesn't employ any evasion methods, you can return an empty list for evasion_formal.

Your task is to normalize the behavior and evasion techniques into standardized formal categories.

## Behavior Categories
{behaviors_display}

## Evasion Techniques
{evasions_display}

Respond with a JSON object in this exact format:
{{
  "behavior_formal": ["category1", "category2", ...],
  "evasion_formal": ["technique1", "technique2", ...]
}}

Instructions:
1. For behavior_formal, identify ALL applicable behavior categories (at least one)
2. For evasion_formal, identify ALL applicable evasion techniques (can be empty if none are used)
3. Use concise, snake_case naming for all categories
4. Try to reuse existing categories when appropriate
5. Create new categories only when necessary
"""
        return prompt


def main():
    normalizer = CategoryNormalizer(SNIPPETS_DIR)
    normalizer.analyze_all_packages()

    print("\nAnalysis complete!")
    print(f"Identified behavior categories ({len(normalizer.known_behaviors)}):")
    for behavior in sorted(normalizer.known_behaviors):
        print(f"- {behavior}")

    print(f"\nIdentified evasion techniques ({len(normalizer.known_evasions)}):")
    for evasion in sorted(normalizer.known_evasions):
        print(f"- {evasion}")


if __name__ == "__main__":
    main()
