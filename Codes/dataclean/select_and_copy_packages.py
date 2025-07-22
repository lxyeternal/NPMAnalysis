#!/usr/bin/env python3
import os
import shutil
import random
from pathlib import Path
import re

# 源路径和目标路径
SOURCE_BASE = "/home2/mynames/Documents/NPMAnalysis/Dataset"
TARGET_BASE = "/home2/mynames/Documents/PyPIAgent/Dataset/npm_data"

# 需要跳过的包列表文件
MALWARE_BENIGN_SKIP_LIST = "/home2/mynames/Documents/NPMAnalysis/Codes/dataclean/malware_benign.txt"
SELECTED_BENIGN_SKIP_LIST = "/home2/mynames/Documents/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"

# 要选择的包数量
NUM_PACKAGES = 1000

def load_skip_list(file_path):
    """加载需要跳过的包列表"""
    skip_list = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():
                    # 转换格式从 包名/版本 到 包名
                    package_name = line.strip().split('/')[0]
                    # 对于 @namespace##package 格式，也需要保留
                    skip_list.add(package_name)
    return skip_list

def get_available_packages(folder_type):
    """获取指定类型文件夹中可用的包列表，确保每个包在zip和unzip中都存在"""
    unzip_path = os.path.join(SOURCE_BASE, f"unzip_{folder_type}")
    zip_path = os.path.join(SOURCE_BASE, f"zip_{folder_type}")
    
    # 获取unzip中的包列表
    unzip_packages = set(os.listdir(unzip_path))
    # 获取zip中的包列表
    zip_packages = set(os.listdir(zip_path))
    
    # 找出同时存在于两个目录中的包
    common_packages = unzip_packages.intersection(zip_packages)
    return list(common_packages)

def normalize_package_name(package_name):
    """将包名中的 ## 替换为 / 用于匹配跳过列表"""
    return package_name.replace('##', '/')

def should_skip_package(package_name, skip_lists):
    """检查包是否应该被跳过"""
    normalized_name = normalize_package_name(package_name)
    for skip_list in skip_lists:
        if normalized_name in skip_list:
            return True
    return False

def copy_package(package_name, folder_type):
    """复制包到目标目录，同时复制压缩和解压缩的版本"""
    try:
        unzip_source = os.path.join(SOURCE_BASE, f"unzip_{folder_type}", package_name)
        zip_source = os.path.join(SOURCE_BASE, f"zip_{folder_type}", package_name)
        
        unzip_target = os.path.join(TARGET_BASE, f"unzip_{folder_type}", package_name)
        zip_target = os.path.join(TARGET_BASE, f"zip_{folder_type}", package_name)
        
        # 查找第一个版本目录
        versions = os.listdir(unzip_source)
        if not versions:
            print(f"警告: 包 {package_name} 在解压目录中没有版本子目录")
            return False
        
        version = versions[0]  # 选择第一个版本
        
        # 确认ZIP目录中也有相同版本
        if not os.path.exists(os.path.join(zip_source, version)):
            print(f"警告: 包 {package_name} 的版本 {version} 在压缩目录中不存在")
            return False
        
        # 复制解压缩的包
        unzip_version_source = os.path.join(unzip_source, version, "package")
        if os.path.exists(unzip_version_source):
            os.makedirs(unzip_target, exist_ok=True)
            shutil.copytree(unzip_version_source, unzip_target, dirs_exist_ok=True)
        else:
            print(f"警告: 解压缩目录 {unzip_version_source} 不存在")
            return False
        
        # 复制压缩包
        zip_version_source = os.path.join(zip_source, version)
        zip_files = [f for f in os.listdir(zip_version_source) if f.endswith('.tgz')]
        if zip_files:
            os.makedirs(zip_target, exist_ok=True)
            zip_file = zip_files[0]
            shutil.copy2(os.path.join(zip_version_source, zip_file), os.path.join(zip_target, zip_file))
        else:
            print(f"警告: 压缩目录 {zip_version_source} 中没有找到.tgz文件")
            return False
        
        print(f"成功复制包 {package_name} 版本 {version}")
        return True
    except Exception as e:
        print(f"复制包 {package_name} 时出错: {str(e)}")
        return False

def main():
    """主函数"""
    # 加载需要跳过的包列表
    malware_benign_skip_list = load_skip_list(MALWARE_BENIGN_SKIP_LIST)
    selected_benign_skip_list = load_skip_list(SELECTED_BENIGN_SKIP_LIST)
    
    print(f"已加载需要跳过的恶意样本: {len(malware_benign_skip_list)} 个")
    print(f"已加载需要跳过的良性样本: {len(selected_benign_skip_list)} 个")
    
    # 确保目标目录存在
    for folder in ["unzip_benign", "unzip_malware", "zip_benign", "zip_malware"]:
        os.makedirs(os.path.join(TARGET_BASE, folder), exist_ok=True)
    
    # 获取可用的包列表
    benign_packages = get_available_packages("benign")
    malware_packages = get_available_packages("malware")
    
    print(f"找到 {len(benign_packages)} 个可用的良性包")
    print(f"找到 {len(malware_packages)} 个可用的恶意包")
    
    # 过滤掉需要跳过的包
    benign_packages = [p for p in benign_packages if not should_skip_package(p, [selected_benign_skip_list])]
    malware_packages = [p for p in malware_packages if not should_skip_package(p, [malware_benign_skip_list])]
    
    print(f"过滤后剩余 {len(benign_packages)} 个良性包")
    print(f"过滤后剩余 {len(malware_packages)} 个恶意包")
    
    # 随机选择包
    if len(benign_packages) >= NUM_PACKAGES:
        selected_benign = random.sample(benign_packages, NUM_PACKAGES)
    else:
        selected_benign = benign_packages
        print(f"警告: 良性包数量不足 {NUM_PACKAGES}，仅选择了 {len(selected_benign)} 个")
    
    if len(malware_packages) >= NUM_PACKAGES:
        selected_malware = random.sample(malware_packages, NUM_PACKAGES)
    else:
        selected_malware = malware_packages
        print(f"警告: 恶意包数量不足 {NUM_PACKAGES}，仅选择了 {len(selected_malware)} 个")
    
    # 复制包
    benign_success = 0
    for package in selected_benign:
        if copy_package(package, "benign"):
            benign_success += 1
    
    malware_success = 0
    for package in selected_malware:
        if copy_package(package, "malware"):
            malware_success += 1
    
    print(f"成功复制 {benign_success}/{len(selected_benign)} 个良性包")
    print(f"成功复制 {malware_success}/{len(selected_malware)} 个恶意包")
    
    # 保存选择的包列表，方便以后参考
    with open(os.path.join(TARGET_BASE, "selected_benign_packages.txt"), 'w') as f:
        for package in selected_benign:
            f.write(f"{package}\n")
    
    with open(os.path.join(TARGET_BASE, "selected_malware_packages.txt"), 'w') as f:
        for package in selected_malware:
            f.write(f"{package}\n")

if __name__ == "__main__":
    main() 