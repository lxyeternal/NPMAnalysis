#!/usr/bin/env python3
import os
import glob
import re
from collections import defaultdict

def extract_detection_types(file_path):
    """
    从guarddog检测文件中提取检测类型（如obfuscation, code-execution, shady-links等）
    """
    types = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # 检查是否为漏报（恶意被检测为零指标）
            if "Found 0 potentially malicious indicators" in content or content.strip() == "benign":
                return "missed", []
                
            # 提取发现的指标数量
            indicator_count_match = re.search(r'Found (\d+) potentially malicious indicators', content)
            indicator_count = int(indicator_count_match.group(1)) if indicator_count_match else 0
            
            # 查找所有检测类型
            # 典型格式为： "obfuscation: found 1 source code matches"
            matches = re.findall(r'(\w+(?:-\w+)*): found \d+ source code matches', content)
            types.extend(matches)
            
            # 有些情况可能有其他格式，尝试另一种模式
            other_matches = re.findall(r'(\w+(?:-\w+)*): found \d+ matches', content)
            types.extend(other_matches)
            
            if indicator_count > 0 and not types:
                return "detected_but_unknown_type", []
                
            return "detected", types
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return "error", []

def extract_package_info(file_path):
    """
    从文件路径中提取包名和版本信息
    预期格式: .../malware/包名/版本/文件.txt
    使用os.path逐层查找
    """
    # 获取文件所在目录
    dir_path = os.path.dirname(file_path)
    
    # 获取文件所在目录的父目录（版本目录）
    version_dir = os.path.dirname(dir_path)
    if not os.path.exists(version_dir):
        return os.path.basename(file_path).replace(".txt", ""), "unknown"
    
    version = os.path.basename(version_dir)
    
    # 获取包名目录（版本目录的父目录）
    package_dir = os.path.dirname(version_dir)
    if not os.path.exists(package_dir):
        return os.path.basename(file_path).replace(".txt", ""), version
    
    package_name = os.path.basename(package_dir)
    
    return package_name, version

def main():
    """主函数，分析guarddog恶意软件检测结果"""
    # 输出文件路径
    output_file = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/false_negative/guarddog_malware_analysis.txt"
    
    # guarddog恶意样本文件夹路径
    malware_folder = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/guarddog/malware"
    
    # 用于存储检测文件及其检测类型
    all_files = []
    missed_detections = []  # 漏报的文件
    single_behavior_files = []  # 只匹配一种行为的文件
    
    # 用于统计各种检测类型的计数
    type_counts = defaultdict(int)
    
    # 按类型分类的文件列表
    files_by_type = defaultdict(list)
    
    # 按包名和版本统计
    package_version_stats = defaultdict(lambda: defaultdict(lambda: {"detected": 0, "missed": 0, "behaviors": set()}))
    
    total_malware = 0
    detected_count = 0
    missed_count = 0
    error_count = 0
    
    # 递归查找所有txt文件
    for file_path in glob.glob(os.path.join(malware_folder, "**", "*.txt"), recursive=True):
        total_malware += 1
        status, types = extract_detection_types(file_path)
        
        package_name, version = extract_package_info(file_path)
        package_info = f"{package_name}@{version}"
        
        # 更新包名和版本统计
        if status == "detected":
            package_version_stats[package_name][version]["detected"] += 1
            for detection_type in types:
                package_version_stats[package_name][version]["behaviors"].add(detection_type)
        elif status == "missed":
            package_version_stats[package_name][version]["missed"] += 1
        
        if status == "error":
            error_count += 1
            continue
            
        if status == "missed":
            missed_count += 1
            missed_detections.append((file_path, package_info))
            all_files.append((file_path, [], "missed", package_info))
            continue
            
        detected_count += 1
        all_files.append((file_path, types, "detected", package_info))
        
        # 更新类型计数
        for detection_type in types:
            type_counts[detection_type] += 1
            files_by_type[detection_type].append((file_path, package_info))
            
        # 检查是否只有一种行为
        if len(types) == 1:
            single_behavior_files.append((file_path, types[0], package_info))
    
    # 将分析结果写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Guarddog恶意软件检测分析\n")
        f.write(f"总共分析 {total_malware} 个恶意样本\n")
        f.write(f"成功检测: {detected_count} 个样本 ({detected_count/total_malware*100:.2f}%)\n")
        f.write(f"漏报: {missed_count} 个样本 ({missed_count/total_malware*100:.2f}%)\n")
        if error_count > 0:
            f.write(f"分析错误: {error_count} 个样本 ({error_count/total_malware*100:.2f}%)\n")
        f.write("\n")
        
        # 写入单一行为文件统计
        f.write(f"只匹配一种行为的文件: {len(single_behavior_files)} 个 ({len(single_behavior_files)/detected_count*100:.2f}% 的检测样本)\n\n")
        
        # 写入行为类型统计
        f.write("检测行为类型分布统计：\n")
        f.write("=" * 30 + "\n")
        for detection_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{detection_type}: {count} 个文件 ({count/detected_count*100:.2f}% 的检测样本)\n")
        
        # 按包名和版本统计
        f.write("\n\n按包名和版本统计：\n")
        f.write("=" * 30 + "\n")
        for package_name, versions in sorted(package_version_stats.items()):
            total_pkg_files = sum(v["detected"] + v["missed"] for v in versions.values())
            detected_pkg_files = sum(v["detected"] for v in versions.values())
            f.write(f"\n## 包名: {package_name} (总共 {total_pkg_files} 个样本, 检测率: {detected_pkg_files/total_pkg_files*100:.2f}%)\n")
            
            for version, stats in sorted(versions.items()):
                total_ver = stats["detected"] + stats["missed"]
                if total_ver > 0:
                    detection_rate = stats["detected"] / total_ver * 100
                    f.write(f"  - 版本 {version}: 总共 {total_ver} 个样本, 检测 {stats['detected']} 个, 漏报 {stats['missed']} 个, 检测率: {detection_rate:.2f}%\n")
                    if stats["behaviors"]:
                        f.write(f"    检测到的行为: {', '.join(sorted(stats['behaviors']))}\n")
        
        # 分类型列出文件
        f.write("\n\n详细行为分类列表：\n")
        f.write("=" * 30 + "\n")
        for detection_type, files in sorted(files_by_type.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"\n## {detection_type} ({len(files)} 个文件):\n")
            for i, (file_path, package_info) in enumerate(sorted(files, key=lambda x: x[1]), 1):
                f.write(f"{i}. {package_info} - {file_path}\n")
        
        # 单一行为文件列表
        f.write("\n\n只匹配一种行为的文件列表：\n")
        f.write("=" * 30 + "\n")
        behavior_group = defaultdict(list)
        for file_path, behavior, package_info in single_behavior_files:
            behavior_group[behavior].append((package_info, file_path))
            
        for behavior, packages in sorted(behavior_group.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"\n## {behavior} ({len(packages)} 个文件):\n")
            for i, (package_info, file_path) in enumerate(sorted(packages), 1):
                f.write(f"{i}. {package_info} - {file_path}\n")
        
        # 漏报文件列表
        f.write("\n\n漏报文件列表 (未检测到恶意行为)：\n")
        f.write("=" * 30 + "\n")
        for i, (file_path, package_info) in enumerate(sorted(missed_detections, key=lambda x: x[1]), 1):
            f.write(f"{i}. {package_info} - {file_path}\n")

    print(f"分析完成! 共分析 {total_malware} 个恶意样本")
    print(f"成功检测: {detected_count} 个样本 ({detected_count/total_malware*100:.2f}%)")
    print(f"漏报: {missed_count} 个样本 ({missed_count/total_malware*100:.2f}%)")
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main() 