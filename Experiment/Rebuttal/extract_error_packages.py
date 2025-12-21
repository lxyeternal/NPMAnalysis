#!/usr/bin/env python3
"""
从detailed_error_analysis_report.txt中提取包名和版本信息
输出格式: 类型 \t 包名 \t 版本
"""

import re
import sys
from pathlib import Path

def extract_packages_from_report(report_file):
    """
    从错误报告文件中提取包名和版本信息
    """
    malware_packages = []
    benign_packages = []
    
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文件失败: {e}", file=sys.stderr)
        return [], []
    
    # 分割恶意包和良性包部分
    sections = content.split('【良性包 ERROR 文件】')
    
    if len(sections) >= 2:
        malware_section = sections[0]
        benign_section = sections[1]
    else:
        # 如果没有良性包部分，全部当作恶意包
        malware_section = content
        benign_section = ""
    
    # 提取恶意包信息
    malware_packages = extract_packages_from_section(malware_section, "malware")
    
    # 提取良性包信息
    if benign_section:
        benign_packages = extract_packages_from_section(benign_section, "benign")
    
    return malware_packages, benign_packages

def extract_packages_from_section(section_content, package_type):
    """
    从一个部分中提取包信息
    """
    packages = []
    
    # 匹配包名/版本的模式
    # 例如: "   1. arm-machinelearningservices/99.10.9"
    # 或者: "   1. @aluffyz##discord-botjs/1.4.2"
    pattern = r'^\s*\d+\.\s+(.+?)/(.+?)(?:\s|$)'
    
    lines = section_content.split('\n')
    
    for line in lines:
        # 跳过路径行和内容行
        if '路径:' in line or '内容:' in line:
            continue
            
        match = re.match(pattern, line)
        if match:
            package_name = match.group(1).strip()
            version = match.group(2).strip()
            
            # 清理版本号中的额外字符
            # 例如: "1.1.4zhe'yan" -> "1.1.4"
            version = re.sub(r'[^0-9\.\-\w].*$', '', version)
            
            packages.append((package_name, version))
    
    return packages

def output_formatted_results(malware_packages, benign_packages, output_file=None):
    """
    输出格式化的结果
    """
    output_lines = []
    
    # 添加恶意包
    for package_name, version in malware_packages:
        output_lines.append(f"unzip_malware\t{package_name}\t{version}")
    
    # 添加良性包
    for package_name, version in benign_packages:
        output_lines.append(f"unzip_benign\t{package_name}\t{version}")
    
    # 输出结果
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for line in output_lines:
                    f.write(line + '\n')
            print(f"结果已保存到: {output_file}")
        except Exception as e:
            print(f"保存文件失败: {e}", file=sys.stderr)
    else:
        # 输出到标准输出
        for line in output_lines:
            print(line)
    
    return output_lines

def print_statistics(malware_packages, benign_packages):
    """
    打印统计信息
    """
    print(f"\n统计信息:", file=sys.stderr)
    print(f"恶意包数量: {len(malware_packages)}", file=sys.stderr)
    print(f"良性包数量: {len(benign_packages)}", file=sys.stderr)
    print(f"总计: {len(malware_packages) + len(benign_packages)}", file=sys.stderr)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='从错误报告中提取包名和版本信息')
    parser.add_argument('report_file', help='错误报告文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（可选，默认输出到标准输出）')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not Path(args.report_file).exists():
        print(f"错误: 文件不存在 {args.report_file}", file=sys.stderr)
        sys.exit(1)
    
    # 提取包信息
    malware_packages, benign_packages = extract_packages_from_report(args.report_file)
    
    # 输出结果
    output_formatted_results(malware_packages, benign_packages, args.output)
    
    # 显示统计信息
    if args.stats:
        print_statistics(malware_packages, benign_packages)

if __name__ == "__main__":
    main()
