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
            
            # 检查是否为假阳性（良性被检测为恶意）
            if "Found 0 potentially malicious indicators" in content or content.strip() == "benign":
                return []  # 不是假阳性
                
            # 查找所有检测类型
            # 典型格式为： "obfuscation: found 1 source code matches"
            matches = re.findall(r'(\w+(?:-\w+)*): found \d+ source code matches', content)
            types.extend(matches)
            
            # 有些情况可能有其他格式，尝试另一种模式
            other_matches = re.findall(r'(\w+(?:-\w+)*): found \d+ matches', content)
            types.extend(other_matches)
            
            return types
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def find_txt_files(directory):
    """递归查找目录中的所有txt文件"""
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

def main():
    """主函数，分析guarddog假阳性文件的检测类型"""
    # 输出文件路径
    output_file = "/home/wenbo/NPMAnalysis/Codes/tool_detect/false_positive/guarddog_false_positives_types.txt"
    
    # guarddog良性样本文件夹路径
    benign_folder = "/home/wenbo/NPMAnalysis/Codes/tool_detect/tool_output/guarddog/benign"
    
    # 用于存储假阳性文件及其检测类型
    false_positives = []
    
    # 用于统计各种检测类型的计数
    type_counts = defaultdict(int)
    
    # 按类型分类的文件列表
    files_by_type = defaultdict(list)
    
    # 递归查找所有txt文件
    txt_files = find_txt_files(benign_folder)
    total_benign = len(txt_files)
    
    print(f"开始分析目录: {benign_folder}")
    print(f"找到 {total_benign} 个txt文件")
    
    # 遍历所有找到的txt文件
    for i, file_path in enumerate(txt_files):
        types = extract_detection_types(file_path)
        
        if types:  # 如果提取到了检测类型，则说明是假阳性
            false_positives.append((file_path, types))
            
            # 更新类型计数
            for detection_type in types:
                type_counts[detection_type] += 1
                files_by_type[detection_type].append(file_path)
        
        if (i + 1) % 100 == 0:
            print(f"已处理 {i + 1}/{total_benign} 个文件...")
    
    print(f"\n分析完成! 共处理 {total_benign} 个文件")
    print(f"发现 {len(false_positives)} 个假阳性")
    
    # 将假阳性的统计结果写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Guarddog假阳性文件类型统计 (错误地将良性识别为恶意)\n")
        f.write(f"总共找到 {len(false_positives)} 个假阳性 (占良性样本总数 {total_benign} 的 {len(false_positives)/total_benign*100:.2f}%)\n\n")
        
        # 写入类型统计
        f.write("检测类型统计：\n")
        f.write("=" * 30 + "\n")
        for detection_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{detection_type}: {count} 个文件 ({count/len(false_positives)*100:.2f}%)\n")
        
        # 分类型列出文件
        f.write("\n\n详细分类列表：\n")
        f.write("=" * 30 + "\n")
        for detection_type, files in sorted(files_by_type.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"\n## {detection_type} ({len(files)} 个文件):\n")
            for i, file_path in enumerate(sorted(files), 1):
                package_name = os.path.basename(file_path)
                f.write(f"{i}. {package_name} - {file_path}\n")
        
        # 完整列表
        f.write("\n\n所有假阳性文件及其检测类型：\n")
        f.write("=" * 30 + "\n")
        for i, (file_path, types) in enumerate(sorted(false_positives, key=lambda x: x[0]), 1):
            package_name = os.path.basename(file_path)
            f.write(f"{i}. {package_name}\n")
            f.write(f"   路径: {file_path}\n")
            f.write(f"   检测类型: {', '.join(types)}\n\n")
    
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main() 