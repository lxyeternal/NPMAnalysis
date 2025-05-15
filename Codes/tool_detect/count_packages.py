#!/usr/bin/env python3
import os
import re
from collections import defaultdict

# 基本路径
base_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output"

# 存储结果的字典
results = {}

# 遍历所有工具目录
for tool in os.listdir(base_path):
    tool_path = os.path.join(base_path, tool)
    if not os.path.isdir(tool_path):
        continue
    
    results[tool] = {}
    
    # 对packj的特殊处理
    if tool == 'packj':
        for mode in ['result_static', 'result_trace']:
            mode_path = os.path.join(tool_path, mode)
            if not os.path.isdir(mode_path):
                continue
                
            results[tool][mode] = {}
            
            # 处理benign和malware
            for category in ['benign', 'malware']:
                category_path = os.path.join(mode_path, category)
                if not os.path.isdir(category_path):
                    continue
                
                # 收集包名和版本
                packages = defaultdict(set)
                total_versions = 0
                for pkg_dir in os.listdir(category_path):
                    if os.path.isdir(os.path.join(category_path, pkg_dir)):
                        # 提取包名和版本
                        match = re.match(r'(.+)-(\d+\.\d+\.\d+.*)', pkg_dir)
                        if match:
                            pkg_name, version = match.groups()
                            packages[pkg_name].add(version)
                            total_versions += 1
                        else:
                            packages[pkg_dir].add("unknown")
                            total_versions += 1
                
                results[tool][mode][category] = {
                    "package_count": len(packages),
                    "version_count": total_versions,
                    "packages": {pkg: list(versions) for pkg, versions in packages.items()}
                }
    else:
        # 处理其他工具的benign和malware
        for category in ['benign', 'malware']:
            category_path = os.path.join(tool_path, category)
            if not os.path.isdir(category_path):
                continue
            
            # 收集包名和版本
            packages = defaultdict(set)
            total_versions = 0
            for pkg_dir in os.listdir(category_path):
                pkg_path = os.path.join(category_path, pkg_dir)
                if os.path.isdir(pkg_path):
                    for version_dir in os.listdir(pkg_path):
                        version_path = os.path.join(pkg_path, version_dir)
                        if os.path.isdir(version_path):
                            packages[pkg_dir].add(version_dir)
                            total_versions += 1
            
            results[tool][category] = {
                "package_count": len(packages),
                "version_count": total_versions,
                "packages": {pkg: list(versions) for pkg, versions in packages.items()}
            }

# 分析结果，检查每个工具的benign和malware是否包含相同的包
summary = {}

for tool, tool_data in results.items():
    summary[tool] = {}
    
    if tool == 'packj':
        for mode in tool_data:
            benign_data = tool_data[mode].get('benign', {})
            malware_data = tool_data[mode].get('malware', {})
            
            benign_pkgs = set(benign_data.get('packages', {}).keys())
            malware_pkgs = set(malware_data.get('packages', {}).keys())
            
            benign_versions = benign_data.get('version_count', 0)
            malware_versions = malware_data.get('version_count', 0)
            
            summary[tool][mode] = {
                "benign_package_count": len(benign_pkgs),
                "benign_version_count": benign_versions,
                "malware_package_count": len(malware_pkgs),
                "malware_version_count": malware_versions,
                "common_package_count": len(benign_pkgs.intersection(malware_pkgs)),
                "benign_only_packages": len(benign_pkgs - malware_pkgs),
                "malware_only_packages": len(malware_pkgs - benign_pkgs),
                "is_consistent": benign_pkgs == malware_pkgs
            }
    else:
        benign_data = tool_data.get('benign', {})
        malware_data = tool_data.get('malware', {})
        
        benign_pkgs = set(benign_data.get('packages', {}).keys())
        malware_pkgs = set(malware_data.get('packages', {}).keys())
        
        benign_versions = benign_data.get('version_count', 0)
        malware_versions = malware_data.get('version_count', 0)
        
        summary[tool] = {
            "benign_package_count": len(benign_pkgs),
            "benign_version_count": benign_versions,
            "malware_package_count": len(malware_pkgs),
            "malware_version_count": malware_versions,
            "common_package_count": len(benign_pkgs.intersection(malware_pkgs)),
            "benign_only_packages": len(benign_pkgs - malware_pkgs),
            "malware_only_packages": len(malware_pkgs - benign_pkgs),
            "is_consistent": benign_pkgs == malware_pkgs
        }

# 打印摘要信息
print("工具包版本一致性分析摘要:")
print("-" * 50)
for tool, tool_summary in summary.items():
    print(f"\n工具: {tool}")
    
    if tool == 'packj':
        for mode, mode_summary in tool_summary.items():
            print(f"  模式: {mode}")
            print(f"    良性包数量: {mode_summary['benign_package_count']}")
            print(f"    良性版本数量: {mode_summary['benign_version_count']}")
            print(f"    恶意包数量: {mode_summary['malware_package_count']}")
            print(f"    恶意版本数量: {mode_summary['malware_version_count']}")
            print(f"    共同包数量: {mode_summary['common_package_count']}")
            print(f"    仅在良性中的包: {mode_summary['benign_only_packages']}")
            print(f"    仅在恶意中的包: {mode_summary['malware_only_packages']}")
            print(f"    是否一致: {mode_summary['is_consistent']}")
    else:
        print(f"  良性包数量: {tool_summary['benign_package_count']}")
        print(f"  良性版本数量: {tool_summary['benign_version_count']}")
        print(f"  恶意包数量: {tool_summary['malware_package_count']}")
        print(f"  恶意版本数量: {tool_summary['malware_version_count']}")
        print(f"  共同包数量: {tool_summary['common_package_count']}")
        print(f"  仅在良性中的包: {tool_summary['benign_only_packages']}")
        print(f"  仅在恶意中的包: {tool_summary['malware_only_packages']}")
        print(f"  是否一致: {tool_summary['is_consistent']}") 