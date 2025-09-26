#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 packj 结果文件，提取包含 'risk(s) apply to you' 的包的 process、files、network 数据
"""

import os
import re
import glob
from collections import defaultdict
import json
from pathlib import Path

def extract_syscall_data(file_path):
    """
    从 result.txt 文件中提取 process、files、network 数据
    返回: (process_count, files_count, network_count) 或 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 检查是否包含 "risk(s) apply to you"
        if "risk(s) apply to you" not in content:
            return None
        
        # 查找包含 syscalls 数据的行
        # 格式: [1m[32mPASS[0m [[34mfound 161 process,15 files,558 network syscalls[0m]
        # 需要匹配ANSI颜色代码
        pattern = r'found (\d+) process,(\d+) files,(\d+) network syscalls'
        match = re.search(pattern, content)
        
        if match:
            process_count = int(match.group(1))
            files_count = int(match.group(2))
            network_count = int(match.group(3))
            return (process_count, files_count, network_count)
        
        return None
        
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return None

def analyze_directory(base_dir):
    """
    分析指定目录下的所有 result.txt 文件
    """
    print(f"正在分析目录: {base_dir}")
    
    # 找到所有 result.txt 文件
    result_files = glob.glob(os.path.join(base_dir, "**/result.txt"), recursive=True)
    print(f"找到 {len(result_files)} 个 result.txt 文件")
    
    # 存储数据
    valid_packages = []
    process_counts = []
    files_counts = []
    network_counts = []
    
    # 统计信息
    total_files = len(result_files)
    processed_files = 0
    valid_files = 0
    
    for file_path in result_files:
        processed_files += 1
        if processed_files % 100 == 0:
            print(f"已处理 {processed_files}/{total_files} 个文件...")
        
        data = extract_syscall_data(file_path)
        if data:
            valid_files += 1
            process_count, files_count, network_count = data
            
            # 从文件路径提取包名和版本信息
            # 路径格式: .../包名/版本/result.txt
            path_parts = Path(file_path).parts
            if len(path_parts) >= 3:
                package_name = path_parts[-3]
                version = path_parts[-2]
            else:
                package_name = "unknown"
                version = "unknown"
            
            package_info = {
                'package_name': package_name,
                'version': version,
                'file_path': file_path,
                'process_count': process_count,
                'files_count': files_count,
                'network_count': network_count
            }
            
            valid_packages.append(package_info)
            process_counts.append(process_count)
            files_counts.append(files_count)
            network_counts.append(network_count)
    
    print(f"\n处理完成!")
    print(f"总文件数: {total_files}")
    print(f"包含 'risk(s) apply to you' 且有 syscalls 数据的文件数: {valid_files}")
    
    if valid_files > 0:
        # 计算统计数据
        print(f"\n=== 统计结果 ===")
        print(f"有效包版本数量: {valid_files}")
        
        # Process 统计
        process_avg = sum(process_counts) / len(process_counts)
        process_min = min(process_counts)
        process_max = max(process_counts)
        print(f"\nProcess 统计:")
        print(f"  平均值: {process_avg:.2f}")
        print(f"  最小值: {process_min}")
        print(f"  最大值: {process_max}")
        print(f"  总数: {sum(process_counts)}")
        
        # Files 统计
        files_avg = sum(files_counts) / len(files_counts)
        files_min = min(files_counts)
        files_max = max(files_counts)
        print(f"\nFiles 统计:")
        print(f"  平均值: {files_avg:.2f}")
        print(f"  最小值: {files_min}")
        print(f"  最大值: {files_max}")
        print(f"  总数: {sum(files_counts)}")
        
        # Network 统计
        network_avg = sum(network_counts) / len(network_counts)
        network_min = min(network_counts)
        network_max = max(network_counts)
        print(f"\nNetwork 统计:")
        print(f"  平均值: {network_avg:.2f}")
        print(f"  最小值: {network_min}")
        print(f"  最大值: {network_max}")
        print(f"  总数: {sum(network_counts)}")
        
        # 维度覆盖统计
        has_process = sum(1 for p in process_counts if p > 0)
        has_files = sum(1 for f in files_counts if f > 0)
        has_network = sum(1 for n in network_counts if n > 0)
        
        print(f"\n=== 维度覆盖统计 ===")
        print(f"包含 process 数据的包: {has_process}/{valid_files} ({has_process/valid_files*100:.1f}%)")
        print(f"包含 files 数据的包: {has_files}/{valid_files} ({has_files/valid_files*100:.1f}%)")
        print(f"包含 network 数据的包: {has_network}/{valid_files} ({has_network/valid_files*100:.1f}%)")
        
        # 保存详细数据到 JSON 文件
        output_file = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/packj_analysis_results.json"
        analysis_results = {
            'summary': {
                'total_files': total_files,
                'valid_files': valid_files,
                'process_stats': {
                    'average': process_avg,
                    'min': process_min,
                    'max': process_max,
                    'total': sum(process_counts),
                    'packages_with_data': has_process
                },
                'files_stats': {
                    'average': files_avg,
                    'min': files_min,
                    'max': files_max,
                    'total': sum(files_counts),
                    'packages_with_data': has_files
                },
                'network_stats': {
                    'average': network_avg,
                    'min': network_min,
                    'max': network_max,
                    'total': sum(network_counts),
                    'packages_with_data': has_network
                }
            },
            'packages': valid_packages
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n详细结果已保存到: {output_file}")
        
        # 显示前10个包的详细信息
        print(f"\n=== 前10个包的详细信息 ===")
        for i, pkg in enumerate(valid_packages[:10]):
            print(f"{i+1}. {pkg['package_name']} v{pkg['version']}")
            print(f"   Process: {pkg['process_count']}, Files: {pkg['files_count']}, Network: {pkg['network_count']}")
    
    return valid_packages

def main():
    base_directory = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace_new/benign"
    
    if not os.path.exists(base_directory):
        print(f"错误: 目录不存在 {base_directory}")
        return
    
    analyze_directory(base_directory)

if __name__ == "__main__":
    main()
