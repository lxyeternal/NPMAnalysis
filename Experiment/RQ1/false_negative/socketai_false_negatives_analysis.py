#!/usr/bin/env python3
import os
import json
import sys

def load_skip_list(file_path):
    """加载需要跳过的包列表"""
    skip_list = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():
                    skip_list.add(line.strip())
    return skip_list

def analyze_socketai(file_path):
    """
    分析socketai的检测结果
    解析package_summary.txt文件中的is_malicious字段
    如果is_malicious为true，则返回malware，否则返回benign
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            data = json.loads(content)
            if data.get("is_malicious", False):
                return "malware"
            else:
                return "benign"
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        # 如果解析失败，默认为benign
        return "benign"

def extract_package_info(file_path):
    """从文件路径中提取包名和版本"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            data = json.loads(content)
            package_name = data.get("package_name", "")
            version = data.get("version", "")
            return package_name, version
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        # 如果解析失败，从路径中提取
        dirname = os.path.dirname(file_path)
        parts = dirname.split(os.sep)
        
        # 尝试从路径中找到包名和版本
        if len(parts) >= 2:
            package_name = parts[-2]
            version = parts[-1]
            return package_name, version
        else:
            return "unknown", "unknown"

def find_false_negatives():
    """查找socketai工具的所有漏报包"""
    base_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/socketai"
    malware_path = os.path.join(base_path, "malware")
    
    # 加载需要跳过的恶意样本列表
    malware_benign_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/malware_benign.txt"
    malware_benign_skip_list = load_skip_list(malware_benign_path)
    
    false_negatives = []
    total_samples = 0
    skipped_samples = 0
    correct_detections = 0
    
    # 统计包和版本数量
    unique_packages = set()
    unique_versions = set()
    
    # 处理恶意样本
    for root, dirs, files in os.walk(malware_path):
        if 'package_summary.txt' in files:
            file_path = os.path.join(root, 'package_summary.txt')
            total_samples += 1
            
            # 从路径中提取包名和版本
            package_name, version = extract_package_info(file_path)
            package_info = f"{package_name}/{version}"
            
            # 记录唯一的包和版本
            unique_packages.add(package_name)
            unique_versions.add(package_info)
            
            # 检查是否需要跳过
            if package_info in malware_benign_skip_list:
                skipped_samples += 1
                continue
            
            # 分析检测结果
            prediction = analyze_socketai(file_path)
            
            # 如果恶意样本被错误地识别为良性，则为漏报
            if prediction == "benign":
                false_negatives.append(file_path)
            else:
                correct_detections += 1
    
    # 计算统计信息
    analyzed_samples = total_samples - skipped_samples
    false_negative_rate = len(false_negatives) / analyzed_samples * 100 if analyzed_samples > 0 else 0
    recall = correct_detections / analyzed_samples * 100 if analyzed_samples > 0 else 0
    
    # 保存漏报包列表到文件
    output_file = os.path.join(os.path.dirname(__file__), "socketai_false_negatives_types.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入统计信息
        f.write("SocketAI工具漏报分析报告（恶意样本被错误地识别为良性）\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"总样本数: {total_samples}\n")
        f.write(f"跳过的样本数: {skipped_samples}\n")
        f.write(f"分析的样本数: {analyzed_samples}\n")
        f.write(f"唯一包数量: {len(unique_packages)}\n")
        f.write(f"唯一版本数量: {len(unique_versions)}\n")
        f.write(f"正确检测数: {correct_detections}\n")
        f.write(f"漏报数: {len(false_negatives)}\n")
        f.write(f"漏报率: {false_negative_rate:.2f}%\n")
        f.write(f"召回率: {recall:.2f}%\n\n")
        
        f.write("以下是所有漏报的文件路径:\n")
        f.write("-" * 60 + "\n\n")
        
        # 写入漏报文件路径
        for file_path in false_negatives:
            f.write(f"{file_path}\n")
    
    print(f"找到 {len(false_negatives)} 个漏报包，已保存到 {output_file}")
    print(f"总样本数: {total_samples}, 跳过: {skipped_samples}, 分析: {analyzed_samples}")
    print(f"漏报率: {false_negative_rate:.2f}%, 召回率: {recall:.2f}%")
    return false_negatives

if __name__ == "__main__":
    find_false_negatives()
