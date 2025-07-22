#!/usr/bin/env python3
import os
import random
import glob

# 指定路径
benign_path = "/home2/mynames/Documents/NPMAnalysis/Dataset/zip_benign"
output_file = "selected_benign_packages.txt"

def get_all_package_versions():
    """获取所有包的版本信息"""
    package_versions = []
    
    # 遍历所有包目录
    for package_dir in glob.glob(os.path.join(benign_path, "*")):
        if not os.path.isdir(package_dir):
            continue
            
        package_name = os.path.basename(package_dir)
        
        # 遍历包内的所有版本目录
        for version_dir in glob.glob(os.path.join(package_dir, "*")):
            if not os.path.isdir(version_dir):
                continue
                
            version = os.path.basename(version_dir)
            
            # 检查是否存在对应的tgz文件
            tgz_file = os.path.join(version_dir, f"{package_name}-{version}.tgz")
            if os.path.exists(tgz_file):
                package_versions.append((package_name, version))
    
    return package_versions

def main():
    print("开始收集所有包版本信息...")
    all_versions = get_all_package_versions()
    total_versions = len(all_versions)
    print(f"共找到 {total_versions} 个包版本")
    
    # 选择1000个版本（或全部，如果总数少于1000）
    num_to_select = min(1000, total_versions)
    selected_versions = random.sample(all_versions, num_to_select)
    
    # 写入文件
    with open(output_file, "w") as f:
        for package_name, version in selected_versions:
            f.write(f"{package_name}/{version}\n")
    
    print(f"已成功选择 {num_to_select} 个包版本并写入到 {output_file}")

if __name__ == "__main__":
    main()
