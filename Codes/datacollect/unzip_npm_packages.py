#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# @File     : unzip_npm_packages.py
# @Project  : NPMAnalysis
# Time      : 2024
# Author    : mynames
# version   : python 3.8
# Description：解压NPM包并保持三级目录结构 (名称-版本-解压后文件)
"""

import os
import tarfile
import zipfile


def mkdir(unzip_filepath) -> None:
    """创建目录（如果不存在）"""
    if not os.path.exists(unzip_filepath):
        os.makedirs(unzip_filepath)


def untar_file(raw_filepath, unzip_filepath):
    """解压tar.gz或tgz包"""
    with tarfile.open(raw_filepath) as tf:
        tf.extractall(unzip_filepath)
    return unzip_filepath


def unzip_file(raw_filepath, unzip_filepath):
    """解压zip包"""
    with zipfile.ZipFile(raw_filepath, "r") as zFile:
        for fileM in zFile.namelist():
            zFile.extract(fileM, unzip_filepath)
    return unzip_filepath


def depresspkg(filepath, unzip_filepath):
    """根据文件扩展名解压文件"""
    tar_suffix = ".tar.gz"
    zip_suffix = ".zip"
    whl_suffix = ".whl"
    tgz_suffix = ".tgz"

    mkdir(unzip_filepath)

    try:
        if filepath.endswith(tar_suffix) or filepath.endswith(tgz_suffix):
            return untar_file(filepath, unzip_filepath)
        elif filepath.endswith(zip_suffix) or filepath.endswith(whl_suffix):
            return unzip_file(filepath, unzip_filepath)
        else:
            print(f"不支持的文件格式: {filepath}")
            return filepath
    except Exception as e:
        print(f"解压 {filepath} 失败: {e}")
        return filepath


def process_npm_packages(input_dir, output_dir):
    """
    处理三级结构的NPM包目录
    结构: input_dir/包名/版本/包文件.tgz
    """
    if not os.path.exists(input_dir):
        print(f"输入目录不存在: {input_dir}")
        return

    # 创建输出根目录
    mkdir(output_dir)
    
    # 统计计数器
    total_packages = 0
    successful_unzips = 0
    failed_unzips = 0
    
    print(f"开始处理目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    # 遍历包名目录
    for pkg_name in os.listdir(input_dir):
        pkg_path = os.path.join(input_dir, pkg_name)
        if not os.path.isdir(pkg_path):
            continue
            
        # 遍历版本目录
        for version in os.listdir(pkg_path):
            version_path = os.path.join(pkg_path, version)
            if not os.path.isdir(version_path):
                continue
                
            # 遍历版本目录下的文件
            for filename in os.listdir(version_path):
                file_path = os.path.join(version_path, filename)
                if not os.path.isfile(file_path):
                    continue
                    
                # 创建对应的输出目录
                output_pkg_dir = os.path.join(output_dir, pkg_name)
                output_version_dir = os.path.join(output_pkg_dir, version)
                
                # 解压文件
                total_packages += 1
                try:
                    depresspkg(file_path, output_version_dir)
                    print(f"成功: {pkg_name}/{version}/{filename}")
                    successful_unzips += 1
                except Exception as e:
                    print(f"失败: {pkg_name}/{version}/{filename} - 错误: {str(e)}")
                    failed_unzips += 1
    
    print("\n解压总结:")
    print(f"总包数: {total_packages}")
    print(f"成功解压: {successful_unzips}")
    print(f"失败解压: {failed_unzips}")


if __name__ == "__main__":
    # 定义固定的输入和输出路径
    benign_input_dir = "/home/mynames/NPMAnalysis/Dataset/zip_benign"
    benign_output_dir = "/home/mynames/NPMAnalysis/Dataset/unzip_benign"
    malware_input_dir = "/home/mynames/NPMAnalysis/Dataset/zip_malware"
    malware_output_dir = "/home/mynames/NPMAnalysis/Dataset/unzip_malware"
    
    print("==== 开始解压良性NPM包 ====")
    process_npm_packages(benign_input_dir, benign_output_dir)
    
    print("\n==== 开始解压恶意NPM包 ====")
    process_npm_packages(malware_input_dir, malware_output_dir)
    
    print("\n所有解压任务完成！") 