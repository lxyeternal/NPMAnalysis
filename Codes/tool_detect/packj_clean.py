#!/usr/bin/env python3
import os
import glob
import shutil
import re
from pathlib import Path
from collections import Counter

# 指定目录路径
base_dir = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace/malware"

def find_files_with_code_pattern():
    """查找所有包含[code X]格式字符串的文件，并统计各种code值的出现次数"""
    total_files = 0
    files_with_code_pattern = 0
    files_with_code_pattern_list = []
    code_pattern_counter = Counter()
    all_patterns_found = set()
    
    # 使用glob递归查找所有result.txt文件
    result_files = glob.glob(f"{base_dir}/*/*/result.txt", recursive=True)
    
    # 正则表达式匹配[code X]格式
    code_pattern = re.compile(r'\[code\s+([^\]]+)\]')
    
    # 遍历所有文件
    for file_path in result_files:
        total_files += 1
        file_has_pattern = False
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # 查找所有匹配的模式
                matches = code_pattern.findall(content)
                
                if matches:
                    file_has_pattern = True
                    files_with_code_pattern_list.append(file_path)
                    
                    # 统计每种code值的出现次数
                    for match in matches:
                        code_value = match.strip()
                        code_pattern_counter[code_value] += 1
                        all_patterns_found.add(f"[code {code_value}]")
                
                # 检查是否包含"list index out of range"
                if "list index out of range" in content:
                    if not file_has_pattern:
                        file_has_pattern = True
                        files_with_code_pattern_list.append(file_path)
                    code_pattern_counter["list index out of range"] += 1
                    all_patterns_found.add("[list index out of range]")
                
                # 检查是否包含"KeyboardInterrupt"
                if "KeyboardInterrupt" in content:
                    if not file_has_pattern:
                        file_has_pattern = True
                        files_with_code_pattern_list.append(file_path)
                    code_pattern_counter["KeyboardInterrupt"] += 1
                    all_patterns_found.add("[KeyboardInterrupt]")
        
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
        
        if file_has_pattern:
            files_with_code_pattern += 1
    
    # 输出结果
    print(f"总共检查的文件数量: {total_files}")
    print(f"包含[code X]格式或特定错误字符串的文件数量: {files_with_code_pattern}")
    print(f"包含这些字符串的文件比例: {files_with_code_pattern/total_files:.2%}")
    
    # 输出各种code值的统计信息
    print("\n各种code值及其出现次数:")
    for code_value, count in sorted(code_pattern_counter.items(), key=lambda x: x[1], reverse=True):
        print(f"- [code {code_value}]: {count}次")
    
    # 输出所有发现的模式
    print("\n所有发现的模式:")
    for pattern in sorted(all_patterns_found):
        print(f"- {pattern}")
    
    # 输出包含这些模式的文件列表
    # print("\n包含这些模式的文件列表:")
    # for file_path in files_with_code_pattern_list:
    #     print(f"- {file_path}")
    
    return files_with_code_pattern_list

def delete_files_and_folders(files_list):
    """删除指定文件列表中的文件所在的版本文件夹，并在必要时删除包名文件夹"""
    removed_version_dirs = []
    removed_package_dirs = []
    
    # 收集需要删除的版本文件夹和包名文件夹
    versions_to_remove = []
    packages_to_check = set()
    
    for file_path in files_list:
        # 获取版本文件夹路径和包名文件夹路径
        version_dir = os.path.dirname(file_path)
        package_dir = os.path.dirname(version_dir)
        
        versions_to_remove.append(version_dir)
        packages_to_check.add(package_dir)
    
    # 第一步：删除版本文件夹
    for version_dir in versions_to_remove:
        if os.path.exists(version_dir):
            shutil.rmtree(version_dir)
            removed_version_dirs.append(version_dir)
            print(f"已删除版本文件夹: {version_dir}")
    
    # 第二步：检查包名文件夹是否为空，如果为空则删除
    for package_dir in packages_to_check:
        if os.path.exists(package_dir):
            remaining_versions = [d for d in os.listdir(package_dir) if os.path.isdir(os.path.join(package_dir, d))]
            if not remaining_versions:
                shutil.rmtree(package_dir)
                removed_package_dirs.append(package_dir)
                print(f"已删除包名文件夹: {package_dir}")
    
    # 输出删除结果
    print(f"\n删除的版本文件夹数量: {len(removed_version_dirs)}")
    print(f"删除的包名文件夹数量: {len(removed_package_dirs)}")
    
    # 输出删除的文件夹列表
    print("\n删除的版本文件夹:")
    for dir_path in removed_version_dirs:
        print(f"- {dir_path}")
    
    print("\n删除的包名文件夹:")
    for dir_path in removed_package_dirs:
        print(f"- {dir_path}")

def main():
    # 查找包含[code X]格式字符串的文件
    print("正在查找包含[code X]格式字符串的文件...\n")
    files_to_remove = find_files_with_code_pattern()
    
    # 询问用户是否要删除
    if files_to_remove:
        user_input = input("\n是否要删除这些文件所在的版本文件夹？(yes/no): ")
        if user_input.lower() == "yes":
            print("\n开始删除文件夹...\n")
            delete_files_and_folders(files_to_remove)
        else:
            print("操作已取消，未删除任何文件。")
    else:
        print("没有找到需要删除的文件。")

if __name__ == "__main__":
    main() 