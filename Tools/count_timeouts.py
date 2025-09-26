#!/usr/bin/env python3
"""
统计packj分析结果中超时的数量，并打印超时文件的完整路径
"""

import os
import sys
from pathlib import Path

# 结果目录
RESULT_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace"

def count_timeouts():
    """统计benign和malware文件夹中超时的数量，并返回超时文件的路径"""
    result = {
        "benign": {"total": 0, "timeout": 0, "timeout_files": []},
        "malware": {"total": 0, "timeout": 0, "timeout_files": []}
    }
    
    # 遍历benign和malware文件夹
    for category in ["benign", "malware"]:
        category_dir = os.path.join(RESULT_DIR, category)
        
        if not os.path.exists(category_dir):
            print(f"❌ 目录不存在: {category_dir}")
            continue
            
        print(f"🔍 正在扫描目录: {category_dir}")
        
        # 遍历所有包
        for package_name in os.listdir(category_dir):
            package_dir = os.path.join(category_dir, package_name)
            if not os.path.isdir(package_dir):
                continue
            
            # 遍历版本
            for version in os.listdir(package_dir):
                version_dir = os.path.join(package_dir, version)
                if not os.path.isdir(version_dir):
                    continue
                
                # 检查result.txt文件
                result_file = os.path.join(version_dir, "result.txt")
                if os.path.exists(result_file):
                    result[category]["total"] += 1
                    
                    # 检查是否包含"ERROR: Timeout"
                    try:
                        with open(result_file, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content == "ERROR: Timeout":
                                result[category]["timeout"] += 1
                                result[category]["timeout_files"].append(result_file)
                    except Exception as e:
                        print(f"❌ 读取文件出错 {result_file}: {str(e)}")
    
    return result

def main():
    """主函数"""
    print("🎯 开始统计超时结果")
    
    # 统计超时
    result = count_timeouts()
    
    # 输出结果
    print("\n" + "=" * 80)
    print("📊 统计结果:")
    print("=" * 80)
    
    for category in ["benign", "malware"]:
        total = result[category]["total"]
        timeout = result[category]["timeout"]
        timeout_rate = (timeout / total * 100) if total > 0 else 0
        
        print(f"📁 {category.upper()}:")
        print(f"   - 总文件数: {total}")
        print(f"   - 超时数量: {timeout}")
        print(f"   - 超时比例: {timeout_rate:.2f}%")
        print("-" * 80)
    
    # 打印超时文件的完整路径
    print("\n" + "=" * 80)
    print("📋 超时文件列表:")
    print("=" * 80)
    
    for category in ["benign", "malware"]:
        print(f"\n📁 {category.upper()} 超时文件 ({len(result[category]['timeout_files'])}个):")
        print("-" * 80)
        
        for file_path in result[category]["timeout_files"]:
            print(f"   {file_path}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()