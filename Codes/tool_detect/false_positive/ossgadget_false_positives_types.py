import os
import re
from collections import defaultdict

def load_selected_packages(file_path):
    """
    加载selected_benign_packages.txt文件中的包名和版本
    返回一个集合，包含"包名/版本"格式的字符串
    """
    selected_packages = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    selected_packages.add(line)
        return selected_packages
    except Exception as e:
        print(f"Error loading selected packages: {e}")
        return set()

def extract_detection_types(file_path):
    """提取ossgadget检测文件中的检测类型，处理ANSI颜色代码"""
    detection_types = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # 匹配Tag行，例如: "Tag: [34mSecurity.Backdoor.LOLBAS.Linux[0m"
            # 使用正则表达式处理ANSI颜色代码
            tags = re.findall(r'Tag: \x1B\[34m(.*?)\x1B\[0m', content)
            
            # 收集所有标签
            for tag in tags:
                detection_types.add(tag)
                
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        
    return detection_types

def find_txt_files(directory):
    """递归查找目录中的所有txt文件"""
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                txt_files.append(os.path.join(root, file))
    return txt_files

def extract_package_info(file_path):
    """
    从文件路径中提取包名和版本信息
    预期格式: .../benign/包名/版本/文件.txt
    使用os.listdir逐层查找
    """
    # 获取文件所在目录
    dir_path = os.path.dirname(file_path)
    
    # 获取文件所在目录的父目录（版本目录）
    version_dir = os.path.dirname(dir_path)
    if not os.path.exists(version_dir):
        return os.path.basename(file_path).replace(".txt", ""), "unknown"
    
    version = os.path.basename(version_dir)
    
    # 获取包名目录（版本目录的父目录）
    package_dir = os.path.dirname(version_dir)
    if not os.path.exists(package_dir):
        return os.path.basename(file_path).replace(".txt", ""), version
    
    package_name = os.path.basename(package_dir)
    
    # 检查父目录是否为benign目录
    benign_dir = os.path.dirname(package_dir)
    if os.path.basename(benign_dir) != "benign":
        return os.path.basename(file_path).replace(".txt", ""), "unknown"
    
    return package_name, version

def main():
    # 设置输出文件路径
    output_file = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/false_positive/ossgadget_false_positives_types.txt"
    
    # 设置benign样本文件夹路径
    benign_folder = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/ossgadget/benign"
    
    # 加载需要跳过的包列表
    selected_packages_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"
    selected_packages = load_selected_packages(selected_packages_path)
    print(f"加载了 {len(selected_packages)} 个需要跳过的包")
    
    # 用于存储每种检测类型的文件列表
    type_to_files = defaultdict(list)
    
    # 用于统计每种检测类型的数量
    type_counts = defaultdict(int)
    
    # 按包名和版本统计假阳性
    package_version_counts = defaultdict(lambda: defaultdict(list))
    
    # 存储所有假阳性文件及其检测类型
    false_positives = []
    
    # 记录跳过的包数量
    skipped_count = 0
    
    # 递归查找所有txt文件
    txt_files = find_txt_files(benign_folder)
    total_files = len(txt_files)
    files_with_detections = 0
    
    print(f"开始分析目录: {benign_folder}")
    print(f"找到 {total_files} 个txt文件")
    
    # 遍历所有找到的txt文件
    for i, file_path in enumerate(txt_files):
        # 获取包名和版本
        package_name, version = extract_package_info(file_path)
        
        # 检查是否在跳过列表中
        for selected_package in selected_packages:
            if selected_package in file_path:
                print(f"跳过了 {selected_package} 包")
                skipped_count += 1
                break
        else:  # 如果没有匹配到需要跳过的包，则继续处理
            # 获取该文件中的检测类型
            detection_types = extract_detection_types(file_path)
            
            # 更新统计信息
            if detection_types:
                files_with_detections += 1
                false_positives.append((file_path, detection_types, package_name, version))
                
                for detection_type in detection_types:
                    type_to_files[detection_type].append(file_path)
                    type_counts[detection_type] += 1
                    
                # 更新包名和版本统计
                package_version_counts[package_name][version].append((file_path, detection_types))
        
        if (i + 1) % 100 == 0:
            print(f"已处理 {i + 1}/{total_files} 个文件...")
    
    print(f"\n分析完成，共处理 {total_files} 个文件")
    print(f"跳过了 {skipped_count} 个selected_benign_packages中的包")
    print(f"发现 {files_with_detections} 个文件含有误报")
    print(f"发现 {len(type_counts)} 种不同的检测类型")
    
    # 将结果写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("OSSGadget误报类型统计\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"总共分析的良性样本文件数: {total_files - skipped_count}\n")
        f.write(f"跳过了 {skipped_count} 个selected_benign_packages中的包\n")
        f.write(f"含有误报的文件数: {files_with_detections} ({(files_with_detections/(total_files-skipped_count))*100:.2f}%)\n\n")
        
        f.write("各类型误报统计:\n")
        f.write("-" * 30 + "\n")
        for detection_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / files_with_detections) * 100 if files_with_detections > 0 else 0
            f.write(f"{detection_type}: {count} 个文件 ({percentage:.2f}%)\n")
        
        # 按包名和版本统计
        f.write("\n\n按包名和版本统计：\n")
        f.write("=" * 30 + "\n")
        for package_name, versions in sorted(package_version_counts.items()):
            f.write(f"\n## 包名: {package_name} (共 {sum(len(v) for v in versions.values())} 个假阳性)\n")
            for version, files_info in sorted(versions.items()):
                f.write(f"  - 版本 {version}: {len(files_info)} 个假阳性\n")
                for file_path, detection_types in files_info:
                    f.write(f"    * {file_path} - 检测类型: {', '.join(detection_types)}\n")
        
        f.write("\n详细文件列表:\n")
        f.write("=" * 50 + "\n\n")
        for detection_type, files in sorted(type_to_files.items(), key=lambda x: len(x[1]), reverse=True):
            f.write(f"\n{detection_type}类型的文件:\n")
            f.write("-" * 30 + "\n")
            for file_path in files:
                package_name, version = extract_package_info(file_path)
                f.write(f"{package_name} ({version}) - {file_path}\n")
            f.write(f"共 {len(files)} 个文件\n")
    
    print(f"结果已保存到: {output_file}")

if __name__ == "__main__":
    main()