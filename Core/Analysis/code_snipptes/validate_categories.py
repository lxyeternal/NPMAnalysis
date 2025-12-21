#!/usr/bin/env python3

import sys
import os
import json
import hashlib
from typing import List, Dict, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Utils.llm_client import LLMClient

SNIPPETS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/malware_snippets"


class CategoryValidator:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.llm_client = LLMClient()

        self.validated_code_cache: Dict[str, Tuple[List[str], List[str]]] = {}
        self.code_only_cache: Dict[str, Tuple[List[str], List[str]]] = {}

        self.total_snippets = 0
        self.validated_snippets = 0
        self.cached_snippets = 0
        self.code_cached_snippets = 0
        self.skipped_snippets = 0
        self.unchanged_snippets = 0
        self.changed_snippets = 0


    def _get_code_hash(self, code: str, behavior_formal: List[str], evasion_formal: List[str]) -> str:
        combined = code + str(sorted(behavior_formal)) + str(sorted(evasion_formal))
        return hashlib.md5(combined.encode('utf-8')).hexdigest()


    def _get_pure_code_hash(self, code: str) -> str:
        return hashlib.md5(code.encode('utf-8')).hexdigest()


    def validate_all_packages(self):
        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if not os.path.isdir(package_path):
                continue

            print(f"Validating package: {package_name}")
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                if not os.path.isdir(version_path):
                    continue

                json_path = os.path.join(version_path, "result.json")
                if os.path.exists(json_path):
                    self.validate_package_json(json_path)

        print("\nValidation statistics:")
        print(f"Total snippets: {self.total_snippets}")
        print(f"Actually validated: {self.validated_snippets}")
        print(f"Full cache reused: {self.cached_snippets}")
        print(f"Code cache reused: {self.code_cached_snippets}")
        print(f"Skipped (unclassified): {self.skipped_snippets}")
        print(f"Classification unchanged: {self.unchanged_snippets}")
        print(f"Classification changed: {self.changed_snippets}")

        if (self.validated_snippets + self.cached_snippets + self.code_cached_snippets) > 0:
            unchanged_rate = self.unchanged_snippets / (self.validated_snippets + self.cached_snippets + self.code_cached_snippets) * 100
            print(f"Classification consistency rate: {unchanged_rate:.2f}%")

        print(f"\nCache statistics:")
        print(f"Full cache size: {len(self.validated_code_cache)}")
        print(f"Code cache size: {len(self.code_only_cache)}")

        if self.total_snippets > 0:
            cache_efficiency = (self.cached_snippets + self.code_cached_snippets) / self.total_snippets * 100
            print(f"Cache efficiency: {cache_efficiency:.2f}%")


    def validate_package_json(self, json_path: str):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "malicious_snippets" not in data:
                print(f"Warning: {json_path} has no malicious_snippets field")
                return

            modified = False
            for snippet in data["malicious_snippets"]:
                self.total_snippets += 1

                if "malicious_code" not in snippet or "behavior_formal" not in snippet or "evasion_formal" not in snippet:
                    self.skipped_snippets += 1
                    continue

                if "is_validated" in snippet and snippet["is_validated"] is True:
                    if "validate_behavior_formal" in snippet and "validate_evasion_formal" in snippet:
                        self.skipped_snippets += 1
                        continue

                    snippet["validate_behavior_formal"] = snippet["behavior_formal"]
                    snippet["validate_evasion_formal"] = snippet["evasion_formal"]
                    modified = True
                    self.unchanged_snippets += 1
                    print(f"  Already validated, copying original classification")
                    continue

                code = snippet["malicious_code"]
                behavior_formal = snippet["behavior_formal"]
                evasion_formal = snippet["evasion_formal"]

                if isinstance(behavior_formal, str):
                    behavior_formal = [behavior_formal]
                if isinstance(evasion_formal, str):
                    evasion_formal = [evasion_formal]

                code_hash = self._get_pure_code_hash(code)
                if code_hash in self.code_only_cache:
                    validate_behavior_formal, validate_evasion_formal = self.code_only_cache[code_hash]
                    self.code_cached_snippets += 1
                    print(f"  Using code cache result (hash: {code_hash[:8]}...)")

                    snippet["validate_behavior_formal"] = validate_behavior_formal
                    snippet["validate_evasion_formal"] = validate_evasion_formal

                    if (sorted(validate_behavior_formal) == sorted(behavior_formal) and
                        sorted(validate_evasion_formal) == sorted(evasion_formal)):
                        self.unchanged_snippets += 1
                        print(f"  Classification unchanged")
                    else:
                        self.changed_snippets += 1
                        print(f"  Classification changed: behavior={validate_behavior_formal}, evasion={validate_evasion_formal}")

                    snippet["is_validated"] = True
                    modified = True
                    continue

                full_hash = self._get_code_hash(code, behavior_formal, evasion_formal)
                if full_hash in self.validated_code_cache:
                    validate_behavior_formal, validate_evasion_formal = self.validated_code_cache[full_hash]
                    self.cached_snippets += 1
                    print(f"  Using full cache result (hash: {full_hash[:8]}...)")

                    snippet["validate_behavior_formal"] = validate_behavior_formal
                    snippet["validate_evasion_formal"] = validate_evasion_formal

                    if (sorted(validate_behavior_formal) == sorted(behavior_formal) and
                        sorted(validate_evasion_formal) == sorted(evasion_formal)):
                        self.unchanged_snippets += 1
                        print(f"  Classification unchanged")
                    else:
                        self.changed_snippets += 1
                        print(f"  Classification changed: behavior={validate_behavior_formal}, evasion={validate_evasion_formal}")
                else:
                    validate_behavior_formal, validate_evasion_formal = self.validate_snippet(
                        code,
                        behavior_formal,
                        evasion_formal
                    )
                    self.validated_snippets += 1

                    self.validated_code_cache[full_hash] = (validate_behavior_formal, validate_evasion_formal)
                    self.code_only_cache[code_hash] = (validate_behavior_formal, validate_evasion_formal)

                    snippet["validate_behavior_formal"] = validate_behavior_formal
                    snippet["validate_evasion_formal"] = validate_evasion_formal

                    if (sorted(validate_behavior_formal) == sorted(behavior_formal) and
                        sorted(validate_evasion_formal) == sorted(evasion_formal)):
                        self.unchanged_snippets += 1
                        print(f"  Classification unchanged")
                    else:
                        self.changed_snippets += 1
                        print(f"  Classification changed: behavior={validate_behavior_formal}, evasion={validate_evasion_formal}")

                snippet["is_validated"] = True
                modified = True

            if modified:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"Updated: {json_path}")

        except Exception as e:
            print(f"Error processing {json_path}: {e}")


    def validate_snippet(self, code: str, behavior_formal: List[str], evasion_formal: List[str]) -> Tuple[List[str], List[str]]:
        prompt = self._build_prompt(code, behavior_formal, evasion_formal)

        messages = [
            {"role": "system", "content": "You are a security expert specializing in malware analysis, particularly focusing on NPM package malware. Your task is to validate whether the provided behavior and evasion technique classifications accurately match the malicious code."},
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

            if "new_behavior_formal" in result:
                validate_behavior_formal = result["new_behavior_formal"]
            else:
                validate_behavior_formal = behavior_formal

            if "new_evasion_formal" in result:
                validate_evasion_formal = result["new_evasion_formal"]
            else:
                validate_evasion_formal = evasion_formal

            return validate_behavior_formal, validate_evasion_formal

        except json.JSONDecodeError:
            print(f"LLM returned invalid JSON: {response}")
            return behavior_formal, evasion_formal


    def _build_prompt(self, code: str, behavior_formal: List[str], evasion_formal: List[str]) -> str:
        prompt = f"""
Please validate whether the provided behavior and evasion technique classifications accurately match the malicious code.

## Malicious Code:
```javascript
{code}
```

## Current Classifications:
- Behavior: {behavior_formal}
- Evasion Techniques: {evasion_formal}

Your task is to determine if these classifications are accurate based on the code's actual functionality and techniques.

## Important Notes on Evasion Techniques:
- Evasion techniques focus specifically on how the malicious code attempts to AVOID DETECTION or ANALYSIS
- Not all malicious code uses evasion techniques - some malicious code is straightforward and doesn't try to hide
- Empty evasion_formal list is perfectly valid for malicious code that doesn't employ evasion methods
- Regular code patterns or optimizations are NOT evasion techniques

## Response Format:
- If the classifications are CORRECT, return an empty JSON object: {{}}
- If the classifications are INCORRECT, return a JSON object with new classifications:
  {{
    "new_behavior_formal": ["category1", "category2", ...],
    "new_evasion_formal": ["technique1", "technique2", ...]
  }}
  Note: new_evasion_formal can be an empty list if no evasion techniques are used

Instructions:
1. Be thorough in your analysis
2. Consider both explicit and implicit behaviors/techniques
3. If the classification is generally accurate but has minor issues, still consider it correct
4. Only suggest new classifications if there are significant discrepancies
5. Remember that evasion_formal can be an empty list if no evasion techniques are used
"""
        return prompt


def main():
    validator = CategoryValidator(SNIPPETS_DIR)
    validator.validate_all_packages()

    print("\nValidation complete!")


if __name__ == "__main__":
    main()
