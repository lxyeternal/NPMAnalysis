#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from collections import defaultdict

# 定义路径
MALWARE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/code_snipptes/malware_snippets"
OUTPUT_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/code_snipptes"

def analyze_malicious_install_scripts():
    """分析恶意软件包中的安装脚本"""
    
    # 统计结果
    preinstall_packages = []
    postinstall_packages = []
    install_packages = []
    combined_packages = []  # 同时包含多种安装脚本的包
    
    # 正则表达式，用于精确匹配各类安装脚本
    preinstall_pattern = re.compile(r'["\']preinstall["\']:\s*["\']')
    postinstall_pattern = re.compile(r'["\']postinstall["\']:\s*["\']')
    install_pattern = re.compile(r'["\']install["\']:\s*["\']')
    
    # 遍历所有目录
    for root, dirs, files in os.walk(MALWARE_DIR):
        for file in files:
            if file == "result.json":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 获取包名和版本
                    package_name = data.get("metadata", {}).get("package_name", "unknown")
                    version = data.get("metadata", {}).get("version", "unknown")
                    package_info = f"{package_name}@{version} - {file_path}"
                    
                    # 检查是否有package/package.json文件
                    # 使用集合存储所有malicious_code，避免重复分析
                    package_json_codes = set()
                    
                    for snippet in data.get("malicious_snippets", []):
                        if snippet.get("file") == "package/package.json":
                            # 将恶意代码添加到集合中，避免重复
                            malicious_code = snippet.get("malicious_code", "")
                            package_json_codes.add(malicious_code)
                    
                    # 只分析每个不同的package.json一次
                    has_preinstall = False
                    has_postinstall = False
                    has_install = False
                    
                    for malicious_code in package_json_codes:
                        # 使用正则表达式匹配各类安装脚本
                        if preinstall_pattern.search(malicious_code) or "preinstall" in malicious_code:
                            has_preinstall = True
                        
                        if postinstall_pattern.search(malicious_code) or "postinstall" in malicious_code:
                            has_postinstall = True
                        
                        if install_pattern.search(malicious_code):
                            has_install = True
                    
                    # 统计各类型脚本
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
                    
                    # 如果同时包含多种安装脚本，记录到组合类别
                    if len(script_types) > 1:
                        combined_packages.append(f"{package_info} - 包含脚本类型: {', '.join(script_types)}")
                
                except Exception as e:
                    pass  # 忽略错误
    
    # 生成输出文件
    output_file = os.path.join(OUTPUT_DIR, "malicious_install_scripts_analysis.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("恶意软件包安装脚本分析结果\n")
        f.write("==========================\n\n")
        
        f.write(f"1. preinstall 脚本 (总计: {len(preinstall_packages)}个)\n")
        f.write("-" * 80 + "\n")
        for pkg in preinstall_packages:
            f.write(f"  - {pkg}\n")
        f.write("\n\n")
        
        f.write(f"2. postinstall 脚本 (总计: {len(postinstall_packages)}个)\n")
        f.write("-" * 80 + "\n")
        for pkg in postinstall_packages:
            f.write(f"  - {pkg}\n")
        f.write("\n\n")
        
        f.write(f"3. install 脚本 (总计: {len(install_packages)}个)\n")
        f.write("-" * 80 + "\n")
        for pkg in install_packages:
            f.write(f"  - {pkg}\n")
        f.write("\n\n")
        
        f.write(f"4. 同时包含多种安装脚本的包 (总计: {len(combined_packages)}个)\n")
        f.write("-" * 80 + "\n")
        for pkg in combined_packages:
            f.write(f"  - {pkg}\n")

if __name__ == "__main__":
    analyze_malicious_install_scripts() 