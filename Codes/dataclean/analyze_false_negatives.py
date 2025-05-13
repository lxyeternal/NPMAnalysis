#!/usr/bin/env python3
import os
import glob
import re
import json
import subprocess
import shutil
from collections import defaultdict
import time
import sys
import multiprocessing
from functools import partial

# 添加utils目录到Python路径以导入LLMAgent
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils"))
from llmquery import LLMAgent

# 路径配置
GUARDDOG_MALWARE_PATH = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/guarddog/malware"
UNZIP_MALWARE_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
OUTPUT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/package_label"
PROMPTS_PATH = "/home2/wenbo/Documents/NPMAnalysis/Prompts"

# 创建输出目录
os.makedirs(OUTPUT_PATH, exist_ok=True)

# 进程数量
NUM_PROCESSES = 24

def is_false_negative(file_path):
    """
    判断guarddog检测结果是否为漏报（未检测到恶意行为）
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # 检查是否为漏报（恶意被检测为零指标）
            if "Found 0 potentially malicious indicators" in content or content.strip() == "benign":
                return True
        return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

def get_source_files(package_path):
    """
    获取包中的package.json和所有js文件
    返回文件内容和绝对路径
    """
    result = {}
    file_paths = {}
    
    # 查找package.json文件
    package_json_path = None
    for path in glob.glob(os.path.join(package_path, "**/package.json"), recursive=True):
        # 优先使用根目录下的package.json
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
    
    # 查找所有js文件
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

def load_prompt_template(prompt_file):
    """
    从文件中加载prompt模板
    """
    prompt_path = os.path.join(PROMPTS_PATH, prompt_file)
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Failed to load prompt template {prompt_path}: {e}")
        return None

# 加载prompt模板
PACKAGE_JSON_PROMPT_TEMPLATE = load_prompt_template("package_json_analysis_prompt.txt")
JS_CODE_PROMPT_TEMPLATE = load_prompt_template("js_code_analysis_prompt.txt")

def get_npm_prompt(file_content, is_package_json=False):
    """
    构建分析npm包的prompt
    """
    if is_package_json:
        return PACKAGE_JSON_PROMPT_TEMPLATE.replace("{CODE}", file_content)
    else:
        return JS_CODE_PROMPT_TEMPLATE.replace("{CODE}", file_content)

def query_llm(llm_agent, prompt):
    """
    使用指定的LLM代理分析代码
    假设LLM输出的就是JSON格式
    """
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
        
        # 简化的JSON解析
        try:
            analysis = json.loads(content)
            return analysis.get("is_malicious", False), analysis.get("malicious_code", "")
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Original response: {content}")
            return False, ""
    except Exception as e:
        error_str = str(e)
        # 检测是否为上下文长度超出错误
        if "context_length_exceeded" in error_str or "maximum context length" in error_str:
            print(f"File too large, exceeding model context length limit, automatically classified as malicious: {error_str}")
            # 返回为恶意代码，并添加说明
            return True, "File too large, exceeding model context length limit, automatically classified as potentially malicious. This typically indicates highly obfuscated code or code containing suspicious content."
        
        print(f"Error querying LLM: {e}")
        return False, ""

def analyze_file_with_two_llms(file_content, is_package_json=False):
    """
    使用两个LLM分析文件内容是否为恶意代码
    只有当两个LLM都认为是恶意代码时，才返回True
    
    注意：每个进程需要自己的LLM代理实例
    """
    # 在每个进程中创建新的LLM代理实例
    llm_agent1 = LLMAgent()
    llm_agent2 = LLMAgent()
    
    # 检查文件大小，如果超过1MB，直接判定为恶意
    if len(file_content) > 1024 * 1024:
        print(f"  File size exceeds 1MB ({len(file_content)/1024/1024:.2f}MB), automatically classified as malicious")
        return True, "File too large (over 1MB), which typically indicates highly obfuscated code or code containing suspicious content, automatically classified as potentially malicious."
    
    prompt = get_npm_prompt(file_content, is_package_json)
    
    # 使用第一个LLM代理
    is_malicious1, code1 = query_llm(llm_agent1, prompt)
    print(f"  LLM1 analysis result: {'Malicious' if is_malicious1 else 'Not malicious'}")
    
    # 如果第一个LLM因为上下文长度问题判定为恶意，直接返回结果
    if is_malicious1 and "exceeding model context length limit" in code1:
        return True, code1
    
    # 稍微等待一下，避免频繁请求
    time.sleep(2)
    
    # 使用第二个LLM代理
    is_malicious2, code2 = query_llm(llm_agent2, prompt)
    print(f"  LLM2 analysis result: {'Malicious' if is_malicious2 else 'Not malicious'}")
    
    # 如果第二个LLM因为上下文长度问题判定为恶意，直接返回结果
    if is_malicious2 and "exceeding model context length limit" in code2:
        return True, code2
    
    # 只有两个LLM都认为是恶意的，才返回True
    if is_malicious1 and is_malicious2:
        # 优先使用更详细的恶意代码描述
        if len(code1) > len(code2):
            return True, code1
        else:
            return True, code2
    else:
        return False, ""

def analyze_package(package_info):
    """
    分析可能是漏报的恶意包
    
    Args:
        package_info: 元组，包含(package_name, version, guarddog_file_path, index, total)
    """
    package_name, version, guarddog_file_path, index, total = package_info
    
    print(f"\n[{index}/{total}] Starting analysis: {package_name}@{version}")
    
    # 构建解压后的恶意包路径
    unzip_package_path = os.path.join(UNZIP_MALWARE_PATH, package_name, version)
    if not os.path.exists(unzip_package_path):
        print(f"Unzipped package path does not exist: {unzip_package_path}")
        return None
    
    # 获取源文件内容和路径
    try:
        source_files, file_paths = get_source_files(unzip_package_path)
    except Exception as e:
        print(f"Error getting source files: {e}")
        return None
    
    if not source_files.get('package.json') and not source_files.get('js_files'):
        print(f"No files found to analyze: {package_name}@{version}")
        return None
    
    # 存储分析结果
    analysis_results = {
        "package_name": package_name,
        "version": version,
        "guarddog_path": os.path.abspath(guarddog_file_path),
        "malicious_files": [],
        "malicious_code": {}
    }
    
    # 分析package.json
    if source_files.get('package.json'):
        package_json_path = file_paths['package.json']
        print(f"Analyzing package.json: {package_json_path}")
        is_malicious, malicious_code = analyze_file_with_two_llms(source_files['package.json'], is_package_json=True)
        
        if is_malicious:
            analysis_results["malicious_files"].append(package_json_path)
            analysis_results["malicious_code"][package_json_path] = malicious_code
    
    # 分析JS文件
    js_files_list = list(source_files.get('js_files', {}).items())
    print(f"Found {len(js_files_list)} JS files")
    
    for i, (js_file, content) in enumerate(js_files_list):
        if len(content) < 100:  # 忽略非常小的文件
            continue
        
        # 获取完整的JS文件路径
        js_file_path = file_paths['js_files'][js_file]
        file_size_mb = len(content) / 1024 / 1024
        print(f"Analyzing JS file [{i+1}/{len(js_files_list)}]: {js_file_path} (Size: {file_size_mb:.2f}MB)")
        
        is_malicious, malicious_code = analyze_file_with_two_llms(content)
        
        if is_malicious:
            analysis_results["malicious_files"].append(js_file_path)
            analysis_results["malicious_code"][js_file_path] = malicious_code
    
    # 创建输出目录
    output_package_dir = os.path.join(OUTPUT_PATH, package_name)
    output_version_dir = os.path.join(output_package_dir, version)
    os.makedirs(output_version_dir, exist_ok=True)
    
    # 写入分析结果
    output_file = os.path.join(output_version_dir, f"{package_name}-{version}-analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    
    # 输出分析结果文件的完整路径
    output_file_abs = os.path.abspath(output_file)
    print(f"[{index}/{total}] Analysis completed: {package_name}@{version}")
    print(f"Results saved to: {output_file_abs}")
    
    if analysis_results["malicious_files"]:
        print(f"Found {len(analysis_results['malicious_files'])} malicious files")
    else:
        print("No malicious code found")
    return analysis_results

def main():
    """主函数"""
    print("Starting analysis of guarddog false negatives...")
    
    # 查找所有guarddog检测结果
    false_negatives = []
    total_malware = 0
    
    for file_path in glob.glob(os.path.join(GUARDDOG_MALWARE_PATH, "**", "*.txt"), recursive=True):
        total_malware += 1
        
        if is_false_negative(file_path):
            # 从路径中提取包名和版本
            rel_path = os.path.relpath(file_path, GUARDDOG_MALWARE_PATH)
            parts = rel_path.split(os.sep)
            
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]
                false_negatives.append((package_name, version, file_path))
    
    print(f"Total malware samples analyzed: {total_malware}")
    print(f"Found {len(false_negatives)} false negative samples")
    
    # 创建总结文件
    summary_file = os.path.join(OUTPUT_PATH, "analysis_summary.json")
    summary_file_abs = os.path.abspath(summary_file)
    print(f"Summary file will be saved to: {summary_file_abs}")
    
    # 准备多进程所需的参数列表
    package_infos = []
    for i, (package_name, version, file_path) in enumerate(false_negatives, 1):
        package_infos.append((package_name, version, file_path, i, len(false_negatives)))
    
    # 使用多进程池进行分析
    results = []
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        # 使用进程池并行处理
        for result in pool.imap_unordered(analyze_package, package_infos):
            if result:
                results.append(result)
                # 保存当前进度的汇总结果
                save_summary(results, total_malware, len(false_negatives), summary_file)
    
    # 最终保存汇总结果
    save_summary(results, total_malware, len(false_negatives), summary_file)
    
    print(f"\nAnalysis completed! Analyzed {len(false_negatives)} false negative samples")
    print(f"Found {len([r for r in results if r['malicious_files']])} packages containing malicious code")
    print(f"All results have been saved to: {os.path.abspath(OUTPUT_PATH)}")
    print(f"Summary information saved to: {summary_file_abs}")

def save_summary(results, total_malware, false_negatives_count, summary_file):
    """保存汇总结果"""
    malicious_packages = []
    packages_with_detected_malicious_code = 0
    
    for result in results:
        if result["malicious_files"]:
            packages_with_detected_malicious_code += 1
            # 包含包名、版本及完整的恶意文件路径
            malicious_packages.append({
                "package_name": result["package_name"],
                "version": result["version"],
                "malicious_files": result["malicious_files"],  # 这已经是完整路径
                "result_file": os.path.abspath(os.path.join(
                    OUTPUT_PATH, 
                    result["package_name"], 
                    result["version"], 
                    f"{result['package_name']}-{result['version']}-analysis.json"
                ))
            })
    
    summary_results = {
        "total_malware": total_malware,
        "false_negatives_count": false_negatives_count,
        "packages_with_detected_malicious_code": packages_with_detected_malicious_code,
        "packages_with_no_detected_malicious_code": len(results) - packages_with_detected_malicious_code,
        "progress": f"{len(results)}/{false_negatives_count}",
        "output_directory": os.path.abspath(OUTPUT_PATH),
        "malicious_packages": malicious_packages
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 设置多进程启动方法
    if sys.platform == 'darwin':  # macOS
        multiprocessing.set_start_method('spawn')
    main() 