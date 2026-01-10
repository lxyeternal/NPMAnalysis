#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path
import multiprocessing
import time
import random
import argparse
import sys
from datetime import datetime

# 定义源目录和目标目录
MALWARE_SOURCE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
BENIGN_SOURCE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign"
MALWARE_TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/packj/result_trace/malware-1"
BENIGN_TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/packj/result_trace/benign-1"
DOMAIN_PACKAGE_DIR = "/tmp/domain_package"

# Docker容器配置
DOCKER_CONTAINER_PREFIX = "packj-dev-"
NUM_DOCKER_CONTAINERS = 16  # 默认Docker容器数量，可通过命令行参数修改
DOCKER_IMAGE = "ossillate/packj:latest"
HOST_PM_UTIL_PATH = "/home2/wenbo/Documents/NPMAnalysis/Tools/packj/packj/audit/pm_util.py"
CONTAINER_PM_UTIL_PATH = "/home/ubuntu/packj/packj/audit/pm_util.py"

# 错误包列表文件路径 (datacopy格式: category\tpackage_name\tversion)
ERROR_PACKAGES_FILE = "/home2/wenbo/Documents/NPMAnalysis/trace_error_packages_list.txt"

# Docker容器内的包目录
DOCKER_DOMAIN_PACKAGE_DIR = "/tmp/packj/domain_package"

# 创建一个全局锁，用于同步输出
print_lock = multiprocessing.Lock()

def synchronized_print(*args, **kwargs):
    """
    线程安全的打印函数，避免输出混乱
    """
    with print_lock:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}]", *args, **kwargs)
        sys.stdout.flush()  # 确保立即输出

def load_error_packages():
    """
    从错误包列表文件中加载需要分析的包名和版本
    返回一个集合，包含所有的 "包名/版本" 字符串
    """
    error_packages = set()

    if not os.path.exists(ERROR_PACKAGES_FILE):
        synchronized_print(f"错误：找不到错误包列表文件: {ERROR_PACKAGES_FILE}")
        return error_packages

    with open(ERROR_PACKAGES_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and '/' in line:
                error_packages.add(line)

    synchronized_print(f"已加载 {len(error_packages)} 个错误包")
    return error_packages

def load_error_packages_datacopy():
    """
    从datacopy格式的错误包列表文件中加载包信息
    格式: category\tpackage_name\tversion
    返回一个列表，每个元素为 (category, package_name, version)
    """
    packages = []

    if not os.path.exists(ERROR_PACKAGES_FILE):
        synchronized_print(f"错误：找不到错误包列表文件: {ERROR_PACKAGES_FILE}")
        return packages

    with open(ERROR_PACKAGES_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 3:
                category, package_name, version = parts[0], parts[1], parts[2]
                packages.append((category, package_name, version))

    synchronized_print(f"已加载 {len(packages)} 个错误包")
    return packages

def find_shallowest_package_json(start_path):
    """
    在指定目录中查找最浅层的package.json文件
    返回package.json所在的目录路径
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

def build_docker_path(category, package_name, version):
    """
    构建Docker容器内的包路径
    将 ## 替换为 / 以支持作用域包
    并找到最浅层的package.json所在目录
    """
    # 替换 ## 为 /
    host_package_name = package_name.replace('##', '/')

    # 构建宿主机路径 (用于查找package.json)
    host_base_path = f"/tmp/domain_package/{category}/{host_package_name}/{version}"

    # 查找最浅层的package.json所在目录
    package_json_dir = find_shallowest_package_json(host_base_path)

    if package_json_dir:
        # 计算相对于host_base_path的相对路径
        rel_path = os.path.relpath(package_json_dir, host_base_path)
        if rel_path == '.':
            # package.json就在根目录
            docker_path = f"{DOCKER_DOMAIN_PACKAGE_DIR}/{category}/{host_package_name}/{version}"
        else:
            # package.json在子目录中
            docker_path = f"{DOCKER_DOMAIN_PACKAGE_DIR}/{category}/{host_package_name}/{version}/{rel_path}"
        synchronized_print(f"找到package.json目录: {package_json_dir} -> Docker路径: {docker_path}")
        return docker_path
    else:
        # 找不到package.json，返回基础路径
        synchronized_print(f"警告: 在 {host_base_path} 中未找到package.json")
        docker_path = f"{DOCKER_DOMAIN_PACKAGE_DIR}/{category}/{host_package_name}/{version}"
        return docker_path

def run_packj_analysis_simple(docker_path, category, package_name, version, docker_container, timeout_seconds=180):
    """
    简化版的packj分析函数
    直接使用Docker路径进行分析

    Args:
        docker_path: Docker容器内的包路径
        category: 类别 (unzip_benign 或 unzip_malware)
        package_name: 包名 (原始格式，用于保存结果)
        version: 版本
        docker_container: Docker容器名称
        timeout_seconds: 超时时间（秒）
    """
    # 确定是否为恶意包
    is_malware = "malware" in category

    # 确定目标目录
    target_base_dir = MALWARE_TARGET_DIR if is_malware else BENIGN_TARGET_DIR

    # 使用原始包名/版本创建结果目录
    target_dir = os.path.join(target_base_dir, package_name, version)

    # 检查是否已经分析过
    result_file = os.path.join(target_dir, "result.txt")
    if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
        with open(result_file, 'r') as f:
            content = f.read()
            if not content.startswith("ERROR:"):
                synchronized_print(f"[{docker_container}] 跳过已成功分析的包: {package_name}/{version}")
                return True

    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        synchronized_print(f"[{docker_container}] 创建结果目录失败: {str(e)}")
        return False

    # 打印调试信息
    synchronized_print(f"[{docker_container}] 分析包: {package_name}/{version}")
    synchronized_print(f"[{docker_container}] Docker路径: {docker_path}")

    # 运行docker命令
    cmd = f"docker exec -u ubuntu -it {docker_container} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:{docker_path}"
    synchronized_print(f"[{docker_container}] 执行命令: {cmd}")

    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            stdout, stderr = process.communicate(timeout=timeout_seconds)

            # 保存结果到文件
            with open(result_file, 'w') as f:
                f.write(stdout)

            synchronized_print(f"[{docker_container}] 分析完成: {package_name}/{version}, 结果保存到 {result_file}")
            synchronized_print("-" * 80)
            return True

        except subprocess.TimeoutExpired:
            process.kill()

            # 清理可能残留的进程
            cleanup_cmd = f"docker exec {docker_container} pkill -f 'python3 /home/ubuntu/packj/main.py'"
            subprocess.run(cleanup_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            timeout_msg = f"分析超时（{timeout_seconds}秒）"
            synchronized_print(f"[{docker_container}] {timeout_msg}: {package_name}/{version}")

            with open(result_file, 'w') as f:
                f.write(f"ERROR: {timeout_msg}")

            synchronized_print("-" * 80)
            return False

    except Exception as e:
        synchronized_print(f"[{docker_container}] 分析失败: {package_name}/{version}, 错误: {str(e)}")
        synchronized_print("-" * 80)
        return False

def should_analyze_package(package_name, version, error_packages):
    """
    检查包是否在错误包列表中，需要重新分析
    """
    package_key = f"{package_name}/{version}"
    return package_key in error_packages

def build_package_path_from_error_list(package_name, version, is_malware):
    """
    根据包名和版本直接构建包路径，并复制到/tmp目录
    
    Args:
        package_name: 包名
        version: 版本
        is_malware: 是否为恶意包
    
    Returns:
        复制后的包路径，如果失败则返回None
    """
    # 构建源路径: base路径/包名/版本
    source_base_dir = MALWARE_SOURCE_DIR if is_malware else BENIGN_SOURCE_DIR
    source_path = os.path.join(source_base_dir, package_name, version)
    
    synchronized_print(f"构建源路径: {source_path}")
    
    # 检查源路径是否存在
    if not os.path.exists(source_path):
        synchronized_print(f"错误：源路径不存在: {source_path}")
        return None
    
    # 查找package.json目录
    package_json_dir = find_package_json_dir(source_path)
    if not package_json_dir:
        synchronized_print(f"错误：在 {source_path} 中未找到package.json")
        return None
    
    synchronized_print(f"找到package.json目录: {package_json_dir}")
    
    # 构建/tmp目录中的目标路径
    # 保持相同的目录结构：/tmp/error_packages/malware(或benign)/包名/版本/
    package_type = "malware" if is_malware else "benign"
    tmp_base_dir = f"/tmp/error_packages/{package_type}"
    tmp_target_path = os.path.join(tmp_base_dir, package_name, version)
    
    try:
        # 确保目标目录存在
        os.makedirs(tmp_target_path, exist_ok=True)
        
        # 复制package.json所在目录的内容到目标目录
        if os.path.exists(tmp_target_path):
            # 如果目标已存在，先删除
            shutil.rmtree(tmp_target_path)
        
        # 复制整个package.json目录
        shutil.copytree(package_json_dir, tmp_target_path)
        synchronized_print(f"成功复制包到: {tmp_target_path}")
        
        return tmp_target_path
        
    except Exception as e:
        synchronized_print(f"复制包时出错: {str(e)}")
        return None

class DockerManager:
    """
    Docker容器管理类，负责创建和准备Docker容器
    """
    def __init__(self, container_prefix=DOCKER_CONTAINER_PREFIX, num_containers=NUM_DOCKER_CONTAINERS):
        self.container_prefix = container_prefix
        self.num_containers = num_containers
        self.container_names = [f"{container_prefix}{i+1}" for i in range(num_containers)]
    
    def get_existing_containers(self):
        """
        获取所有以指定前缀开头的现有容器
        """
        cmd = f"docker ps -a --filter name={self.container_prefix} --format '{{{{.Names}}}}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        containers = result.stdout.strip().split('\n')
        return [c for c in containers if c]  # 过滤空行
    
    def remove_containers(self, containers):
        """
        删除指定的容器
        """
        if not containers:
            return
        
        synchronized_print(f"正在删除现有容器: {', '.join(containers)}")
        for container in containers:
            # 先停止容器（如果正在运行）
            stop_cmd = f"docker stop {container}"
            subprocess.run(stop_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 然后删除容器
            rm_cmd = f"docker rm {container}"
            subprocess.run(rm_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def create_containers(self):
        """
        创建指定数量的Docker容器
        """
        synchronized_print(f"正在创建 {self.num_containers} 个Docker容器...")
        for container_name in self.container_names:
            # 使用--entrypoint覆盖入口点，并运行tail命令保持容器运行
            # 添加卷挂载，将宿主机的/tmp目录挂载到容器的/tmp/packj目录
            cmd = f"docker run -d --name {container_name} --entrypoint '/bin/bash' -v /tmp:/tmp/packj {DOCKER_IMAGE} -c 'tail -f /dev/null'"
            synchronized_print(f"创建容器: {container_name} (挂载 /tmp -> /tmp/packj)")
            result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                synchronized_print(f"创建容器 {container_name} 失败: {result.stderr}")
            else:
                # 检查容器是否成功启动
                check_cmd = f"docker ps -q -f name={container_name}"
                check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
                if check_result.stdout.strip():
                    synchronized_print(f"容器 {container_name} 成功启动")
                    
                    # 设置容器内挂载目录的权限 - 第一条命令
                    chmod_cmd = f"docker exec -u 0 {container_name} chmod -R 777 /tmp/packj"
                    chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
                    if chmod_result.returncode == 0:
                        synchronized_print(f"容器 {container_name} 内的 /tmp/packj 权限设置成功")
                    else:
                        synchronized_print(f"容器 {container_name} 内的 /tmp/packj 权限设置失败: {chmod_result.stderr}")
                    
                    # 设置容器内 /tmp 目录的权限 - 第二条命令
                    chmod_cmd = f"docker exec -u 0 {container_name} chmod -R 777 /tmp"
                    chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
                    if chmod_result.returncode == 0:
                        synchronized_print(f"容器 {container_name} 内的 /tmp 权限设置成功")
                    else:
                        synchronized_print(f"容器 {container_name} 内的 /tmp 权限设置失败: {chmod_result.stderr}")
                    
                    # 设置容器内根目录的权限 - 第三条命令
                    chmod_cmd = f"docker exec -u 0 {container_name} chmod -R 777 /"
                    chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
                    if chmod_result.returncode == 0:
                        synchronized_print(f"容器 {container_name} 内的根目录权限设置成功")
                    else:
                        synchronized_print(f"容器 {container_name} 内的根目录权限设置失败: {chmod_result.stderr}")
                else:
                    synchronized_print(f"警告: 容器 {container_name} 可能未成功启动")

    def set_container_permissions(self):
        """
        设置容器内的权限
        """
        synchronized_print("正在设置容器权限...")
        
        for container_name in self.container_names:
            # 检查容器是否在运行
            check_cmd = f"docker ps -q -f name={container_name}"
            check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            if not check_result.stdout.strip():
                synchronized_print(f"警告: 容器 {container_name} 不存在或未运行，跳过权限设置")
                continue
            
            # 设置目录所有权
            chown_cmd = f"docker exec -u 0 -it {container_name} chown -R ubuntu:ubuntu /tmp/packj"
            synchronized_print(f"设置容器 {container_name} 的目录所有权: {chown_cmd}")
            chown_result = subprocess.run(chown_cmd, shell=True, stderr=subprocess.PIPE, text=True)
            
            if chown_result.returncode != 0:
                synchronized_print(f"设置容器 {container_name} 的目录所有权失败: {chown_result.stderr}")
            
            # 设置 /tmp/packj 目录权限 - 第一条命令
            chmod_cmd = f"docker exec -u 0 -it {container_name} chmod -R 777 /tmp/packj"
            synchronized_print(f"设置容器 {container_name} 的 /tmp/packj 目录权限: {chmod_cmd}")
            chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
            
            if chmod_result.returncode != 0:
                synchronized_print(f"设置容器 {container_name} 的 /tmp/packj 目录权限失败: {chmod_result.stderr}")
            
            # 设置 /tmp 目录权限 - 第二条命令
            chmod_cmd = f"docker exec -u 0 -it {container_name} chmod -R 777 /tmp"
            synchronized_print(f"设置容器 {container_name} 的 /tmp 目录权限: {chmod_cmd}")
            chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
            
            if chmod_result.returncode != 0:
                synchronized_print(f"设置容器 {container_name} 的 /tmp 目录权限失败: {chmod_result.stderr}")
            
            # 设置根目录权限 - 第三条命令
            chmod_cmd = f"docker exec -u 0 -it {container_name} chmod -R 777 /"
            synchronized_print(f"设置容器 {container_name} 的根目录权限: {chmod_cmd}")
            chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
            
            if chmod_result.returncode != 0:
                synchronized_print(f"设置容器 {container_name} 的根目录权限失败: {chmod_result.stderr}")
            else:
                synchronized_print(f"容器 {container_name} 的所有权限设置成功")

    def copy_files_to_containers(self):
        """
        将必要的文件复制到每个容器中
        """
        synchronized_print(f"正在将文件复制到容器...")
        for container_name in self.container_names:
            # 检查容器是否存在并运行
            check_cmd = f"docker ps -q -f name={container_name}"
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            if not result.stdout.strip():
                synchronized_print(f"警告: 容器 {container_name} 不存在或未运行，跳过文件复制")
                continue
            
            # 创建目标目录（如果不存在）
            mkdir_cmd = f"docker exec {container_name} mkdir -p /home/ubuntu/packj/packj/audit"
            subprocess.run(mkdir_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 复制文件到容器
            cp_cmd = f"docker cp {HOST_PM_UTIL_PATH} {container_name}:{CONTAINER_PM_UTIL_PATH}"
            synchronized_print(f"复制文件到 {container_name}: {cp_cmd}")
            result = subprocess.run(cp_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                synchronized_print(f"警告: 复制文件到容器 {container_name} 失败: {result.stderr}")
            else:
                synchronized_print(f"成功复制文件到容器 {container_name}")
    
    def setup_containers(self):
        """
        设置Docker容器：检查现有容器，删除旧容器，创建新容器，复制文件
        """
        synchronized_print("开始设置Docker容器...")
        
        # 检查现有容器
        existing_containers = self.get_existing_containers()
        if existing_containers:
            synchronized_print(f"发现现有容器: {', '.join(existing_containers)}")
            self.remove_containers(existing_containers)
        
        # 创建新容器
        self.create_containers()
        
        # 等待容器启动
        synchronized_print("等待容器启动...")
        time.sleep(2)
        
        # 设置容器权限
        self.set_container_permissions()
        
        # 复制文件到容器
        self.copy_files_to_containers()
        
        synchronized_print("Docker容器设置完成")
        return self.container_names

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
    检查包是否已经分析过（不包含ERROR的结果）
    """
    result_file = os.path.join(target_base_dir, package_name, version, "result.txt")
    if os.path.exists(result_file):
        # 检查文件是否有内容且不包含ERROR
        if os.path.getsize(result_file) > 0:
            with open(result_file, 'r') as f:
                content = f.read()
                if not content.startswith("ERROR:"):
                    return True
    return False

# 修改路径映射逻辑
def get_docker_path(host_path):
    """
    将宿主机路径转换为Docker容器内路径
    规则：
    1. /tmp/* -> /tmp/packj/*
    """
    if host_path.startswith('/tmp/'):
        return '/tmp/packj' + host_path[4:]
    return host_path

def process_domain_package(package_path, package_name, version, is_malware, container_name="unknown"):
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
        
        try:
            # 确保目录存在，但不设置权限
            os.makedirs(target_dir, exist_ok=True)
        except PermissionError:
            synchronized_print(f"[{container_name}] 权限错误: 无法创建目录 {target_dir}")
            # 跳过作用域包处理，直接使用原始路径
            synchronized_print(f"[{container_name}] 跳过作用域包处理，使用原始路径: {package_path}")
            return package_path, package_name, original_package_name
        except Exception as e:
            synchronized_print(f"[{container_name}] 创建目录失败: {str(e)}")
            return package_path, package_name, original_package_name
        
        # 检查目标路径是否已存在
        if os.path.exists(target_path):
            synchronized_print(f"[{container_name}] 目标路径已存在: {target_path}")
            # 不尝试删除现有文件，直接使用现有路径
        else:
            # 复制文件/目录
            try:
                if os.path.isdir(package_path):
                    shutil.copytree(package_path, target_path)
                else:
                    shutil.copy2(package_path, target_path)
                synchronized_print(f"[{container_name}] 已将 {package_name} 转换为标准作用域包结构: {standard_package_name}")
                # 不再设置复制后文件的权限
            except PermissionError as e:
                synchronized_print(f"[{container_name}] 权限错误，无法复制文件: {str(e)}")
                # 如果无法复制，使用原始路径
                synchronized_print(f"[{container_name}] 使用原始路径: {package_path}")
                return package_path, package_name, original_package_name
            except Exception as e:
                synchronized_print(f"[{container_name}] 复制文件时出错: {str(e)}")
                # 如果出现其他错误，使用原始路径
                return package_path, package_name, original_package_name
        
        # 返回新路径用于分析，但保留原始包名用于结果保存
        return target_path, standard_package_name, original_package_name
    
    return package_path, package_name, original_package_name

def run_packj_analysis(package_path, is_malware, source_base_dir, docker_container=None, timeout_seconds=180):
    """
    运行packj分析并保存结果
    
    Args:
        package_path: 包路径
        is_malware: 是否为恶意包
        source_base_dir: 源目录
        docker_container: Docker容器名称
        timeout_seconds: 超时时间（秒）
    """
    # 使用默认Docker容器名称如果未指定
    if docker_container is None:
        docker_container = "packj-dev"
        
    # 提取包名和版本
    package_name, version = extract_package_info(package_path, source_base_dir)
    
    # 确定目标目录
    target_base_dir = MALWARE_TARGET_DIR if is_malware else BENIGN_TARGET_DIR
    
    # 使用包名/版本的目录结构
    result_dir_path = os.path.join(target_base_dir, package_name, version)
    
    # 检查是否已经分析过（不包含ERROR的结果）
    result_file = os.path.join(result_dir_path, "result.txt")
    if is_already_analyzed(package_name, version, target_base_dir):
        synchronized_print(f"[{docker_container}] 跳过已成功分析的包: {package_name}/{version}")
        return True
    
    # 处理作用域包
    analysis_path, display_name, result_name = process_domain_package(package_path, package_name, version, is_malware, docker_container)
    
    # 使用原始包名/版本创建结果目录
    target_dir = os.path.join(target_base_dir, result_name, version)
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        synchronized_print(f"[{docker_container}] 创建结果目录失败: {str(e)}")
        return False
    
    # 打印原始路径，帮助调试
    synchronized_print(f"[{docker_container}] 原始路径: {package_path}")
    synchronized_print(f"[{docker_container}] 处理后路径: {analysis_path}")
    
    # 修改路径格式，将宿主机路径转换为Docker容器内路径
    docker_path = get_docker_path(analysis_path)
    
    # 打印Docker路径，帮助调试
    synchronized_print(f"[{docker_container}] Docker路径: {docker_path}")
    
    # 运行docker命令
    cmd = f"docker exec -u ubuntu -it {docker_container} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:{docker_path}"
    synchronized_print(f"[{docker_container}] 执行Docker命令: {cmd}")
    
    try:
        # 使用subprocess.Popen和超时机制
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        try:
            # 等待进程完成，设置超时
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            
            # 保存结果到文件
            result_file = os.path.join(target_dir, "result.txt")
            with open(result_file, 'w') as f:
                f.write(stdout)
            
            synchronized_print(f"[{docker_container}] 分析完成: {result_name}/{version}, 结果保存到 {result_file}")
            synchronized_print("-" * 80)  # 添加分隔线，使输出更清晰
            return True
            
        except subprocess.TimeoutExpired:
            # 超时处理：终止当前进程但保留Docker容器
            process.kill()
            
            # 清理可能残留的进程
            cleanup_cmd = f"docker exec {docker_container} pkill -f 'python3 /home/ubuntu/packj/main.py'"
            subprocess.run(cleanup_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 记录超时信息
            timeout_msg = f"分析超时（{timeout_seconds}秒）"
            synchronized_print(f"[{docker_container}] {timeout_msg}: {result_name}/{version}")
            
            # 保存超时信息到结果文件
            result_file = os.path.join(target_dir, "result.txt")
            with open(result_file, 'w') as f:
                f.write(f"ERROR: {timeout_msg}")
            
            synchronized_print("-" * 80)  # 添加分隔线，使输出更清晰
            return False
            
    except Exception as e:
        synchronized_print(f"[{docker_container}] 分析失败: {analysis_path}, 错误: {str(e)}")
        synchronized_print("-" * 80)  # 添加分隔线，使输出更清晰
        return False

def run_packj_analysis_direct(package_path, package_name, version, is_malware, docker_container=None, timeout_seconds=180):
    """
    直接运行packj分析，不需要从路径中提取包名和版本
    
    Args:
        package_path: 包路径
        package_name: 包名
        version: 版本
        is_malware: 是否为恶意包
        docker_container: Docker容器名称
        timeout_seconds: 超时时间（秒）
    """
    # 使用默认Docker容器名称如果未指定
    if docker_container is None:
        docker_container = "packj-dev-1"
        
    # 确定目标目录
    target_base_dir = MALWARE_TARGET_DIR if is_malware else BENIGN_TARGET_DIR
    
    # 使用包名/版本的目录结构
    result_dir_path = os.path.join(target_base_dir, package_name, version)
    
    # 检查是否已经分析过
    result_file = os.path.join(result_dir_path, "result.txt")
    if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
        synchronized_print(f"[{docker_container}] 跳过已分析的包: {package_name}/{version}")
        return True
    
    # 处理作用域包
    analysis_path, display_name, result_name = process_domain_package(package_path, package_name, version, is_malware, docker_container)
    
    # 使用原始包名/版本创建结果目录
    target_dir = os.path.join(target_base_dir, result_name, version)
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        synchronized_print(f"[{docker_container}] 创建结果目录失败: {str(e)}")
        return False
    
    # 修改路径格式，将宿主机路径转换为Docker容器内路径
    docker_path = get_docker_path(analysis_path)
    
    # 打印调试信息
    synchronized_print(f"[{docker_container}] 分析包: {package_name}/{version}")
    synchronized_print(f"[{docker_container}] 本地路径: {analysis_path}")
    synchronized_print(f"[{docker_container}] Docker路径: {docker_path}")
    
    # 运行docker命令
    cmd = f"docker exec -u ubuntu -it {docker_container} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:{docker_path}"
    synchronized_print(f"[{docker_container}] 执行Docker命令: {cmd}")
    
    try:
        # 使用subprocess.Popen和超时机制
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        try:
            # 等待进程完成，设置超时
            stdout, stderr = process.communicate(timeout=timeout_seconds)
            
            # 保存结果到文件
            result_file = os.path.join(target_dir, "result.txt")
            with open(result_file, 'w') as f:
                f.write(stdout)
            
            synchronized_print(f"[{docker_container}] 分析完成: {result_name}/{version}, 结果保存到 {result_file}")
            synchronized_print("-" * 80)  # 添加分隔线，使输出更清晰
            return True
            
        except subprocess.TimeoutExpired:
            # 超时处理：终止当前进程但保留Docker容器
            process.kill()
            
            # 清理可能残留的进程
            cleanup_cmd = f"docker exec {docker_container} pkill -f 'python3 /home/ubuntu/packj/main.py'"
            subprocess.run(cleanup_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 记录超时信息
            timeout_msg = f"分析超时（{timeout_seconds}秒）"
            synchronized_print(f"[{docker_container}] {timeout_msg}: {result_name}/{version}")
            
            # 保存超时信息到结果文件
            result_file = os.path.join(target_dir, "result.txt")
            with open(result_file, 'w') as f:
                f.write(f"ERROR: {timeout_msg}")
            
            synchronized_print("-" * 80)  # 添加分隔线，使输出更清晰
            return False
            
    except Exception as e:
        synchronized_print(f"[{docker_container}] 分析失败: {analysis_path}, 错误: {str(e)}")
        synchronized_print("-" * 80)  # 添加分隔线，使输出更清晰
        return False

def worker_process_direct(package_list, is_malware, worker_id, docker_containers, timeout_seconds):
    """
    直接处理包列表的工作进程函数
    
    Args:
        package_list: 包列表，每个元素为(package_name, version, copied_path)
        is_malware: 是否为恶意包
        worker_id: 工作进程ID
        docker_containers: Docker容器列表
        timeout_seconds: 超时时间
    """
    # 为每个工作进程分配一个Docker容器
    docker_container = docker_containers[worker_id % len(docker_containers)]
    
    synchronized_print(f"工作进程 {worker_id} 使用Docker容器 {docker_container} 开始处理 {len(package_list)} 个包")
    synchronized_print("=" * 80)  # 添加明显的分隔线
    
    for i, (package_name, version, copied_path) in enumerate(package_list):
        # 添加一个小的随机延迟，避免所有进程同时启动
        time.sleep(random.uniform(0.1, 0.5))
        synchronized_print(f"[{docker_container}] 处理包 {i+1}/{len(package_list)}: {package_name}/{version}")
        run_packj_analysis_direct(copied_path, package_name, version, is_malware, docker_container, timeout_seconds)
    
    synchronized_print(f"[{docker_container}] 已完成所有 {len(package_list)} 个包的处理")
    synchronized_print("=" * 80)  # 添加明显的分隔线

def worker_process(package_list, is_malware, source_base_dir, worker_id, docker_containers, timeout_seconds, error_packages):
    """
    工作进程函数，处理分配给它的包列表
    """
    # 为每个工作进程分配一个Docker容器
    docker_container = docker_containers[worker_id % len(docker_containers)]
    
    synchronized_print(f"工作进程 {worker_id} 使用Docker容器 {docker_container} 开始处理 {len(package_list)} 个包")
    synchronized_print("=" * 80)  # 添加明显的分隔线
    
    for i, package_path in enumerate(package_list):
        # 添加一个小的随机延迟，避免所有进程同时启动
        time.sleep(random.uniform(0.1, 0.5))
        
        # 检查包是否在错误列表中
        package_name, version = extract_package_info(package_path, source_base_dir)
        if not should_analyze_package(package_name, version, error_packages):
            synchronized_print(f"[{docker_container}] 跳过不在错误列表中的包: {package_name}/{version}")
            continue
        
        synchronized_print(f"[{docker_container}] 处理包 {i+1}/{len(package_list)}: {package_name}/{version}")
        run_packj_analysis(package_path, is_malware, source_base_dir, docker_container, timeout_seconds)
    
    synchronized_print(f"[{docker_container}] 已完成所有 {len(package_list)} 个包的处理")
    synchronized_print("=" * 80)  # 添加明显的分隔线

def process_error_packages_directly(error_packages, is_malware, use_parallel=False, num_containers=1, timeout_seconds=180):
    """
    直接根据错误包列表处理包，不扫描目录
    
    Args:
        error_packages: 错误包集合，格式为"包名/版本"
        is_malware: 是否为恶意包
        use_parallel: 是否并行处理
        num_containers: Docker容器数量
        timeout_seconds: 超时时间
    """
    # 过滤出当前类型的包（恶意包或良性包）
    package_type = "malware" if is_malware else "benign"
    filtered_packages = []
    
    for package_key in error_packages:
        if '/' in package_key:
            package_name, version = package_key.split('/', 1)
            
            # 构建并复制包
            copied_path = build_package_path_from_error_list(package_name, version, is_malware)
            if copied_path:
                filtered_packages.append((package_name, version, copied_path))
            else:
                synchronized_print(f"跳过无法处理的包: {package_key}")
    
    if not filtered_packages:
        synchronized_print(f"没有找到可处理的{package_type}包")
        return
    
    synchronized_print(f"准备处理 {len(filtered_packages)} 个{package_type}包")
    
    if not use_parallel:
        # 串行处理
        for package_name, version, copied_path in filtered_packages:
            synchronized_print(f"处理包: {package_name}/{version}")
            
            # 将/tmp路径转换为Docker路径
            docker_path = get_docker_path(copied_path)
            
            # 运行分析
            success = run_packj_analysis_direct(copied_path, package_name, version, is_malware, timeout_seconds=timeout_seconds)
            if success:
                synchronized_print(f"成功分析: {package_name}/{version}")
            else:
                synchronized_print(f"分析失败: {package_name}/{version}")
    else:
        # 并行处理
        # 生成Docker容器名称列表
        docker_containers = [f"{DOCKER_CONTAINER_PREFIX}{i+1}" for i in range(num_containers)]
        synchronized_print(f"使用 {num_containers} 个Docker容器进行并行处理: {', '.join(docker_containers)}")
        
        # 将包列表分成几个子列表，每个进程处理一个子列表
        packages_per_process = [[] for _ in range(num_containers)]
        for i, (package_name, version, copied_path) in enumerate(filtered_packages):
            container_idx = i % num_containers
            container_name = docker_containers[container_idx]
            synchronized_print(f"[{container_name}] 分配包: {package_name}/{version}")
            packages_per_process[container_idx].append((package_name, version, copied_path))
        
        # 创建并启动多个进程
        processes = []
        for i in range(num_containers):
            if packages_per_process[i]:  # 只有当有包需要处理时才创建进程
                container_name = docker_containers[i]
                synchronized_print(f"[{container_name}] 启动工作进程，处理 {len(packages_per_process[i])} 个包")
                p = multiprocessing.Process(
                    target=worker_process_direct,
                    args=(packages_per_process[i], is_malware, i, docker_containers, timeout_seconds)
                )
                processes.append(p)
                p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        container_summary = [f"{docker_containers[i]}: {len(packages_per_process[i])}个包" for i in range(num_containers) if packages_per_process[i]]
        synchronized_print(f"所有进程已完成处理 {len(filtered_packages)} 个包 ({', '.join(container_summary)})")

def process_directory(source_dir, is_malware, use_parallel=False, num_containers=1, timeout_seconds=180, error_packages=None):
    """
    处理指定目录下的所有包，可选择并行处理
    只处理错误包列表中的包
    """
    if error_packages is None:
        error_packages = set()
    
    # 获取一级目录（包名）
    package_dirs = [os.path.join(source_dir, d) for d in os.listdir(source_dir) 
                   if os.path.isdir(os.path.join(source_dir, d))]
    
    # 确定目标目录
    target_base_dir = MALWARE_TARGET_DIR if is_malware else BENIGN_TARGET_DIR
    
    if not use_parallel:
        # 串行处理
        processed_count = 0
        skipped_count = 0
        
        for package_dir in package_dirs:
            package_name = os.path.basename(package_dir)
            synchronized_print(f"检查包: {package_name}")
            
            # 获取包下的所有版本目录
            try:
                version_dirs = [os.path.join(package_dir, v) for v in os.listdir(package_dir)
                              if os.path.isdir(os.path.join(package_dir, v))]
                
                if not version_dirs:
                    synchronized_print(f"警告: 包 {package_name} 下没有版本目录")
                    continue
                
                for version_dir in version_dirs:
                    version = os.path.basename(version_dir)
                    
                    # 检查是否在错误包列表中
                    if not should_analyze_package(package_name, version, error_packages):
                        synchronized_print(f"跳过不在错误列表中的包: {package_name}/{version}")
                        skipped_count += 1
                        continue
                    
                    synchronized_print(f"处理版本: {package_name}/{version}")
                    
                    # 先检查是否已经成功分析过
                    if is_already_analyzed(package_name, version, target_base_dir):
                        synchronized_print(f"跳过已成功分析的包: {package_name}/{version}")
                        continue
                    
                    # 在版本目录中查找package.json
                    package_json_dir = find_package_json_dir(version_dir)
                    
                    if package_json_dir:
                        synchronized_print(f"找到package.json: {package_json_dir}")
                        run_packj_analysis(package_json_dir, is_malware, source_dir, timeout_seconds=timeout_seconds)
                        processed_count += 1
                    else:
                        synchronized_print(f"未找到package.json: {version_dir}")
            except Exception as e:
                synchronized_print(f"处理包 {package_name} 时出错: {str(e)}")
        
        synchronized_print(f"串行处理完成: 处理了 {processed_count} 个包，跳过了 {skipped_count} 个包")
    else:
        # 并行处理
        # 生成Docker容器名称列表
        docker_containers = [f"{DOCKER_CONTAINER_PREFIX}{i+1}" for i in range(num_containers)]
        synchronized_print(f"使用 {num_containers} 个Docker容器进行并行处理: {', '.join(docker_containers)}")
        
        # 收集所有需要处理的包路径（只包含错误包列表中的包）
        all_packages = []
        total_packages_found = 0
        packages_to_analyze = 0
        
        for package_dir in package_dirs:
            package_name = os.path.basename(package_dir)
            synchronized_print(f"检查包: {package_name}")
            
            # 获取包下的所有版本目录
            try:
                version_dirs = [os.path.join(package_dir, v) for v in os.listdir(package_dir)
                              if os.path.isdir(os.path.join(package_dir, v))]
                
                if not version_dirs:
                    synchronized_print(f"警告: 包 {package_name} 下没有版本目录")
                    continue
                
                for version_dir in version_dirs:
                    version = os.path.basename(version_dir)
                    total_packages_found += 1
                    
                    # 检查是否在错误包列表中
                    if not should_analyze_package(package_name, version, error_packages):
                        continue
                    
                    synchronized_print(f"发现错误包: {package_name}/{version}")
                    
                    # 先检查是否已经成功分析过
                    if is_already_analyzed(package_name, version, target_base_dir):
                        synchronized_print(f"跳过已成功分析的包: {package_name}/{version}")
                        continue
                    
                    # 在版本目录中查找package.json
                    package_json_dir = find_package_json_dir(version_dir)
                    
                    if package_json_dir:
                        synchronized_print(f"找到package.json: {package_json_dir}")
                        all_packages.append(package_json_dir)
                        packages_to_analyze += 1
                    else:
                        synchronized_print(f"未找到package.json: {version_dir}")
            except Exception as e:
                synchronized_print(f"处理包 {package_name} 时出错: {str(e)}")
        
        synchronized_print(f"总共发现 {total_packages_found} 个包，其中 {packages_to_analyze} 个在错误列表中需要分析")
        
        if not all_packages:
            synchronized_print(f"没有找到需要处理的错误包: {source_dir}")
            return
        
        # 将包列表分成几个子列表，每个进程处理一个子列表
        packages_per_process = [[] for _ in range(num_containers)]
        for i, package_path in enumerate(all_packages):
            container_idx = i % num_containers
            container_name = docker_containers[container_idx]
            package_name, version = extract_package_info(package_path, source_dir)
            synchronized_print(f"[{container_name}] 分配包: {package_name}/{version}")
            packages_per_process[container_idx].append(package_path)
        
        # 创建并启动多个进程
        processes = []
        for i in range(num_containers):
            if packages_per_process[i]:  # 只有当有包需要处理时才创建进程
                container_name = docker_containers[i]
                synchronized_print(f"[{container_name}] 启动工作进程，处理 {len(packages_per_process[i])} 个包")
                p = multiprocessing.Process(
                    target=worker_process,
                    args=(packages_per_process[i], is_malware, source_dir, i, docker_containers, timeout_seconds, error_packages)
                )
                processes.append(p)
                p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        container_summary = [f"{docker_containers[i]}: {len(packages_per_process[i])}个包" for i in range(num_containers) if packages_per_process[i]]
        synchronized_print(f"所有进程已完成处理 {len(all_packages)} 个错误包 ({', '.join(container_summary)})")

def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='使用packj分析错误报告中的特定NPM包')
    parser.add_argument('--parallel', action='store_true', help='是否使用并行处理')
    parser.add_argument('--containers', type=int, default=NUM_DOCKER_CONTAINERS, 
                        help=f'Docker容器数量 (默认: {NUM_DOCKER_CONTAINERS})')
    parser.add_argument('--skip-docker-setup', action='store_true', 
                        help='跳过Docker容器设置（假设容器已经存在并准备好）')
    parser.add_argument('--only-docker-setup', action='store_true',
                        help='只执行Docker容器设置，不进行包分析')
    parser.add_argument('--timeout', type=int, default=600,
                        help='单个包分析的超时时间（秒），默认600秒(10分钟)')
    parser.add_argument('--error-file', type=str, default=ERROR_PACKAGES_FILE,
                        help=f'错误包列表文件路径 (默认: {ERROR_PACKAGES_FILE})')
    return parser.parse_args()

def worker_process_simple(package_list, worker_id, docker_containers, timeout_seconds):
    """
    简化版工作进程函数

    Args:
        package_list: 包列表，每个元素为 (category, package_name, version, docker_path)
        worker_id: 工作进程ID
        docker_containers: Docker容器列表
        timeout_seconds: 超时时间
    """
    docker_container = docker_containers[worker_id % len(docker_containers)]

    synchronized_print(f"工作进程 {worker_id} 使用Docker容器 {docker_container} 开始处理 {len(package_list)} 个包")
    synchronized_print("=" * 80)

    for i, (category, package_name, version, docker_path) in enumerate(package_list):
        time.sleep(random.uniform(0.1, 0.5))
        synchronized_print(f"[{docker_container}] 处理包 {i+1}/{len(package_list)}: {package_name}/{version}")
        run_packj_analysis_simple(docker_path, category, package_name, version, docker_container, timeout_seconds)

    synchronized_print(f"[{docker_container}] 已完成所有 {len(package_list)} 个包的处理")
    synchronized_print("=" * 80)

def process_packages_simple(packages, use_parallel=False, num_containers=1, timeout_seconds=180):
    """
    简化版包处理函数
    直接使用datacopy格式的包列表

    Args:
        packages: 包列表，每个元素为 (category, package_name, version)
        use_parallel: 是否并行处理
        num_containers: Docker容器数量
        timeout_seconds: 超时时间
    """
    if not packages:
        synchronized_print("没有找到可处理的包")
        return

    # 构建Docker路径
    package_with_paths = []
    for category, package_name, version in packages:
        docker_path = build_docker_path(category, package_name, version)
        package_with_paths.append((category, package_name, version, docker_path))

    synchronized_print(f"准备处理 {len(package_with_paths)} 个包")

    if not use_parallel:
        # 串行处理
        docker_container = f"{DOCKER_CONTAINER_PREFIX}1"
        for category, package_name, version, docker_path in package_with_paths:
            synchronized_print(f"处理包: {package_name}/{version}")
            run_packj_analysis_simple(docker_path, category, package_name, version, docker_container, timeout_seconds)
    else:
        # 并行处理
        docker_containers = [f"{DOCKER_CONTAINER_PREFIX}{i+1}" for i in range(num_containers)]
        synchronized_print(f"使用 {num_containers} 个Docker容器进行并行处理: {', '.join(docker_containers)}")

        # 分配包到各个容器
        packages_per_process = [[] for _ in range(num_containers)]
        for i, pkg_info in enumerate(package_with_paths):
            container_idx = i % num_containers
            packages_per_process[container_idx].append(pkg_info)

        # 创建并启动多个进程
        processes = []
        for i in range(num_containers):
            if packages_per_process[i]:
                container_name = docker_containers[i]
                synchronized_print(f"[{container_name}] 启动工作进程，处理 {len(packages_per_process[i])} 个包")
                p = multiprocessing.Process(
                    target=worker_process_simple,
                    args=(packages_per_process[i], i, docker_containers, timeout_seconds)
                )
                processes.append(p)
                p.start()

        # 等待所有进程完成
        for p in processes:
            p.join()

        synchronized_print(f"所有进程已完成处理 {len(package_with_paths)} 个包")

def main():
    """
    主函数
    """
    # 解析命令行参数
    args = parse_arguments()
    use_parallel = args.parallel
    num_containers = args.containers
    skip_docker_setup = args.skip_docker_setup
    only_docker_setup = args.only_docker_setup
    timeout_seconds = args.timeout
    error_file = args.error_file

    # 更新全局错误包文件路径
    global ERROR_PACKAGES_FILE
    ERROR_PACKAGES_FILE = error_file

    # 如果只执行Docker设置，强制使用并行模式
    if only_docker_setup:
        use_parallel = True

    # 第一步：设置Docker容器（如果需要）
    if use_parallel and not skip_docker_setup:
        docker_manager = DockerManager(DOCKER_CONTAINER_PREFIX, num_containers)
        docker_manager.setup_containers()

        if only_docker_setup:
            synchronized_print(f"\n已完成 {num_containers} 个Docker容器的设置。")
            synchronized_print(f"容器名称: {', '.join([f'{DOCKER_CONTAINER_PREFIX}{i+1}' for i in range(num_containers)])}")
            return  # 如果只执行Docker设置，此处退出

    # 加载错误包列表 (使用datacopy格式)
    packages = load_error_packages_datacopy()
    if not packages:
        synchronized_print("错误：没有找到需要分析的错误包")
        return

    # 打印运行模式
    if use_parallel:
        synchronized_print(f"使用并行模式，{num_containers} 个Docker容器，超时时间: {timeout_seconds}秒")
    else:
        synchronized_print(f"使用串行模式，单Docker容器，超时时间: {timeout_seconds}秒")
    synchronized_print(f"将分析 {len(packages)} 个错误包")

    # 处理所有包
    synchronized_print("\n开始处理错误包...")
    process_packages_simple(packages, use_parallel, num_containers, timeout_seconds)

if __name__ == "__main__":
    # 确保目标目录存在
    os.makedirs(MALWARE_TARGET_DIR, exist_ok=True)
    os.makedirs(BENIGN_TARGET_DIR, exist_ok=True)
    os.makedirs(DOMAIN_PACKAGE_DIR, exist_ok=True)
    
    # 设置多进程启动方法（如果在Windows上运行）
    if os.name == 'nt':
        multiprocessing.set_start_method('spawn')
    
    main()

# 使用示例:
# python detect_error_packages.py --only-docker-setup --containers 3
# python detect_error_packages.py --parallel --containers 4 --skip-docker-setup --timeout 1200
