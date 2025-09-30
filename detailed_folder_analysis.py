#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细的文件夹分析脚本
分析malware和benign文件夹的结构和ERROR文件
"""

import os
import json
from collections import defaultdict

# 定义基础路径
BASE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace_new"
MALWARE_DIR = os.path.join(BASE_DIR, "malware")
BENIGN_DIR = os.path.join(BASE_DIR, "benign")

def load_skip_lists():
    """加载需要跳过的包列表"""
    malware_skip_versions = set()
    benign_skip_versions = set()
    
    # 加载malware需要跳过的包（从malware_benign.txt）
    malware_skip_file = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/malware_benign.txt"
    if os.path.exists(malware_skip_file):
        try:
            with open(malware_skip_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # 跳过空行
                        malware_skip_versions.add(line)
        except Exception as e:
            print(f"加载malware跳过列表失败: {malware_skip_file}, 错误: {e}")
    
    # 加载benign需要跳过的包（从selected_benign_packages.txt）
    benign_skip_file = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"
    if os.path.exists(benign_skip_file):
        try:
            with open(benign_skip_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # 跳过空行
                        benign_skip_versions.add(line)
        except Exception as e:
            print(f"加载benign跳过列表失败: {benign_skip_file}, 错误: {e}")
    
    print(f"加载了 {len(malware_skip_versions)} 个malware需要跳过的包")
    print(f"加载了 {len(benign_skip_versions)} 个benign需要跳过的包")
    
    return malware_skip_versions, benign_skip_versions

def analyze_directory_structure(base_dir, dir_type):
    """
    分析目录结构
    
    Args:
        base_dir: 基础目录路径
        dir_type: 目录类型 ("malware" 或 "benign")
    
    Returns:
        tuple: (包名文件夹数量, 版本文件夹数量, 包名到版本的映射, 所有版本路径列表)
    """
    print(f"\n{'='*60}")
    print(f"分析 {dir_type.upper()} 目录结构")
    print(f"{'='*60}")
    
    if not os.path.exists(base_dir):
        print(f"目录不存在: {base_dir}")
        return 0, 0, {}, []
    
    package_count = 0
    version_count = 0
    package_to_versions = defaultdict(list)
    all_version_paths = []
    
    # 遍历包名文件夹
    for package_name in os.listdir(base_dir):
        package_path = os.path.join(base_dir, package_name)
        
        if os.path.isdir(package_path):
            package_count += 1
            
            # 遍历版本文件夹
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                
                if os.path.isdir(version_path):
                    version_count += 1
                    package_to_versions[package_name].append(version)
                    all_version_paths.append({
                        'package': package_name,
                        'version': version,
                        'path': version_path,
                        'package_version': f"{package_name}/{version}"
                    })
    
    print(f"包名文件夹数量: {package_count}")
    print(f"版本文件夹数量: {version_count}")
    print(f"平均每个包的版本数: {version_count/package_count if package_count > 0 else 0:.2f}")
    
    # 显示版本数最多的前10个包
    sorted_packages = sorted(package_to_versions.items(), key=lambda x: len(x[1]), reverse=True)
    print(f"\n版本数最多的前10个包:")
    for i, (pkg, versions) in enumerate(sorted_packages[:10], 1):
        print(f"  {i:2d}. {pkg}: {len(versions)} 个版本")
    
    return package_count, version_count, dict(package_to_versions), all_version_paths

def filter_skip_versions(all_version_paths, skip_versions, dir_type):
    """
    过滤需要跳过的版本
    
    Args:
        all_version_paths: 所有版本路径列表
        skip_versions: 需要跳过的版本集合
        dir_type: 目录类型
    
    Returns:
        tuple: (过滤后的版本路径列表, 跳过的数量)
    """
    print(f"\n{'='*60}")
    print(f"过滤 {dir_type.upper()} 中需要跳过的版本")
    print(f"{'='*60}")
    
    filtered_paths = []
    skipped_count = 0
    skipped_details = []
    
    for version_info in all_version_paths:
        package_version = version_info['package_version']
        
        if package_version in skip_versions:
            skipped_count += 1
            skipped_details.append(package_version)
            print(f"  跳过: {package_version}")
        else:
            filtered_paths.append(version_info)
    
    print(f"\n过滤前版本数量: {len(all_version_paths)}")
    print(f"跳过版本数量: {skipped_count}")
    print(f"过滤后版本数量: {len(filtered_paths)}")
    
    # 显示前10个跳过的包作为示例
    if skipped_details:
        print(f"\n跳过的包示例（前10个）:")
        for i, pkg in enumerate(skipped_details[:10], 1):
            print(f"  {i:2d}. {pkg}")
        if len(skipped_details) > 10:
            print(f"  ... 还有 {len(skipped_details) - 10} 个")
    
    return filtered_paths, skipped_count

def analyze_error_files(filtered_paths, dir_type):
    """
    分析ERROR文件
    
    Args:
        filtered_paths: 过滤后的版本路径列表
        dir_type: 目录类型
    
    Returns:
        tuple: (ERROR文件数量, ERROR文件路径列表, 正常文件数量, 缺失文件数量)
    """
    print(f"\n{'='*60}")
    print(f"分析 {dir_type.upper()} 中的ERROR文件")
    print(f"{'='*60}")
    
    error_count = 0
    normal_count = 0
    missing_count = 0
    error_file_paths = []
    
    print("ERROR文件详情:")
    
    for version_info in filtered_paths:
        result_file = os.path.join(version_info['path'], 'result.txt')
        
        if not os.path.exists(result_file):
            missing_count += 1
            continue
        
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                if content.startswith("ERROR:"):
                    error_count += 1
                    error_file_paths.append({
                        'package_version': version_info['package_version'],
                        'file_path': result_file,
                        'content': content
                    })
                    print(f"  ERROR: {version_info['package_version']}")
                    print(f"    路径: {result_file}")
                    print(f"    内容: {content}")
                    print()
                else:
                    normal_count += 1
                    
        except Exception as e:
            print(f"  读取文件失败: {result_file}, 错误: {e}")
            missing_count += 1
    
    print(f"\n统计结果:")
    print(f"  总版本数量: {len(filtered_paths)}")
    print(f"  ERROR文件数量: {error_count}")
    print(f"  正常文件数量: {normal_count}")
    print(f"  缺失文件数量: {missing_count}")
    print(f"  ERROR比例: {error_count/len(filtered_paths)*100 if filtered_paths else 0:.2f}%")
    
    return error_count, error_file_paths, normal_count, missing_count

def save_error_report(malware_errors, benign_errors):
    """保存ERROR报告"""
    report_file = "/home2/wenbo/Documents/NPMAnalysis/detailed_error_analysis_report.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("详细ERROR文件分析报告\n")
        f.write("=" * 80 + "\n\n")
        
        # Malware ERROR文件
        f.write(f"【恶意包 ERROR 文件】\n")
        f.write(f"ERROR文件数量: {len(malware_errors)}\n\n")
        
        for i, error_info in enumerate(malware_errors, 1):
            f.write(f"{i:4d}. {error_info['package_version']}\n")
            f.write(f"      路径: {error_info['file_path']}\n")
            f.write(f"      内容: {error_info['content']}\n\n")
        
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Benign ERROR文件
        f.write(f"【良性包 ERROR 文件】\n")
        f.write(f"ERROR文件数量: {len(benign_errors)}\n\n")
        
        for i, error_info in enumerate(benign_errors, 1):
            f.write(f"{i:4d}. {error_info['package_version']}\n")
            f.write(f"      路径: {error_info['file_path']}\n")
            f.write(f"      内容: {error_info['content']}\n\n")
    
    print(f"\n详细报告已保存到: {report_file}")

def main():
    """主函数"""
    print("开始详细分析文件夹结构和ERROR文件...")
    
    # 加载跳过列表
    malware_skip_versions, benign_skip_versions = load_skip_lists()
    
    # 分析malware目录
    malware_pkg_count, malware_ver_count, malware_pkg_to_ver, malware_all_paths = analyze_directory_structure(MALWARE_DIR, "malware")
    
    # 分析benign目录
    benign_pkg_count, benign_ver_count, benign_pkg_to_ver, benign_all_paths = analyze_directory_structure(BENIGN_DIR, "benign")
    
    # 过滤跳过的版本（使用对应的跳过列表）
    malware_filtered, malware_skipped = filter_skip_versions(malware_all_paths, malware_skip_versions, "malware")
    benign_filtered, benign_skipped = filter_skip_versions(benign_all_paths, benign_skip_versions, "benign")
    
    # 分析ERROR文件
    malware_error_count, malware_error_paths, malware_normal, malware_missing = analyze_error_files(malware_filtered, "malware")
    benign_error_count, benign_error_paths, benign_normal, benign_missing = analyze_error_files(benign_filtered, "benign")
    
    # 打印总结
    print(f"\n{'='*80}")
    print("最终统计总结")
    print(f"{'='*80}")
    
    print(f"\n【目录结构统计】")
    print(f"  Malware包名文件夹: {malware_pkg_count}")
    print(f"  Malware版本文件夹: {malware_ver_count}")
    print(f"  Benign包名文件夹: {benign_pkg_count}")
    print(f"  Benign版本文件夹: {benign_ver_count}")
    print(f"  总包名文件夹: {malware_pkg_count + benign_pkg_count}")
    print(f"  总版本文件夹: {malware_ver_count + benign_ver_count}")
    
    print(f"\n【过滤后统计】")
    print(f"  Malware过滤前: {malware_ver_count}, 跳过: {malware_skipped}, 过滤后: {len(malware_filtered)}")
    print(f"  Benign过滤前: {benign_ver_count}, 跳过: {benign_skipped}, 过滤后: {len(benign_filtered)}")
    print(f"  总过滤前: {malware_ver_count + benign_ver_count}")
    print(f"  总跳过: {malware_skipped + benign_skipped}")
    print(f"  总过滤后: {len(malware_filtered) + len(benign_filtered)}")
    
    print(f"\n【ERROR文件统计】")
    print(f"  Malware ERROR: {malware_error_count}/{len(malware_filtered)} ({malware_error_count/len(malware_filtered)*100 if malware_filtered else 0:.2f}%)")
    print(f"  Benign ERROR: {benign_error_count}/{len(benign_filtered)} ({benign_error_count/len(benign_filtered)*100 if benign_filtered else 0:.2f}%)")
    print(f"  总ERROR: {malware_error_count + benign_error_count}/{len(malware_filtered) + len(benign_filtered)} ({(malware_error_count + benign_error_count)/(len(malware_filtered) + len(benign_filtered))*100 if (malware_filtered or benign_filtered) else 0:.2f}%)")
    
    print(f"\n【文件状态统计】")
    print(f"  Malware - 正常: {malware_normal}, ERROR: {malware_error_count}, 缺失: {malware_missing}")
    print(f"  Benign - 正常: {benign_normal}, ERROR: {benign_error_count}, 缺失: {benign_missing}")
    
    # 保存详细报告
    save_error_report(malware_error_paths, benign_error_paths)

if __name__ == "__main__":
    main()
