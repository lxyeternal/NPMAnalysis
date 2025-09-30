#!/usr/bin/env python3
"""
Script to extract examples for each of the 15 classification behaviors.
Each example includes package name, version, malicious code context, and detection tool results.
"""

import csv
import json
import os
import re
from collections import defaultdict
from pathlib import Path

def normalize_package_name(package_name):
    """Normalize package name to match directory structure"""
    # Replace ## with ## for scoped packages
    if package_name.startswith('@'):
        return package_name.replace('@', '@').replace('##', '##')
    return package_name

def find_package_files(package_name, version, base_dirs):
    """Find relevant files for a package across different directories"""
    normalized_name = normalize_package_name(package_name)
    files = {}
    
    # Check malware snippets
    snippet_dir = base_dirs['snippets'] / normalized_name / version
    if snippet_dir.exists():
        result_file = snippet_dir / 'result.json'
        if result_file.exists():
            files['snippet'] = result_file
    
    # Check tool detection results
    for tool in ['genie', 'guarddog', 'ossgadget', 'socketai']:
        tool_dir = base_dirs['tools'] / tool / 'malware' / normalized_name
        if tool_dir.exists():
            # Look for version-specific files
            for file_path in tool_dir.rglob('*'):
                if file_path.is_file() and version in str(file_path):
                    files[tool] = file_path
                    break
    
    # Special handling for packj with static and trace modes
    # Check static mode
    static_dir = base_dirs['tools'] / 'packj' / 'result_static' / 'malware' / normalized_name / version
    if static_dir.exists():
        for file_path in static_dir.glob('*.txt'):
            files['packj_static'] = file_path
            break
    
    # Check trace mode
    trace_dir = base_dirs['tools'] / 'packj' / 'result_trace' / 'malware' / normalized_name / version
    if trace_dir.exists():
        for file_path in trace_dir.glob('*.txt'):
            files['packj_trace'] = file_path
            break
    
    return files

def get_sap_result(package_name, version, sap_file):
    """Get SAP detection result for a package"""
    try:
        with open(sap_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Package Name'] == f"{package_name}$${version}":
                    return {
                        'type': row.get('type', ''),
                        'DT': row.get('DT', ''),
                        'RF': row.get('RF', ''),
                        'XGB': row.get('XGB', '')
                    }
    except Exception as e:
        print(f"Error reading SAP results: {e}")
    return None

def extract_malicious_context(snippet_file):
    """Extract malicious code context from snippet file"""
    try:
        with open(snippet_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        context = {
            'package_name': data.get('metadata', {}).get('package_name', ''),
            'version': data.get('metadata', {}).get('version', ''),
            'snippets': []
        }
        
        for snippet in data.get('malicious_snippets', []):
            context['snippets'].append({
                'file': snippet.get('file', ''),
                'line_number': snippet.get('line_number', ''),
                'type': snippet.get('type', ''),
                'malicious_code': snippet.get('malicious_code', ''),
                'behavior_summary': snippet.get('behavior_summary', ''),
                'evasion_techniques': snippet.get('evasion_techniques', ''),
                'behavior_formal': snippet.get('behavior_formal', []),
                'evasion_formal': snippet.get('evasion_formal', [])
            })
        
        return context
    except Exception as e:
        print(f"Error reading snippet file {snippet_file}: {e}")
        return None

def get_tool_results(tool_files):
    """Extract results from tool detection files"""
    results = {}
    
    for tool, file_path in tool_files.items():
        if tool == 'snippet':
            continue
            
        try:
            if file_path.suffix == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    results[tool] = f.read().strip()
            elif file_path.suffix == '.csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    results[tool] = f.read().strip()
        except Exception as e:
            print(f"Error reading {tool} result file {file_path}: {e}")
            results[tool] = f"Error reading file: {e}"
    
    return results

def infer_tool_detection(tool_name, result_text, sap_result=None):
    """Infer whether a tool detected malicious behavior from its result text.

    Heuristic-based because tool output formats vary.
    Returns tuple (detected_bool, reason_string).
    """
    try:
        name_lower = tool_name.lower()
        if sap_result is not None and name_lower == 'sap':
            t = (sap_result.get('type') or '').lower()
            if 'malicious' in t or '恶意' in t:
                return True, 'SAP 分类结果标记为恶意'
            # If any classifier columns look like probabilities/labels
            clf_vals = [sap_result.get('DT', ''), sap_result.get('RF', ''), sap_result.get('XGB', '')]
            clf_text = ' '.join([str(v) for v in clf_vals]).lower()
            if any(k in clf_text for k in ['malicious', '恶意', '1.0', 'true', 'yes']):
                return True, 'SAP 分类器输出指示为恶意'
            return False, 'SAP 未标记为恶意'

        text = (result_text or '')
        text_lower = text.lower()
        positive_keywords = [
            'malicious', 'suspicious', 'malware', 'backdoor', 'credential', 'exfiltration', 'exfiltrate',
            'ddos', 'rce', 'remote code', 'exec', 'shell', 'obfuscation', 'anti-debug', 'persistence',
            'c2', 'command and control', 'keylog', 'steal', 'stealer', 'token', 'webhook'
        ]
        negative_keywords = ['no issues found', 'no suspicious', 'not detected', 'clean', 'no risk']

        if any(k in text_lower for k in positive_keywords):
            return True, '包含恶意/可疑关键字'
        if any(k in text_lower for k in negative_keywords):
            return False, '包含未检测/干净的指示'

        # Tool-specific mild hints
        if 'guarddog' in name_lower and ('indicator' in text_lower or 'finding' in text_lower):
            return True, 'GuardDog 指示存在发现'
        if 'ossgadget' in name_lower and 'confidence' in text_lower:
            return True, 'OSS Gadget 输出包含风险评分'
        if 'socket' in name_lower and ('alert' in text_lower or 'risk' in text_lower):
            return True, 'Socket 报告包含风险/告警'
        if 'genie' in name_lower and ('detect' in text_lower or 'threat' in text_lower):
            return True, 'Genie 输出包含检测/威胁字样'
        if 'packj' in name_lower and ('flag' in text_lower or 'suspicious' in text_lower):
            return True, 'Packj 输出包含可疑标记'

        # Fallback: treat non-empty as not enough evidence
        return False, '未找到明确恶意迹象'
    except Exception:
        return False, '解析失败'

def main():
    # Define base directories
    base_dirs = {
        'classifications': Path('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/behavior_annoation/key_results/package_all_classifications.csv'),
        'snippets': Path('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/code_snipptes/malware_snippets'),
        'tools': Path('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output'),
        'sap': Path('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Tools/sap/scripts/sap_detection_results.csv')
    }
    
    # Read classifications
    classifications_data = []
    try:
        with open(base_dirs['classifications'], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                classifications_data.append(row)
    except Exception as e:
        print(f"Error reading classifications file: {e}")
        return
    
    # Get all unique classifications
    all_classifications = set()
    for row in classifications_data:
        classifications_str = row['classifications']
        # Parse the string representation of list
        classifications = eval(classifications_str)
        all_classifications.update(classifications)
    
    print(f"Found {len(all_classifications)} unique classifications:")
    for cls in sorted(all_classifications):
        print(f"  - {cls}")
    
    # Group packages by classification
    classification_packages = defaultdict(list)
    for row in classifications_data:
        package_name = row['package_name']
        version = row['version']
        classifications_str = row['classifications']
        classifications = eval(classifications_str)
        
        for cls in classifications:
            classification_packages[cls].append((package_name, version))
    
    # Extract examples for each classification
    examples = {}
    used_packages = set()
    
    for classification in sorted(all_classifications):
        print(f"\nProcessing classification: {classification}")
        
        # Find a package that hasn't been used yet
        selected_package = None
        for package_name, version in classification_packages[classification]:
            package_key = f"{package_name}##{version}"
            if package_key not in used_packages:
                selected_package = (package_name, version)
                used_packages.add(package_key)
                break
        
        if not selected_package:
            print(f"  No unused package found for {classification}")
            continue
        
        package_name, version = selected_package
        print(f"  Selected package: {package_name} {version}")
        
        # Find relevant files
        files = find_package_files(package_name, version, base_dirs)
        
        # Extract malicious context
        malicious_context = None
        if 'snippet' in files:
            malicious_context = extract_malicious_context(files['snippet'])
        
        # Get tool results
        tool_results = get_tool_results(files)
        
        # Get SAP results
        sap_result = get_sap_result(package_name, version, base_dirs['sap'])
        
        # Compile example
        example = {
            'classification': classification,
            'package_name': package_name,
            'version': version,
            'malicious_context': malicious_context,
            'tool_results': tool_results,
            'sap_result': sap_result
        }
        
        examples[classification] = example
        print(f"  Successfully extracted example for {classification}")
    
    # Generate final document
    output_file = Path('/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/rebuttal/classification_examples.md')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# NPM 恶意行为分类示例\n\n")
        f.write("本文件为 15 类恶意行为各选取 1 个真实恶意包代码片段的说明，包含：代码上下文、行为与规避技术说明、以及多工具检测对比（未检出的工具将被加粗标注）。\n\n")
        
        for classification in sorted(examples.keys()):
            example = examples[classification]
            f.write(f"## 行为类别：{classification}\n\n")
            f.write(f"**包名：** `{example['package_name']}`  \n")
            f.write(f"**版本：** `{example['version']}`\n\n")
            
            # Malicious code context
            if example['malicious_context']:
                f.write("### 代码上下文\n\n")
                for i, snippet in enumerate(example['malicious_context']['snippets'], 1):
                    f.write(f"#### 片段 {i}\n\n")
                    f.write(f"**文件：** `{snippet['file']}`  \n")
                    f.write(f"**行号：** `{snippet['line_number']}`  \n")
                    f.write(f"**标注类型：** `{snippet['type']}`\n\n")
                    f.write(f"**行为说明：** {snippet['behavior_summary']}\n\n")
                    f.write(f"**规避技术：** {snippet['evasion_techniques']}\n\n")
                    f.write("**恶意代码：**\n```javascript\n")
                    f.write(snippet['malicious_code'])
                    f.write("\n```\n\n")
                    f.write(f"**形式化行为：** {', '.join(snippet['behavior_formal'])}\n\n")
                    f.write(f"**形式化规避：** {', '.join(snippet['evasion_formal'])}\n\n")

                    # Per-snippet detection summary from available tool results
                    f.write("**工具检测对比：**\n\n")
                    # Build a consistent ordered list of tools to report
                    ordered_tools = [
                        ('guarddog', 'GuardDog'),
                        ('genie', 'Genie'),
                        ('ossgadget', 'OSSGadget'),
                        ('socketai', 'SocketAI'),
                        ('packj_static', 'Packj Static'),
                        ('packj_trace', 'Packj Trace'),
                    ]
                    for key, label in ordered_tools:
                        result_text = example['tool_results'].get(key)
                        detected, reason = infer_tool_detection(key, result_text)
                        if detected:
                            f.write(f"- {label}：检测到（{reason}）\n")
                        else:
                            f.write(f"- **{label}：未检测到**（{reason}）\n")
                    # SAP as a separate ML detection
                    detected, reason = infer_tool_detection('sap', '', sap_result=example['sap_result'] or {})
                    if detected:
                        f.write(f"- SAP：检测到（{reason}）\n\n")
                    else:
                        f.write(f"- **SAP：未检测到**（{reason}）\n\n")
            else:
                f.write("### 代码上下文\n\n*暂无片段数据*\n\n")
            
            # Detection tool results
            f.write("### 原始工具输出（截断展示）\n\n")
            
            # SAP results
            if example['sap_result']:
                f.write("#### SAP\n\n")
                f.write(f"- **Type：** {example['sap_result']['type']}\n")
                f.write(f"- **DT：** {example['sap_result']['DT']}\n")
                f.write(f"- **RF：** {example['sap_result']['RF']}\n")
                f.write(f"- **XGB：** {example['sap_result']['XGB']}\n\n")
            else:
                f.write("#### SAP\n\n*未找到 SAP 结果*\n\n")
            
            # Other tool results
            for tool, result in example['tool_results'].items():
                f.write(f"#### {tool.upper()}\n\n")
                if result:
                    f.write("```\n")
                    f.write(str(result)[:1000])  # Limit output length
                    if len(str(result)) > 1000:
                        f.write("\n... (truncated)")
                    f.write("\n```\n\n")
                else:
                    f.write("*无可用结果*\n\n")
            
            f.write("---\n\n")
    
    print(f"\nGenerated examples document: {output_file}")
    print(f"Total examples extracted: {len(examples)}")

if __name__ == "__main__":
    main()
