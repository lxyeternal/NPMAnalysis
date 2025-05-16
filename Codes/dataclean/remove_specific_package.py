#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sys
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("removal_specific_log.txt"),
        logging.StreamHandler()
    ]
)

# 要处理的基础路径
MALWARE_PATHS = [
    "/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware",
    "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
]

TOOL_OUTPUT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output"

# 要删除的包和版本
PACKAGE_NAME = "@diotoborg##aperiam-cum"
VERSION = "1.1.11"

def remove_package_version(base_path, package_name, version, dry_run=False):
    """
    删除指定路径下的包版本目录，如果包目录为空则一并删除
    
    参数:
        base_path: 基础路径
        package_name: 包名
        version: 版本号
        dry_run: 是否只打印不执行删除操作
    """
    package_path = os.path.join(base_path, package_name)
    
    # 检查包路径是否存在
    if not os.path.exists(package_path):
        logging.info(f"包路径不存在: {package_path}")
        return False
    
    version_path = os.path.join(package_path, version)
    
    # 检查版本路径是否存在
    if not os.path.exists(version_path):
        logging.info(f"版本路径不存在: {version_path}")
        return False
    
    if dry_run:
        # 只打印要删除的版本目录
        logging.info(f"将要删除版本目录: {version_path}")
        
        # 检查包目录是否会变为空
        remaining_files = [f for f in os.listdir(package_path) if f != version]
        if not remaining_files:
            logging.info(f"删除后包目录将为空，将要删除包目录: {package_path}")
        
        return True
    else:
        # 执行实际删除
        try:
            shutil.rmtree(version_path)
            logging.info(f"已删除版本目录: {version_path}")
            
            # 检查包目录是否为空
            if len(os.listdir(package_path)) == 0:
                shutil.rmtree(package_path)
                logging.info(f"包目录为空，已删除: {package_path}")
            
            return True
        except Exception as e:
            logging.error(f"删除失败: {version_path}, 错误: {str(e)}")
            return False

def process_tool_output_directory(tool_output_path, package_name, version, dry_run=False):
    """
    处理工具输出目录中的包版本
    """
    count = 0
    # 遍历工具输出目录下的所有工具文件夹
    for tool_dir in os.listdir(tool_output_path):
        tool_path = os.path.join(tool_output_path, tool_dir)
        
        if not os.path.isdir(tool_path):
            continue
        
        # 特殊处理packj工具
        if tool_dir == "packj":
            for result_type in ["result_static", "result_trace"]:
                result_path = os.path.join(tool_path, result_type)
                if os.path.exists(result_path):
                    malware_path = os.path.join(result_path, "malware")
                    if os.path.exists(malware_path):
                        if remove_package_version(malware_path, package_name, version, dry_run):
                            count += 1
        else:
            # 处理其他工具
            malware_path = os.path.join(tool_path, "malware")
            if os.path.exists(malware_path):
                if remove_package_version(malware_path, package_name, version, dry_run):
                    count += 1
    
    return count

def main():
    """
    主函数
    """
    # 检查是否有--execute参数
    execute_mode = "--execute" in sys.argv
    
    if execute_mode:
        print("警告: 将执行实际删除操作!")
        confirmation = input(f"确认要删除包 {PACKAGE_NAME} 版本 {VERSION} 吗? (yes/no): ")
        
        if confirmation.lower() != "yes":
            print("操作已取消")
            return
        
        logging.info("执行模式: 将执行实际删除操作")
    else:
        logging.info("测试模式: 只打印将要删除的文件，不执行实际删除操作")
    
    logging.info(f"准备处理包 {PACKAGE_NAME} 版本 {VERSION}")
    
    total_count = 0
    
    # 处理主要的恶意软件路径
    for base_path in MALWARE_PATHS:
        if os.path.exists(base_path):
            if remove_package_version(base_path, PACKAGE_NAME, VERSION, not execute_mode):
                total_count += 1
        else:
            logging.warning(f"路径不存在: {base_path}")
    
    # 处理工具输出目录
    if os.path.exists(TOOL_OUTPUT_PATH):
        count = process_tool_output_directory(TOOL_OUTPUT_PATH, PACKAGE_NAME, VERSION, not execute_mode)
        total_count += count
    else:
        logging.warning(f"工具输出路径不存在: {TOOL_OUTPUT_PATH}")
    
    if execute_mode:
        logging.info(f"删除操作完成，共删除 {total_count} 个目录")
    else:
        logging.info(f"检查完成，共找到 {total_count} 个将要删除的目录")
        logging.info("这只是测试运行，未执行实际删除操作。要执行实际删除，请使用 --execute 参数运行脚本。")

if __name__ == "__main__":
    main() 