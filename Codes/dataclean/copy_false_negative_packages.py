#!/usr/bin/env python3
import os
import json
import shutil
import sys
import multiprocessing
import glob
from functools import partial
from collections import defaultdict

# 路径配置
GUARDDOG_MALWARE_PATH = "/home2/mynames/Documents/NPMAnalysis/Codes/tool_detect/tool_output/guarddog/malware"
UNZIP_MALWARE_PATH = "/home2/mynames/Documents/NPMAnalysis/Dataset/unzip_malware"
DEST_PATH = "/home2/mynames/Documents/NPMAnalysis/Codes/dataclean/false_negative"

# 进程数量
NUM_PROCESSES = 24

def is_false_negative(file_path):
    """
    判断guarddog检测结果是否为漏报（未检测到恶意行为）
    
    如果GuardDog检测结果中包含"Found 0 potentially malicious indicators"
    或者文件内容为"benign"，则认为是漏报
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

def copy_package(package_info):
    """
    复制一个漏报的恶意包到目标目录
    
    Args:
        package_info: 元组，包含(package_name, version, guarddog_file_path, index, total)
        版本可能为None，表示没有版本信息
    """
    package_name, version, guarddog_file_path, index, total = package_info
    
    if version:
        print(f"[{index}/{total}] Processing: {package_name}@{version}")
        # 构建源路径（解压后的恶意包路径）
        src_package_path = os.path.join(UNZIP_MALWARE_PATH, package_name, version)
        # 构建目标路径
        dest_package_path = os.path.join(DEST_PATH, package_name, version)
    else:
        print(f"[{index}/{total}] Processing: {package_name} (no version)")
        # 构建源路径（解压后的恶意包路径）
        src_package_path = os.path.join(UNZIP_MALWARE_PATH, package_name)
        # 构建目标路径
        dest_package_path = os.path.join(DEST_PATH, package_name)
    
    if not os.path.exists(src_package_path):
        print(f"  Source package path does not exist: {src_package_path}")
        return False
    
    # 如果目标路径已存在，先删除
    if os.path.exists(dest_package_path):
        try:
            shutil.rmtree(dest_package_path)
        except Exception as e:
            print(f"  Error removing existing directory {dest_package_path}: {e}")
            return False
    
    # 创建目标目录
    try:
        os.makedirs(os.path.dirname(dest_package_path), exist_ok=True)
    except Exception as e:
        print(f"  Error creating directory {os.path.dirname(dest_package_path)}: {e}")
        return False
    
    # 复制整个目录
    try:
        shutil.copytree(src_package_path, dest_package_path)
        if version:
            print(f"  Successfully copied {package_name}@{version} to {dest_package_path}")
        else:
            print(f"  Successfully copied {package_name} to {dest_package_path}")
        return True
    except Exception as e:
        print(f"  Error copying package {src_package_path} to {dest_package_path}: {e}")
        return False

def count_existing_false_negatives():
    """
    统计已复制到目标目录的漏报恶意包数量
    """
    if not os.path.exists(DEST_PATH):
        return 0, 0, {}
    
    package_versions = defaultdict(list)
    package_count = 0
    version_count = 0
    
    # 遍历目标目录
    for item in os.listdir(DEST_PATH):
        item_path = os.path.join(DEST_PATH, item)
        if os.path.isdir(item_path):
            package_count += 1
            
            # 检查是否有版本子目录
            sub_items = os.listdir(item_path)
            has_version_dirs = False
            
            for sub_item in sub_items:
                sub_item_path = os.path.join(item_path, sub_item)
                if os.path.isdir(sub_item_path):
                    has_version_dirs = True
                    package_versions[item].append(sub_item)
                    version_count += 1
            
            # 如果没有版本子目录，视为单版本包
            if not has_version_dirs:
                package_versions[item].append("(no version)")
                version_count += 1
    
    return package_count, version_count, package_versions

def main():
    """主函数"""
    # 创建目标目录
    os.makedirs(DEST_PATH, exist_ok=True)
    
    # 先统计已存在的漏报包数量
    existing_packages, existing_versions, package_versions = count_existing_false_negatives()
    print(f"\n======= 已存在的漏报包统计 =======")
    print(f"发现 {existing_packages} 个不同的NPM包，共 {existing_versions} 个版本或实例被GuardDog漏报")
    
    print("\n开始检测GuardDog漏报...")
    
    # 查找所有guarddog检测结果
    false_negatives = []
    total_malware = 0
    packages_with_versions = defaultdict(list)
    
    # 使用glob递归查找所有txt文件
    for file_path in glob.glob(os.path.join(GUARDDOG_MALWARE_PATH, "**", "*.txt"), recursive=True):
        total_malware += 1
        
        if is_false_negative(file_path):
            # 解析路径获取包名和版本信息
            rel_path = os.path.relpath(file_path, GUARDDOG_MALWARE_PATH)
            parts = rel_path.split(os.sep)
            
            if len(parts) >= 3:  # 包名/版本/txt文件
                package_name = parts[0]
                version = parts[1]
                false_negatives.append((package_name, version, file_path))
                packages_with_versions[package_name].append(version)
            elif len(parts) == 2:  # 包名/txt文件
                package_name = parts[0]
                version = None
                false_negatives.append((package_name, version, file_path))
                packages_with_versions[package_name].append("(no version)")
    
    # 统计结果
    unique_packages = len(packages_with_versions)
    total_versions = len(false_negatives)
    
    print(f"总共分析了 {total_malware} 个恶意包样本")
    print(f"发现 {unique_packages} 个不同的NPM包，共 {total_versions} 个版本或实例被GuardDog漏报")
    
    # 列出有多个版本被漏报的包
    multiple_versions = {pkg: vers for pkg, vers in packages_with_versions.items() if len(vers) > 1}
    if multiple_versions:
        print("\n包含多个版本被漏报的包(前10个):")
        for pkg, versions in sorted(multiple_versions.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"  {pkg}: {len(versions)} 个版本")
    
    if not false_negatives:
        print("未找到漏报样本。")
        return
    
    # 准备多进程所需的参数列表
    package_infos = []
    for i, (package_name, version, file_path) in enumerate(false_negatives, 1):
        package_infos.append((package_name, version, file_path, i, len(false_negatives)))
    
    # 使用多进程池进行复制
    success_count = 0
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        # 使用进程池并行处理
        for result in pool.imap_unordered(copy_package, package_infos):
            if result:
                success_count += 1
    
    print(f"\n复制完成! 成功复制了 {success_count} 个漏报样本")
    print(f"所有包已被复制到: {os.path.abspath(DEST_PATH)}")
    
    # 最终统计结果
    print(f"\n======= 最终统计 =======")
    final_packages, final_versions, _ = count_existing_false_negatives()
    print(f"总共有 {final_packages} 个不同的NPM包，共 {final_versions} 个版本或实例被GuardDog漏报")

if __name__ == "__main__":
    main() 