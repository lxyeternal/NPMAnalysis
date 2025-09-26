#!/usr/bin/env python3
"""
随机选择NPM包并复制脚本
每个包只选择一个版本，总共选择100个包进行复制
"""

import os
import shutil
import random
from pathlib import Path
from typing import List, Dict

def get_package_versions(source_dir: str) -> Dict[str, List[str]]:
    """
    获取所有包及其版本信息
    返回: {package_name: [version1, version2, ...]}
    """
    packages = {}
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"错误：源目录不存在 {source_dir}")
        return packages
    
    for package_dir in source_path.iterdir():
        if package_dir.is_dir():
            package_name = package_dir.name
            versions = []
            
            # 获取该包的所有版本
            for version_dir in package_dir.iterdir():
                if version_dir.is_dir():
                    versions.append(version_dir.name)
            
            if versions:
                packages[package_name] = versions
    
    return packages

def select_random_packages(packages: Dict[str, List[str]], num_packages: int = 100) -> Dict[str, str]:
    """
    随机选择指定数量的包，每个包随机选择一个版本
    返回: {package_name: selected_version}
    """
    if len(packages) < num_packages:
        print(f"警告：可用包数量({len(packages)})少于请求数量({num_packages})")
        num_packages = len(packages)
    
    # 随机选择包
    selected_packages = random.sample(list(packages.keys()), num_packages)
    
    # 为每个包随机选择一个版本
    result = {}
    for package_name in selected_packages:
        selected_version = random.choice(packages[package_name])
        result[package_name] = selected_version
    
    return result

def copy_selected_packages(source_dir: str, dest_dir: str, selected_packages: Dict[str, str]):
    """
    复制选中的包到目标目录
    """
    source_path = Path(source_dir)
    dest_path = Path(dest_dir)
    
    # 确保目标目录存在
    dest_path.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    failed_count = 0
    
    for package_name, version in selected_packages.items():
        source_package_path = source_path / package_name / version
        dest_package_path = dest_path / package_name
        
        try:
            if source_package_path.exists():
                # 复制整个包目录结构（包含版本）
                shutil.copytree(source_package_path.parent, dest_package_path, dirs_exist_ok=True)
                copied_count += 1
                print(f"✓ 复制成功: {package_name} (版本: {version})")
            else:
                print(f"✗ 源路径不存在: {source_package_path}")
                failed_count += 1
        except Exception as e:
            print(f"✗ 复制失败 {package_name}: {e}")
            failed_count += 1
    
    print(f"\n复制完成！成功: {copied_count}, 失败: {failed_count}")

def main():
    # 配置路径
    base_dir = "/home2/wenbo/Documents/NPMAnalysis/Dataset"
    benign_source = os.path.join(base_dir, "unzip_benign")
    malware_source = os.path.join(base_dir, "unzip_malware")
    benign_dest = os.path.join(base_dir, "unzip_benign_new")
    malware_dest = os.path.join(base_dir, "unzip_malware_new")
    
    # 设置随机种子以便重现结果
    random.seed(42)
    
    print("=== NPM包随机选择和复制工具 ===\n")
    
    # 处理benign包
    print("1. 处理benign包...")
    benign_packages = get_package_versions(benign_source)
    print(f"   发现 {len(benign_packages)} 个benign包")
    
    if benign_packages:
        selected_benign = select_random_packages(benign_packages, 100)
        print(f"   选择了 {len(selected_benign)} 个benign包进行复制")
        copy_selected_packages(benign_source, benign_dest, selected_benign)
    
    print("\n" + "="*50 + "\n")
    
    # 处理malware包
    print("2. 处理malware包...")
    malware_packages = get_package_versions(malware_source)
    print(f"   发现 {len(malware_packages)} 个malware包")
    
    if malware_packages:
        selected_malware = select_random_packages(malware_packages, 100)
        print(f"   选择了 {len(selected_malware)} 个malware包进行复制")
        copy_selected_packages(malware_source, malware_dest, selected_malware)
    
    print("\n=== 所有操作完成 ===")

if __name__ == "__main__":
    main()