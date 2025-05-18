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
OUTPUT_TXT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/output.txt"
UNZIP_MALWARE_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
OUTPUT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/package_label"
PROMPTS_PATH = "/home2/wenbo/Documents/NPMAnalysis/Prompts"

# 创建输出目录
os.makedirs(OUTPUT_PATH, exist_ok=True)

# 进程数量
NUM_PROCESSES = 24

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

def query_llm(llm_agent, prompt, is_package_json=False):
    """
    使用指定的LLM代理分析代码
    假设LLM输出的就是JSON格式
    
    对于package.json，返回(is_malicious, malicious_code, behavior_summary, attack_type)
    对于JS文件，返回(is_malicious, malicious_code, behavior_summary, None)
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
            is_malicious = analysis.get("is_malicious", False)
            malicious_code = analysis.get("malicious_code", "")
            behavior_summary = analysis.get("behavior_summary", "")
            
            # 只有package.json才会有attack_type字段
            attack_type = analysis.get("attack_type", "") if is_package_json else None
            
            return is_malicious, malicious_code, behavior_summary, attack_type
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {e}")
            print(f"Original response: {content}")
            return False, "", "", None if not is_package_json else ""
    except Exception as e:
        error_str = str(e)
        # 检测是否为上下文长度超出错误
        if "context_length_exceeded" in error_str or "maximum context length" in error_str:
            print(f"File too large, exceeding model context length limit, automatically classified as malicious: {error_str}")
            # 返回为恶意代码，并添加说明
            attack_type = "other" if is_package_json else None
            return True, "File too large, exceeding model context length limit, automatically classified as potentially malicious. This typically indicates highly obfuscated code or code containing suspicious content.", "Large obfuscated file, likely malicious", attack_type
        
        print(f"Error querying LLM: {e}")
        return False, "", "", None if not is_package_json else ""

def analyze_file(file_content, is_package_json=False):
    """
    使用LLM分析文件内容，提取恶意代码片段
    不再使用两个LLM确认，因为已知这些是恶意包
    
    注意：每个进程需要自己的LLM代理实例
    """
    # 在每个进程中创建新的LLM代理实例
    llm_agent = LLMAgent()
    
    # 检查文件大小，如果超过1MB，直接判定为恶意
    if len(file_content) > 1024 * 1024:
        print(f"  File size exceeds 1MB ({len(file_content)/1024/1024:.2f}MB), automatically classified as malicious")
        attack_type = "other" if is_package_json else None
        return True, "File too large (over 1MB), which typically indicates highly obfuscated code or code containing suspicious content, automatically classified as potentially malicious.", "Large obfuscated file, likely malicious", attack_type
    
    prompt = get_npm_prompt(file_content, is_package_json)
    
    # 使用LLM代理分析
    is_malicious, code, behavior, attack_type = query_llm(llm_agent, prompt, is_package_json)
    print(f"  LLM analysis result: {'Malicious' if is_malicious else 'Not malicious'}")
    
    return is_malicious, code, behavior, attack_type

def analyze_package(package_info):
    """
    分析恶意包
    
    Args:
        package_info: 元组，包含(package_name, version, index, total)
    """
    package_name, version, index, total = package_info
    
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
        "malicious_files": [],
        "malicious_code": {},
        "behavior_summaries": {},
        "attack_types": {}  # 只存储package.json的attack_type
    }
    
    # 分析package.json
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
        
        is_malicious, malicious_code, behavior_summary, _ = analyze_file(content, is_package_json=False)
        
        if is_malicious:
            analysis_results["malicious_files"].append(js_file_path)
            analysis_results["malicious_code"][js_file_path] = malicious_code
            analysis_results["behavior_summaries"][js_file_path] = behavior_summary
            # JS文件不设置attack_type
            print(f"Malicious code found in {js_file}")
            print(f"Behavior: {behavior_summary}")
    
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
        for file_path in analysis_results["malicious_files"]:
            behavior = analysis_results["behavior_summaries"].get(file_path, "")
            # 只有package.json才有attack_type
            if file_path == file_paths.get('package.json'):
                attack = analysis_results["attack_types"].get(file_path, "")
                print(f"File: {file_path}")
                print(f"Behavior: {behavior}")
                print(f"Attack type: {attack}")
            else:
                print(f"File: {file_path}")
                print(f"Behavior: {behavior}")
    else:
        print("No malicious code found")
    return analysis_results

def parse_output_txt():
    """从output.txt文件中读取包名和版本信息"""
    packages = []
    try:
        with open(OUTPUT_TXT_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 使用/分割，获取包名和版本
                parts = line.split('/')
                if len(parts) >= 2:
                    package_name = parts[0]  # 保持原始包名格式
                    version = parts[1]
                    packages.append((package_name, version))
    except Exception as e:
        print(f"Error parsing output.txt: {e}")
    
    return packages

def main():
    """主函数"""
    print("Starting analysis of packages from output.txt...")
    
    # 从output.txt读取包列表
    packages = parse_output_txt()
    
    if not packages:
        print("No packages found in output.txt file")
        return
    
    print(f"Found {len(packages)} packages to analyze")
    
    # 创建总结文件
    summary_file = os.path.join(OUTPUT_PATH, "analysis_summary.json")
    summary_file_abs = os.path.abspath(summary_file)
    print(f"Summary file will be saved to: {summary_file_abs}")
    
    # 准备多进程所需的参数列表
    package_infos = []
    for i, (package_name, version) in enumerate(packages, 1):
        package_infos.append((package_name, version, i, len(packages)))
    
    # 使用多进程池进行分析
    results = []
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        # 使用进程池并行处理
        for result in pool.imap_unordered(analyze_package, package_infos):
            if result:
                results.append(result)
                # 保存当前进度的汇总结果
                save_summary(results, len(packages), summary_file)
    
    # 最终保存汇总结果
    save_summary(results, len(packages), summary_file)
    
    print(f"\nAnalysis completed! Analyzed {len(packages)} packages")
    print(f"Found {len([r for r in results if r['malicious_files']])} packages containing malicious code")
    print(f"All results have been saved to: {os.path.abspath(OUTPUT_PATH)}")
    print(f"Summary information saved to: {summary_file_abs}")

def save_summary(results, total_packages, summary_file):
    """保存汇总结果"""
    malicious_packages = []
    packages_with_detected_malicious_code = 0
    
    for result in results:
        if result["malicious_files"]:
            packages_with_detected_malicious_code += 1
            # 包含包名、版本、恶意文件路径、行为描述和攻击类型
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
            
            # 对于每个恶意文件，添加行为摘要
            # 只对package.json添加attack_type
            if result["malicious_files"] and result["behavior_summaries"]:
                first_file = result["malicious_files"][0]
                package_info["behavior_summary"] = result["behavior_summaries"].get(first_file, "")
                
                # 检查第一个文件是否为package.json
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

if __name__ == "__main__":
    # 设置多进程启动方法
    if sys.platform == 'darwin':  # macOS
        multiprocessing.set_start_method('spawn')
    main() 