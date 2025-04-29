#!/usr/bin/env python3
import os
import shutil
import re

def extract_version(package_name, folder_name):
    """从包名中提取版本号"""
    # 移除文件夹名称和后缀，保留版本部分
    version = package_name.replace(folder_name + '-', '').replace('.tgz', '')
    return version

def reorganize_packages(base_dir):
    count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.tgz'):
                # 当前文件的完整路径
                current_path = os.path.join(root, file)
                
                # 获取包文件夹名称（例如：@0xelod##smart-order-router）
                package_folder = os.path.basename(root)
                
                # 提取版本号
                version = extract_version(file, package_folder)
                
                # 创建新的版本文件夹路径
                version_folder_path = os.path.join(root, version)
                
                # 创建新的文件目标路径
                new_file_path = os.path.join(version_folder_path, file)
                
                # 如果版本文件夹不存在，则创建
                if not os.path.exists(version_folder_path):
                    os.makedirs(version_folder_path)
                
                # 移动文件
                shutil.move(current_path, new_file_path)
                count += 1
                print(f"移动: {current_path} -> {new_file_path}")
    
    print(f"总共处理了 {count} 个文件")

if __name__ == "__main__":
    base_directory = "/home/wenbo/NPMAnalysis/Dataset/zip_benign"
    reorganize_packages(base_directory) 