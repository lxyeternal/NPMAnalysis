#!/usr/bin/env python3
"""
将匹配的包从Dataset目录复制到/tmp/domain_package目录
并对包名进行特殊处理，将##替换为/
"""

import os
import shutil
import sys
from pathlib import Path

# 定义路径常量
DATASET_BASE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset"
TARGET_BASE_DIR = "/tmp/domain_package"
ERROR_PACKAGES_FILE = "/home2/wenbo/Documents/NPMAnalysis/trace_error_packages_list.txt"

def read_error_packages(file_path):
    """
    读取错误包列表文件
    返回格式: [(category, package_name, version), ...]
    """
    packages = []
    if not os.path.exists(file_path):
        print(f"错误：文件不存在 {file_path}")
        return packages
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # 跳过空行
                continue
            
            parts = line.split('\t')
            if len(parts) >= 3:
                category = parts[0].strip()  # unzip_malware 或 unzip_benign
                package_name = parts[1].strip()
                version = parts[2].strip()
                
                # 验证数据有效性
                if category and package_name and version:
                    packages.append((category, package_name, version))
                else:
                    print(f"警告：第{line_num}行数据无效（含空字段）: {line}")
            else:
                print(f"警告：第{line_num}行格式不正确（字段数 < 3）: {line}")
    
    return packages

def convert_package_name(package_name):
    """
    将包名中的##替换为/
    例如: @aluffyz##discord-botjs -> @aluffyz/discord-botjs
    """
    if '##' in package_name:
        return package_name.replace('##', '/')
    return package_name

def find_package_directory(category, package_name, version):
    """
    查找包目录
    """
    source_dir = os.path.join(DATASET_BASE_DIR, category, package_name, version)
    if os.path.exists(source_dir):
        return source_dir
    return None

def copy_package(category, package_name, version, source_dir):
    """
    复制包到目标目录
    """
    # 转换包名（将##替换为/）
    converted_package_name = convert_package_name(package_name)
    
    # 构建目标路径
    target_dir = os.path.join(TARGET_BASE_DIR, category, converted_package_name, version)
    
    try:
        # 创建目标目录
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        
        # 检查目标是否已存在
        if os.path.exists(target_dir):
            print(f"跳过：目标已存在 {target_dir}")
            return True
        
        # 复制目录
        shutil.copytree(source_dir, target_dir)
        print(f"成功复制: {source_dir} -> {target_dir}")
        return True
        
    except Exception as e:
        print(f"复制失败: {source_dir} -> {target_dir}, 错误: {str(e)}")
        return False

def main(test_mode=False, test_limit=10):
    """
    主函数
    """
    print("开始处理包复制...")
    
    # 创建目标基础目录
    os.makedirs(TARGET_BASE_DIR, exist_ok=True)
    
    # 读取错误包列表
    packages = read_error_packages(ERROR_PACKAGES_FILE)
    print(f"读取到 {len(packages)} 个包")
    
    if not packages:
        print("没有找到需要处理的包")
        return
    
    # 测试模式：只处理前几个包
    if test_mode:
        packages = packages[:test_limit]
        print(f"测试模式：只处理前 {len(packages)} 个包")
    
    # 统计信息
    success_count = 0
    not_found_count = 0
    error_count = 0
    
    # 处理每个包
    for i, (category, package_name, version) in enumerate(packages, 1):
        print(f"\n处理 {i}/{len(packages)}: {category}/{package_name}/{version}")
        
        # 显示转换后的包名
        converted_name = convert_package_name(package_name)
        if converted_name != package_name:
            print(f"包名转换: {package_name} -> {converted_name}")
        
        # 查找源目录
        source_dir = find_package_directory(category, package_name, version)
        
        if source_dir is None:
            print(f"未找到源目录: {category}/{package_name}/{version}")
            not_found_count += 1
            continue
        
        print(f"找到源目录: {source_dir}")
        
        # 复制包
        if copy_package(category, package_name, version, source_dir):
            success_count += 1
        else:
            error_count += 1
    
    # 打印统计结果
    print(f"\n处理完成:")
    print(f"成功复制: {success_count}")
    print(f"未找到: {not_found_count}")
    print(f"复制失败: {error_count}")
    print(f"总计: {len(packages)}")

if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_limit = 10
        if len(sys.argv) > 2:
            try:
                test_limit = int(sys.argv[2])
            except ValueError:
                print("警告：测试限制参数无效，使用默认值 10")
        main(test_mode=True, test_limit=test_limit)
    else:
        main()
