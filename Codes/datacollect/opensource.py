#!/usr/bin/env python3
import os
import shutil
import glob
from pathlib import Path

def load_skip_list(file_path):
    """加载需要跳过的包列表"""
    skip_list = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():
                    skip_list.add(line.strip())
    return skip_list

def extract_package_info_from_path(zip_path):
    """
    从zip文件路径中提取包名和版本信息
    路径格式示例：
    - /path/to/@0xelod##smart-order-router/3.25.4-theta/@0xelod##smart-order-router-3.25.4-theta.tgz
    - /path/to/@12build##segment-js-sdk/3.434.3/segment-js-sdk-3.434.3.tgz
    
    返回格式保持##符号，与跳过列表格式一致：@zitterorg##quis-tempora-excepturi/1.0.16
    """
    path_parts = Path(zip_path).parts
    
    # 找到包名和版本
    package_name = None
    version = None
    
    # 从倒数第三个部分开始找（因为最后是文件名，倒数第二是版本，倒数第三是包名）
    if len(path_parts) >= 3:
        version = path_parts[-2]  # 版本文件夹
        package_name = path_parts[-3]  # 包名文件夹
    
    if package_name and version:
        # 保持##格式，与跳过列表格式一致
        return f"{package_name}/{version}"
    
    return None

def find_zip_files(source_path):
    """递归查找所有的tgz文件"""
    zip_files = []
    
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith('.tgz') or file.endswith('.tar.gz'):
                zip_files.append(os.path.join(root, file))
    
    return zip_files

def copy_zip_files(source_benign, source_malware, target_base, malware_skip_list, benign_skip_list):
    """
    复制zip文件到目标路径，按照跳过逻辑过滤
    
    目标结构：
    target_base/
    ├── benign/
    │   └── 包名/版本/压缩包文件
    └── malware/
        └── 包名/版本/压缩包文件
    """
    
    # 确保目标目录存在
    target_benign = os.path.join(target_base, 'benign')
    target_malware = os.path.join(target_base, 'malware')
    os.makedirs(target_benign, exist_ok=True)
    os.makedirs(target_malware, exist_ok=True)
    
    copied_count = {'benign': 0, 'malware': 0}
    skipped_count = {'benign': 0, 'malware': 0}
    
    # 处理良性样本
    print("处理良性样本...")
    benign_files = find_zip_files(source_benign)
    
    for zip_file in benign_files:
        package_info = extract_package_info_from_path(zip_file)
        
        if not package_info:
            print(f"警告: 无法从路径提取包信息: {zip_file}")
            continue
        
        # 检查是否需要跳过
        if package_info in benign_skip_list:
            print(f"跳过良性样本: {package_info}")
            skipped_count['benign'] += 1
            continue
        
        # 构建目标路径
        package_name, version = package_info.split('/', 1)
        # 包名已经是##格式，直接用作文件夹名
        safe_package_name = package_name
        
        target_dir = os.path.join(target_benign, safe_package_name, version)
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制文件
        filename = os.path.basename(zip_file)
        target_file = os.path.join(target_dir, filename)
        
        try:
            # 如果目标文件已存在，跳过复制
            if os.path.exists(target_file):
                print(f"目标文件已存在，跳过: {package_info}")
                continue
            
            shutil.copy2(zip_file, target_file)
            print(f"复制良性样本: {package_info} -> {target_file}")
            copied_count['benign'] += 1
            
        except Exception as e:
            print(f"复制文件失败 {zip_file}: {e}")
    
    # 处理恶意样本
    print("\n处理恶意样本...")
    malware_files = find_zip_files(source_malware)
    
    for zip_file in malware_files:
        package_info = extract_package_info_from_path(zip_file)
        
        if not package_info:
            print(f"警告: 无法从路径提取包信息: {zip_file}")
            continue
        
        # 检查是否需要跳过
        if package_info in malware_skip_list:
            print(f"跳过恶意样本: {package_info}")
            skipped_count['malware'] += 1
            continue
        
        # 构建目标路径
        package_name, version = package_info.split('/', 1)
        # 包名已经是##格式，直接用作文件夹名
        safe_package_name = package_name
        
        target_dir = os.path.join(target_malware, safe_package_name, version)
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制文件
        filename = os.path.basename(zip_file)
        target_file = os.path.join(target_dir, filename)
        
        try:
            # 如果目标文件已存在，跳过复制
            if os.path.exists(target_file):
                print(f"目标文件已存在，跳过: {package_info}")
                continue
            
            shutil.copy2(zip_file, target_file)
            print(f"复制恶意样本: {package_info} -> {target_file}")
            copied_count['malware'] += 1
            
        except Exception as e:
            print(f"复制文件失败 {zip_file}: {e}")
    
    return copied_count, skipped_count

def main():
    """主函数"""
    
    # 配置路径
    source_benign = "/home2/mynames/Documents/NPMAnalysis/Dataset/zip_benign"
    source_malware = "/home2/mynames/Documents/NPMAnalysis/Dataset/zip_malware"
    target_base = "/home2/mynames/Documents/NPMAnalysis/Open_Dataset"
    
    # 跳过列表路径
    malware_skip_path = "/home2/mynames/Documents/NPMAnalysis/Codes/dataclean/malware_benign.txt"
    benign_skip_path = "/home2/mynames/Documents/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"
    
    # 检查源路径是否存在
    if not os.path.exists(source_benign):
        print(f"错误: 良性样本源路径不存在: {source_benign}")
        return
    
    if not os.path.exists(source_malware):
        print(f"错误: 恶意样本源路径不存在: {source_malware}")
        return
    
    # 加载跳过列表
    malware_skip_list = load_skip_list(malware_skip_path)
    benign_skip_list = load_skip_list(benign_skip_path)
    
    print(f"已加载需要跳过的恶意样本: {len(malware_skip_list)} 个")
    print(f"已加载需要跳过的良性样本: {len(benign_skip_list)} 个")
    print("-" * 60)
    
    # 确认操作
    print(f"源路径 (良性): {source_benign}")
    print(f"源路径 (恶意): {source_malware}")
    print(f"目标路径: {target_base}")
    print("-" * 60)
    
    # 统计源文件数量
    benign_files = find_zip_files(source_benign)
    malware_files = find_zip_files(source_malware)
    
    print(f"发现良性样本文件: {len(benign_files)} 个")
    print(f"发现恶意样本文件: {len(malware_files)} 个")
    print("-" * 60)
    
    # 询问用户确认
    confirm = input("确认开始复制文件? (y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        return
    
    # 开始复制文件
    try:
        copied_count, skipped_count = copy_zip_files(
            source_benign, source_malware, target_base, 
            malware_skip_list, benign_skip_list
        )
        
        # 打印统计结果
        print("\n" + "=" * 60)
        print("文件复制完成!")
        print(f"良性样本 - 复制: {copied_count['benign']} 个, 跳过: {skipped_count['benign']} 个")
        print(f"恶意样本 - 复制: {copied_count['malware']} 个, 跳过: {skipped_count['malware']} 个")
        print(f"总计 - 复制: {copied_count['benign'] + copied_count['malware']} 个, "
              f"跳过: {skipped_count['benign'] + skipped_count['malware']} 个")
        
    except KeyboardInterrupt:
        print("\n操作被用户中断")
    except Exception as e:
        print(f"操作过程中出现错误: {e}")

if __name__ == "__main__":
    main()