#!/usr/bin/env python3
import os

def count_unique_package_versions(base_path):
    unique_combinations = set()
    
    # 遍历基础目录
    for package_name in os.listdir(base_path):
        package_path = os.path.join(base_path, package_name)
        
        # 确保是目录
        if os.path.isdir(package_path):
            # 遍历每个包下的版本目录
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                
                # 确保是目录
                if os.path.isdir(version_path):
                    # 按照指定格式连接包名和版本号
                    combination = f"{package_name}$${version}"
                    unique_combinations.add(combination)
    
    return unique_combinations

if __name__ == "__main__":
    benign_path = "/home/wenbo/NPMAnalysis/Dataset/unzip_benign"
    unique_combinations = count_unique_package_versions(benign_path)
    
    print(f"共有 {len(unique_combinations)} 个不重复的包名$$版本号组合")
    
    # 可选：输出所有组合到文件
    # with open("unique_packages.txt", "w") as f:
    #     for combo in sorted(unique_combinations):
    #         f.write(f"{combo}\n") 