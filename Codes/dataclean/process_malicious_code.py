#!/usr/bin/env python3
import os
import json
import hashlib
import shutil
import sys
from pathlib import Path

# 定义路径
SOURCE_DIR = '/home2/mynames/Documents/NPMAnalysis/Codes/dataclean/package_label'
TARGET_DIR = '/home2/mynames/Documents/NPMAnalysis/Codes/code_snipptes/malware_snippets'

def calculate_hash(code_string):
    """计算代码字符串的MD5哈希值"""
    return hashlib.md5(code_string.encode('utf-8')).hexdigest()

def process_package_file(package_path):
    """处理单个包文件，提取恶意代码信息并生成新格式"""
    try:
        with open(package_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 如果没有恶意代码，则跳过
        if not data.get('malicious_code'):
            return None
            
        # 提取包名和版本
        package_name = data.get('package_name')
        version = data.get('version')
        
        if not package_name or not version:
            print(f"Missing package_name or version in {package_path}")
            return None
            
        # 创建结果结构
        result = {
            "metadata": {
                "package_name": package_name,
                "version": version,
                "report_path": "",  # 设置为空
                "match_count": len(data.get('malicious_code', {})),
                "unzip_dir": f"/home2/mynames/Documents/NPMAnalysis/Dataset/unzip_malware/{package_name}/{version}"
            },
            "malicious_snippets": []
        }
        
        # 获取攻击类型
        attack_types = data.get('attack_types', {})
        
        # 处理每个恶意代码片段
        for file_path, code in data.get('malicious_code', {}).items():
            # 获取文件名
            file_name = os.path.basename(file_path)
            
            # 获取行为摘要
            behavior_summary = data.get('behavior_summaries', {}).get(file_path, "Unknown behavior")
            
            # 获取攻击类型作为规避技术
            evasion_techniques = ""
            if file_path in attack_types:
                evasion_techniques = attack_types[file_path]
            
            # 计算代码哈希值
            hash_value = calculate_hash(code)
            
            # 创建代码片段对象
            snippet = {
                "file": f"package/{file_name}",
                "line_number": "",  # 设置为空
                "type": "",  # 设置为空
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
    """处理单个指定的包"""
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
        # 创建目标目录
        target_package_dir = os.path.join(TARGET_DIR, package_name, version)
        os.makedirs(target_package_dir, exist_ok=True)
        
        # 保存结果
        output_path = os.path.join(target_package_dir, 'result.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        # 打印完整路径
        abs_path = os.path.abspath(output_path)
        print(f"{abs_path}")
        return True
    else:
        print(f"No malicious code found in {package_name}@{version}")
        return False

def main():
    """主函数，遍历所有包文件并处理"""
    # 检查是否有命令行参数
    if len(sys.argv) > 2:
        package_name = sys.argv[1]
        version = sys.argv[2]
        print(f"Processing single package: {package_name}@{version}")
        process_single_package(package_name, version)
        return
    
    # 确保目标目录存在
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # 计数器
    processed_count = 0
    error_count = 0
    
    # 遍历源目录
    for root, dirs, files in os.walk(SOURCE_DIR):
        for dir_name in dirs:
            # 构建包目录路径
            package_dir = os.path.join(root, dir_name)
            
            # 跳过非包目录
            if not os.path.isdir(package_dir):
                continue
                
            try:
                # 遍历包目录下的版本目录
                for version_dir in os.listdir(package_dir):
                    version_path = os.path.join(package_dir, version_dir)
                    
                    if not os.path.isdir(version_path):
                        continue
                        
                    # 查找分析文件
                    analysis_files = [f for f in os.listdir(version_path) if f.endswith('-analysis.json')]
                    
                    for analysis_file in analysis_files:
                        file_path = os.path.join(version_path, analysis_file)
                        
                        # 处理文件
                        result = process_package_file(file_path)
                        
                        if result and result["malicious_snippets"]:
                            # 创建目标目录
                            package_name = result["metadata"]["package_name"]
                            version = result["metadata"]["version"]
                            target_package_dir = os.path.join(TARGET_DIR, package_name, version)
                            os.makedirs(target_package_dir, exist_ok=True)
                            
                            # 保存结果
                            output_path = os.path.join(target_package_dir, 'result.json')
                            with open(output_path, 'w', encoding='utf-8') as f:
                                json.dump(result, f, indent=2)
                            
                            # 打印完整路径
                            abs_path = os.path.abspath(output_path)
                            print(f"{abs_path}")
                            
                            processed_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error processing directory {package_dir}: {e}")
    
    print(f"\nProcessing complete. Processed {processed_count} packages with {error_count} errors.")

if __name__ == "__main__":
    main() 