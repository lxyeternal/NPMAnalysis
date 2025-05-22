import os
import re
from collections import defaultdict

# 定义路径
SOURCE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/guarddog/malware"

def analyze_txt_file(txt_path):
    """分析单个txt文件，检查其中的恶意行为类型"""
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 检查是否为良性代码
        if "Found 0 potentially malicious indicators" in content or "benign" in content.lower():
            return "benign", []
        
        # 提取所有恶意行为类型
        behavior_types = []
        
        # 查找所有类型描述行
        matches = re.findall(r'^([\w\-]+): found (\d+) .* matches', content, re.MULTILINE)
        
        for behavior_type, count_str in matches:
            behavior_types.append(behavior_type)
        
        # 如果只有一种恶意行为类型，且是npm-install-script
        if len(behavior_types) == 1 and behavior_types[0] == "npm-install-script":
            # 检查是否只涉及package.json文件
            file_matches = re.findall(r'\*.*?\s+at\s+([\w\-\.\/]+(?:\.js|\.json|\.py|\.ts)):(\d+)', content)
            json_only = all(path.endswith('package.json') for path, _ in file_matches)
            
            if json_only:
                return "npm-install-script-only", file_matches
            else:
                return "npm-install-script-mixed", file_matches
        
        return "mixed", behavior_types
        
    except Exception as e:
        print(f"分析文件 {txt_path} 时出错: {e}")
        return "error", []

def main():
    """主函数，统计所有txt文件中的恶意行为类型"""
    # 结果统计
    stats = {
        "total": 0,
        "benign": 0,
        "npm-install-script-only": 0,
        "npm-install-script-mixed": 0,
        "mixed": 0,
        "error": 0
    }
    
    # 按类型收集包名
    packages_by_type = defaultdict(list)
    
    # 遍历所有txt文件
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith('.txt'):
                stats["total"] += 1
                txt_path = os.path.join(root, file)
                
                # 提取包名和版本
                parts = txt_path.split('/')
                if len(parts) >= 3:
                    package_name = parts[-3]
                    version = parts[-2]
                    package_info = f"{package_name}@{version}"
                else:
                    package_info = txt_path
                
                # 分析文件
                result_type, details = analyze_txt_file(txt_path)
                stats[result_type] += 1
                packages_by_type[result_type].append(package_info)
                
                # 每100个文件打印一次进度
                if stats["total"] % 100 == 0:
                    print(f"已处理 {stats['total']} 个文件...")
    
    # 打印统计结果
    print("\n=== 统计结果 ===")
    print(f"总文件数: {stats['total']}")
    print(f"良性文件数: {stats['benign']}")
    print(f"只有npm-install-script且只在package.json中的文件数: {stats['npm-install-script-only']}")
    print(f"只有npm-install-script但在多种文件中的文件数: {stats['npm-install-script-mixed']}")
    print(f"有多种恶意行为类型的文件数: {stats['mixed']}")
    print(f"处理出错的文件数: {stats['error']}")
    
    # 保存详细结果到文件
    with open("npm_install_script_stats.txt", "w", encoding="utf-8") as f:
        f.write("=== 统计结果 ===\n")
        f.write(f"总文件数: {stats['total']}\n")
        f.write(f"良性文件数: {stats['benign']}\n")
        f.write(f"只有npm-install-script且只在package.json中的文件数: {stats['npm-install-script-only']}\n")
        f.write(f"只有npm-install-script但在多种文件中的文件数: {stats['npm-install-script-mixed']}\n")
        f.write(f"有多种恶意行为类型的文件数: {stats['mixed']}\n")
        f.write(f"处理出错的文件数: {stats['error']}\n\n")
        
        f.write("=== 只有npm-install-script且只在package.json中的包 ===\n")
        for package in sorted(packages_by_type["npm-install-script-only"]):
            f.write(f"{package}\n")
        
        f.write("\n=== 只有npm-install-script但在多种文件中的包 ===\n")
        for package in sorted(packages_by_type["npm-install-script-mixed"]):
            f.write(f"{package}\n")
    
    print(f"\n详细结果已保存到 npm_install_script_stats.txt")

if __name__ == "__main__":
    main() 