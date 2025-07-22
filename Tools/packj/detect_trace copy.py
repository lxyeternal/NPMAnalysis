#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path

# 定义源目录和目标目录
MALWARE_SOURCE_DIR = "/tmp/malicious_package/unzip_malware"
BENIGN_SOURCE_DIR = "/tmp/malicious_package/unzip_benign"
MALWARE_TARGET_DIR = "/home2/mynames/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace/malware"
BENIGN_TARGET_DIR = "/home2/mynames/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace/benign"
DOMAIN_PACKAGE_DIR = "/tmp/domain_package"

def find_package_json_dir(start_path):
    """
    递归查找包含package.json的目录，返回最浅的包含package.json的目录
    """
    min_depth = float('inf')
    package_dir = None
    
    for root, dirs, files in os.walk(start_path):
        if 'package.json' in files:
            # 计算相对于起始路径的深度
            rel_path = os.path.relpath(root, start_path)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth < min_depth:
                min_depth = depth
                package_dir = root
    
    return package_dir

def extract_package_info(package_path, source_base_dir):
    """
    从路径中提取包名和版本
    格式: /tmp/malicious_package/unzip_benign/包名/版本/package...
    """
    # 移除基础路径部分
    rel_path = package_path.replace(source_base_dir, '').lstrip('/')
    path_parts = rel_path.split('/')
    
    # 第一部分是包名，第二部分是版本
    if len(path_parts) >= 2:
        package_name = path_parts[0]
        version = path_parts[1]
        return package_name, version
    else:
        # 如果路径格式不符合预期，使用目录名
        return os.path.basename(os.path.dirname(package_path)), "unknown"

def is_already_analyzed(package_name, version, target_base_dir):
    """
    检查包是否已经分析过
    """
    result_file = os.path.join(target_base_dir, package_name, version, "result.txt")
    if os.path.exists(result_file):
        # 检查文件是否有内容
        if os.path.getsize(result_file) > 0:
            return True
    return False

def process_domain_package(package_path, package_name, version, is_malware):
    """
    处理作用域包（以@开头且包含##的包名）
    将其转换为标准npm作用域包结构并复制到/tmp/domain_package目录
    """
    original_package_name = package_name  # 保存原始包名，用于结果保存
    
    if package_name.startswith('@') and '##' in package_name:
        # 分割包名，将@sxmp##detector转换为@sxmp/detector
        scope, name = package_name.split('##', 1)
        standard_package_name = f"{scope}/{name}"
        
        # 构建新路径，保持原始路径结构，只替换包名和基础目录
        # 从package_path中提取相对路径部分
        if is_malware:
            rel_path = package_path.replace(MALWARE_SOURCE_DIR, "").lstrip('/')
        else:
            rel_path = package_path.replace(BENIGN_SOURCE_DIR, "").lstrip('/')
        
        # 替换路径中的包名部分（将##替换为/）
        rel_path_parts = rel_path.split('/')
        if len(rel_path_parts) > 0:
            rel_path_parts[0] = rel_path_parts[0].replace('##', '/')
        rel_path = '/'.join(rel_path_parts)
        
        # 确定源目录类型（unzip_malware或unzip_benign）
        source_type = "unzip_malware" if is_malware else "unzip_benign"
        
        # 构建新路径
        target_path = os.path.join(DOMAIN_PACKAGE_DIR, source_type, rel_path)
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True)
        
        # 检查目标路径是否已存在
        if os.path.exists(target_path):
            print(f"目标路径已存在: {target_path}")
            # 不尝试删除现有文件，直接使用现有路径
        else:
            # 复制文件/目录
            try:
                if os.path.isdir(package_path):
                    shutil.copytree(package_path, target_path)
                else:
                    shutil.copy2(package_path, target_path)
                print(f"已将 {package_name} 转换为标准作用域包结构: {standard_package_name}")
            except PermissionError as e:
                print(f"权限错误，无法复制文件: {str(e)}")
                # 如果无法复制，但目标路径已存在，仍然继续使用该路径
            except Exception as e:
                print(f"复制文件时出错: {str(e)}")
                # 如果出现其他错误，仍然尝试使用该路径
        
        # 返回新路径用于分析，但保留原始包名用于结果保存
        return target_path, standard_package_name, original_package_name
    
    return package_path, package_name, original_package_name

def run_packj_analysis(package_path, is_malware, source_base_dir):
    """
    运行packj分析并保存结果
    """
    # 提取包名和版本
    package_name, version = extract_package_info(package_path, source_base_dir)
    
    # 确定目标目录
    target_base_dir = MALWARE_TARGET_DIR if is_malware else BENIGN_TARGET_DIR
    
    # 使用包名/版本的目录结构
    result_dir_path = os.path.join(target_base_dir, package_name, version)
    
    # 检查是否已经分析过
    result_file = os.path.join(result_dir_path, "result.txt")
    if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
        print(f"跳过已分析的包: {package_name}/{version}")
        return True
    
    # 处理作用域包
    analysis_path, display_name, result_name = process_domain_package(package_path, package_name, version, is_malware)
    
    # 使用原始包名/版本创建结果目录
    target_dir = os.path.join(target_base_dir, result_name, version)
    os.makedirs(target_dir, exist_ok=True)
    
    # 打印原始路径，帮助调试
    print(f"原始路径: {package_path}")
    print(f"处理后路径: {analysis_path}")
    
    # 修改路径格式，添加/tmp/packj前缀，只替换路径最前面的/tmp
    if DOMAIN_PACKAGE_DIR in analysis_path:
        # 对于已经处理过的作用域包，使用新路径
        # 只替换路径开头的/tmp，而不是所有出现的/tmp
        if analysis_path.startswith('/tmp/'):
            docker_path = '/tmp/packj' + analysis_path[4:]
        else:
            docker_path = analysis_path
    else:
        # 对于普通包，使用原路径
        docker_path = package_path.replace("/tmp/malicious_package", "/tmp/packj/malicious_package")
        docker_path = docker_path.replace("/tmp/malicious_packagee", "/tmp/packj/malicious_package")  # 修复可能的拼写错误
    
    # 打印Docker路径，帮助调试
    print(f"Docker路径: {docker_path}")
    
    # 运行docker命令
    cmd = f"docker exec -u ubuntu -it packj-dev python3 main.py audit -t -p local_nodejs:{docker_path}"
    print(f"执行Docker命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # 保存结果到文件
        result_file = os.path.join(target_dir, "result.txt")
        with open(result_file, 'w') as f:
            f.write(result.stdout)
        
        print(f"分析完成: {result_name}/{version}, 结果保存到 {result_file}")
        return True
    except Exception as e:
        print(f"分析失败: {analysis_path}, 错误: {str(e)}")
        return False

def process_directory(source_dir, is_malware):
    """
    处理指定目录下的所有包
    """
    # 获取一级目录（包名）
    package_dirs = [os.path.join(source_dir, d) for d in os.listdir(source_dir) 
                   if os.path.isdir(os.path.join(source_dir, d))]
    
    for package_dir in package_dirs:
        # 查找包含package.json的最浅目录
        package_json_dir = find_package_json_dir(package_dir)
        
        if package_json_dir:
            print(f"找到package.json目录: {package_json_dir}")
            run_packj_analysis(package_json_dir, is_malware, source_dir)
        else:
            print(f"未找到package.json: {package_dir}")

def main():
    """
    主函数
    """
    print("开始处理恶意包...")
    if os.path.exists(MALWARE_SOURCE_DIR):
        process_directory(MALWARE_SOURCE_DIR, True)
    else:
        print(f"目录不存在: {MALWARE_SOURCE_DIR}")
    
    print("\n开始处理良性包...")
    if os.path.exists(BENIGN_SOURCE_DIR):
        process_directory(BENIGN_SOURCE_DIR, False)
    else:
        print(f"目录不存在: {BENIGN_SOURCE_DIR}")

if __name__ == "__main__":
    # 确保目标目录存在
    os.makedirs(MALWARE_TARGET_DIR, exist_ok=True)
    os.makedirs(BENIGN_TARGET_DIR, exist_ok=True)
    os.makedirs(DOMAIN_PACKAGE_DIR, exist_ok=True)
    
    main()
