#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import re

# 源数据目录和目标目录
SOURCE_DIR = '/home/wenbo/NPMAnalysis/Dataset/raw_dataset'
TARGET_DIR = '/home/wenbo/NPMAnalysis/Dataset/malware'

# 确保目标目录存在
os.makedirs(TARGET_DIR, exist_ok=True)

# 已复制的包集合，用于去重
copied_packages = set()

# 遍历所有子目录
for dataset_dir in os.listdir(SOURCE_DIR):
    dataset_path = os.path.join(SOURCE_DIR, dataset_dir)
    if not os.path.isdir(dataset_path):
        continue
    
    print(f"处理目录: {dataset_path}")
    
    # 使用os.walk遍历所有目录和文件
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.tgz'):
                source_file = os.path.join(root, file)
                rel_path = os.path.relpath(source_file, dataset_path)
                
                # 解析路径获取包名和版本
                path_parts = rel_path.split(os.sep)
                
                # 处理@开头的包
                if path_parts[0].startswith('@'):
                    # 对于@package/name这种形式，合并为@package##name
                    package_name = path_parts[0] + "##" + path_parts[1]
                    version = path_parts[2]
                    tgz_name = file
                else:
                    package_name = path_parts[0]
                    version = path_parts[1]
                    tgz_name = file
                
                # 创建目标路径
                target_package_dir = os.path.join(TARGET_DIR, package_name)
                target_version_dir = os.path.join(target_package_dir, version)
                target_file = os.path.join(target_version_dir, tgz_name)
                
                # 检查是否已经复制过这个包
                package_version_key = f"{package_name}:{version}"
                if package_version_key in copied_packages:
                    print(f"跳过重复包: {package_version_key}")
                    continue
                
                # 创建目录并复制文件
                os.makedirs(target_version_dir, exist_ok=True)
                shutil.copy2(source_file, target_file)
                
                # 添加到已复制集合
                copied_packages.add(package_version_key)
                print(f"已复制: {source_file} -> {target_file}")

print(f"总共复制了 {len(copied_packages)} 个不重复的包版本到 {TARGET_DIR}")