#!/usr/bin/env python3
import os
import json
from collections import defaultdict

# 设置根目录
root_dir = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/package_label"

# 统计变量
malicious_count = 0
benign_count = 0

# 包版本统计
package_stats = defaultdict(lambda: {"malicious": 0, "benign": 0, "versions": []})

# 遍历 package_label 目录
for package_name in os.listdir(root_dir):
    package_path = os.path.join(root_dir, package_name)
    
    # 跳过非目录和特殊文件
    if not os.path.isdir(package_path) or package_name.startswith('.'):
        continue
    
    # 遍历版本目录
    for version in os.listdir(package_path):
        version_path = os.path.join(package_path, version)
        
        if not os.path.isdir(version_path):
            continue
        
        # 寻找分析文件 (通常是 package_name-version-analysis.json)
        analysis_file = f"{package_name}-{version}-analysis.json"
        analysis_path = os.path.join(version_path, analysis_file)
        
        if not os.path.exists(analysis_path):
            # 尝试其他可能的文件命名
            json_files = [f for f in os.listdir(version_path) if f.endswith('.json')]
            if json_files:
                analysis_path = os.path.join(version_path, json_files[0])
            else:
                print(f"警告: 找不到 {version_path} 的分析文件")
                continue
        
        # 读取分析文件
        try:
            with open(analysis_path, 'r') as f:
                data = json.load(f)
            
            # 检查是否为恶意包
            if "malicious_files" in data and len(data["malicious_files"]) > 0:
                malicious_count += 1
                package_stats[package_name]["malicious"] += 1
                package_stats[package_name]["versions"].append({"version": version, "type": "malicious"})
            else:
                benign_count += 1
                package_stats[package_name]["benign"] += 1
                package_stats[package_name]["versions"].append({"version": version, "type": "benign"})
                
        except Exception as e:
            print(f"错误: 处理 {analysis_path} 时出现问题: {e}")

# 输出统计结果
print("="*50)
print(f"总共扫描到 {malicious_count + benign_count} 个包版本")
print(f"恶意包版本数量: {malicious_count}")
print(f"良性包版本数量: {benign_count}")
print("="*50)

# 输出每个包的统计信息
print("包级别统计:")
for pkg_name, stats in sorted(package_stats.items(), 
                             key=lambda x: x[1]["malicious"], 
                             reverse=True):
    total = stats["malicious"] + stats["benign"]
    if total > 0:
        print(f"{pkg_name}: 总版本 {total}, 恶意版本 {stats['malicious']}, 良性版本 {stats['benign']}")

# 保存详细统计结果到文件
output_file = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/package_stats.json"
with open(output_file, 'w') as f:
    json.dump({
        "summary": {
            "total_versions": malicious_count + benign_count,
            "malicious_versions": malicious_count,
            "benign_versions": benign_count
        },
        "package_stats": package_stats
    }, f, indent=2)

print(f"\n详细统计结果已保存到: {output_file}") 