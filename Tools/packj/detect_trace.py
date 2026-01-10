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
MALWARE_SOURCE_DIR = "/tmp/packj/domain_package/unzip_malware"
BENIGN_SOURCE_DIR = "/tmp/packj/domain_package/unzip_benign"
MALWARE_TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/packj/result_trace/malware-1"
BENIGN_TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/packj/result_trace/benign-1"
DOMAIN_PACKAGE_DIR = "/tmp/domain_package"

# Docker容器配置
DOCKER_CONTAINER_PREFIX = "packj-dev-"
NUM_DOCKER_CONTAINERS = 2  # 默认Docker容器数量，可通过命令行参数修改
DOCKER_IMAGE = "ossillate/packj:latest"
HOST_PM_UTIL_PATH = "/home2/wenbo/Documents/NPMAnalysis/Tools/packj/packj/audit/pm_util.py"
CONTAINER_PM_UTIL_PATH = "/home/ubuntu/packj/packj/audit/pm_util.py"

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
        
        # 不再对宿主机目录进行chmod操作
        # synchronized_print(f"设置宿主机目录权限: {DOMAIN_PACKAGE_DIR}")
        # os.system(f"chmod -R 777 {DOMAIN_PACKAGE_DIR}")
        
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


    def upgrade_nodejs_in_containers(self):
        """
        在每个容器中升级Node.js到最新版本
        """
        synchronized_print(f"正在升级容器中的Node.js版本...")
        for container_name in self.container_names:
            # 检查容器是否存在并运行
            check_cmd = f"docker ps -q -f name={container_name}"
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            if not result.stdout.strip():
                synchronized_print(f"警告: 容器 {container_name} 不存在或未运行，跳过Node.js升级")
                continue
            
            synchronized_print(f"开始升级容器 {container_name} 的Node.js...")
            
            # 1. 更新包管理器
            synchronized_print(f"容器 {container_name}: 更新包管理器...")
            update_cmd = f"docker exec -u 0 {container_name} apt-get update -y"
            subprocess.run(update_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 2. 安装必要依赖
            synchronized_print(f"容器 {container_name}: 安装必要依赖...")
            deps_cmd = f"docker exec -u 0 {container_name} apt-get install -y curl software-properties-common"
            subprocess.run(deps_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 3. 添加NodeSource官方仓库
            synchronized_print(f"容器 {container_name}: 添加NodeSource官方仓库...")
            repo_cmd = f"docker exec -u 0 {container_name} bash -c \"curl -fsSL https://deb.nodesource.com/setup_20.x | bash -\""
            subprocess.run(repo_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 4. 安装Node.js 20.x LTS
            synchronized_print(f"容器 {container_name}: 安装Node.js 20.x LTS...")
            install_cmd = f"docker exec -u 0 {container_name} apt-get install -y nodejs"
            result = subprocess.run(install_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                # 验证Node.js版本
                version_cmd = f"docker exec -u ubuntu {container_name} node --version"
                version_result = subprocess.run(version_cmd, shell=True, capture_output=True, text=True)
                if version_result.returncode == 0:
                    node_version = version_result.stdout.strip()
                    synchronized_print(f"容器 {container_name}: Node.js升级成功，版本: {node_version}")
                else:
                    synchronized_print(f"容器 {container_name}: Node.js升级完成，但无法获取版本信息")
            else:
                synchronized_print(f"容器 {container_name}: Node.js升级失败: {result.stderr}")

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
        设置Docker容器：检查现有容器，删除旧容器，创建新容器，升级Node.js，复制文件
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
        
        # 升级Node.js版本
        self.upgrade_nodejs_in_containers()
        
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
    检查包是否已经分析过
    """
    result_file = os.path.join(target_base_dir, package_name, version, "result.txt")
    if os.path.exists(result_file):
        # 检查文件是否有内容
        if os.path.getsize(result_file) > 0:
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
    
    # 打印原始路径，帮助调试
    synchronized_print(f"[{docker_container}] 原始路径: {package_path}")
    synchronized_print(f"[{docker_container}] 处理后路径: {analysis_path}")
    
    # 修改路径格式，将宿主机路径转换为Docker容器内路径
    docker_path = get_docker_path(analysis_path)
    
    # 打印Docker路径，帮助调试
    synchronized_print(f"[{docker_container}] Docker路径: {docker_path}")
    
    # 运行docker命令
    cmd = f"docker exec -u ubuntu -it {docker_container} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:{docker_path}"
    
    # 详细打印分析信息
    synchronized_print("=" * 100)
    synchronized_print(f"📦 包名: {result_name}")
    synchronized_print(f"🔢 版本: {version}")
    synchronized_print(f"🐳 容器: {docker_container}")
    synchronized_print(f"📁 路径: {docker_path}")
    synchronized_print(f"🚀 命令: {cmd}")
    synchronized_print("=" * 100)
    
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
            
            # 分析完成的详细信息
            synchronized_print("✅ " + "=" * 95)
            synchronized_print(f"✅ 分析成功完成!")
            synchronized_print(f"✅ 包名: {result_name}")
            synchronized_print(f"✅ 版本: {version}")
            synchronized_print(f"✅ 容器: {docker_container}")
            synchronized_print(f"✅ 结果文件: {result_file}")
            synchronized_print("✅ " + "=" * 95)
            return True
            
        except subprocess.TimeoutExpired:
            # 超时处理：终止当前进程但保留Docker容器
            process.kill()
            
            # 清理可能残留的进程
            cleanup_cmd = f"docker exec {docker_container} pkill -f 'python3 /home/ubuntu/packj/main.py'"
            subprocess.run(cleanup_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 记录超时信息
            timeout_msg = f"分析超时（{timeout_seconds}秒）"
            
            # 超时的详细信息
            synchronized_print("⏰ " + "=" * 95)
            synchronized_print(f"⏰ 分析超时!")
            synchronized_print(f"⏰ 包名: {result_name}")
            synchronized_print(f"⏰ 版本: {version}")
            synchronized_print(f"⏰ 容器: {docker_container}")
            synchronized_print(f"⏰ 超时时间: {timeout_seconds}秒")
            synchronized_print("⏰ " + "=" * 95)
            
            # 保存超时信息到结果文件
            result_file = os.path.join(target_dir, "result.txt")
            with open(result_file, 'w') as f:
                f.write(f"ERROR: {timeout_msg}")
            
            return False
            
    except Exception as e:
        # 异常的详细信息
        synchronized_print("❌ " + "=" * 95)
        synchronized_print(f"❌ 分析异常!")
        synchronized_print(f"❌ 包名: {result_name}")
        synchronized_print(f"❌ 版本: {version}")
        synchronized_print(f"❌ 容器: {docker_container}")
        synchronized_print(f"❌ 错误: {str(e)}")
        synchronized_print("❌ " + "=" * 95)
        return False

def worker_process(package_list, is_malware, source_base_dir, worker_id, docker_containers, timeout_seconds):
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
        synchronized_print(f"[{docker_container}] 处理包 {i+1}/{len(package_list)}: {os.path.basename(os.path.dirname(package_path))}")
        run_packj_analysis(package_path, is_malware, source_base_dir, docker_container, timeout_seconds)
    
    synchronized_print(f"[{docker_container}] 已完成所有 {len(package_list)} 个包的处理")
    synchronized_print("=" * 80)  # 添加明显的分隔线

def process_directory(source_dir, is_malware, use_parallel=False, num_containers=1, timeout_seconds=180):
    """
    处理指定目录下的所有包，可选择并行处理
    """
    # 获取一级目录（包名）
    package_dirs = [os.path.join(source_dir, d) for d in os.listdir(source_dir) 
                   if os.path.isdir(os.path.join(source_dir, d))]
    
    # 确定目标目录
    target_base_dir = MALWARE_TARGET_DIR if is_malware else BENIGN_TARGET_DIR
    
    if not use_parallel:
        # 串行处理
        for package_dir in package_dirs:
            package_name = os.path.basename(package_dir)
            synchronized_print(f"处理包: {package_name}")
            
            # 获取包下的所有版本目录
            try:
                version_dirs = [os.path.join(package_dir, v) for v in os.listdir(package_dir)
                              if os.path.isdir(os.path.join(package_dir, v))]
                
                if not version_dirs:
                    synchronized_print(f"警告: 包 {package_name} 下没有版本目录")
                    continue
                
                for version_dir in version_dirs:
                    version = os.path.basename(version_dir)
                    synchronized_print(f"处理版本: {package_name}/{version}")
                    
                    # 先检查是否已经分析过
                    if is_already_analyzed(package_name, version, target_base_dir):
                        synchronized_print(f"跳过已分析的包: {package_name}/{version}")
                        continue
                    
                    # 在版本目录中查找package.json
                    package_json_dir = find_package_json_dir(version_dir)
                    
                    if package_json_dir:
                        synchronized_print(f"找到package.json: {package_json_dir}")
                        run_packj_analysis(package_json_dir, is_malware, source_dir, timeout_seconds=timeout_seconds)
                    else:
                        synchronized_print(f"未找到package.json: {version_dir}")
            except Exception as e:
                synchronized_print(f"处理包 {package_name} 时出错: {str(e)}")
    else:
        # 并行处理
        # 生成Docker容器名称列表
        docker_containers = [f"{DOCKER_CONTAINER_PREFIX}{i+1}" for i in range(num_containers)]
        synchronized_print(f"使用 {num_containers} 个Docker容器进行并行处理: {', '.join(docker_containers)}")
        
        # 收集所有需要处理的包路径
        all_packages = []
        for package_dir in package_dirs:
            package_name = os.path.basename(package_dir)
            synchronized_print(f"处理包: {package_name}")
            
            # 获取包下的所有版本目录
            try:
                version_dirs = [os.path.join(package_dir, v) for v in os.listdir(package_dir)
                              if os.path.isdir(os.path.join(package_dir, v))]
                
                if not version_dirs:
                    synchronized_print(f"警告: 包 {package_name} 下没有版本目录")
                    continue
                
                for version_dir in version_dirs:
                    version = os.path.basename(version_dir)
                    synchronized_print(f"处理版本: {package_name}/{version}")
                    
                    # 先检查是否已经分析过
                    if is_already_analyzed(package_name, version, target_base_dir):
                        synchronized_print(f"跳过已分析的包: {package_name}/{version}")
                        continue
                    
                    # 在版本目录中查找package.json
                    package_json_dir = find_package_json_dir(version_dir)
                    
                    if package_json_dir:
                        synchronized_print(f"找到package.json: {package_json_dir}")
                        all_packages.append(package_json_dir)
                    else:
                        synchronized_print(f"未找到package.json: {version_dir}")
            except Exception as e:
                synchronized_print(f"处理包 {package_name} 时出错: {str(e)}")
        
        if not all_packages:
            synchronized_print(f"没有找到需要处理的包: {source_dir}")
            return
        
        # 将包列表分成几个子列表，每个进程处理一个子列表
        packages_per_process = [[] for _ in range(num_containers)]
        for i, package_path in enumerate(all_packages):
            container_idx = i % num_containers
            container_name = docker_containers[container_idx]
            synchronized_print(f"[{container_name}] 分配包: {os.path.basename(os.path.dirname(os.path.dirname(package_path)))}/{os.path.basename(os.path.dirname(package_path))}")
            packages_per_process[container_idx].append(package_path)
        
        # 创建并启动多个进程
        processes = []
        for i in range(num_containers):
            if packages_per_process[i]:  # 只有当有包需要处理时才创建进程
                container_name = docker_containers[i]
                synchronized_print(f"[{container_name}] 启动工作进程，处理 {len(packages_per_process[i])} 个包")
                p = multiprocessing.Process(
                    target=worker_process,
                    args=(packages_per_process[i], is_malware, source_dir, i, docker_containers, timeout_seconds)
                )
                processes.append(p)
                p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        container_summary = [f"{docker_containers[i]}: {len(packages_per_process[i])}个包" for i in range(num_containers) if packages_per_process[i]]
        synchronized_print(f"所有进程已完成处理 {len(all_packages)} 个包 ({', '.join(container_summary)})")

def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='使用packj分析NPM包')
    parser.add_argument('--parallel', action='store_true', help='是否使用并行处理')
    parser.add_argument('--containers', type=int, default=NUM_DOCKER_CONTAINERS, 
                        help=f'Docker容器数量 (默认: {NUM_DOCKER_CONTAINERS})')
    parser.add_argument('--skip-docker-setup', action='store_true', 
                        help='跳过Docker容器设置（假设容器已经存在并准备好）')
    parser.add_argument('--only-docker-setup', action='store_true',
                        help='只执行Docker容器设置，不进行包分析')
    parser.add_argument('--timeout', type=int, default=600,
                        help='单个包分析的超时时间（秒），默认180秒(3分钟)')
    return parser.parse_args()

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
    
    # 打印运行模式
    if use_parallel:
        synchronized_print(f"使用并行模式，{num_containers} 个Docker容器，超时时间: {timeout_seconds}秒")
    else:
        synchronized_print(f"使用串行模式，单Docker容器，超时时间: {timeout_seconds}秒")
    
    # 确保domain_package目录存在并有正确的权限
    os.makedirs(DOMAIN_PACKAGE_DIR, exist_ok=True)
    # 不再设置domain_package目录权限
    # os.system(f"chmod -R 777 {DOMAIN_PACKAGE_DIR}")
    
    # 第二步：处理包
    synchronized_print("\n开始处理恶意包...")
    if os.path.exists(MALWARE_SOURCE_DIR):
        process_directory(MALWARE_SOURCE_DIR, True, use_parallel, num_containers, timeout_seconds)
    else:
        synchronized_print(f"目录不存在: {MALWARE_SOURCE_DIR}")
    
    synchronized_print("\n开始处理良性包...")
    if os.path.exists(BENIGN_SOURCE_DIR):
        process_directory(BENIGN_SOURCE_DIR, False, use_parallel, num_containers, timeout_seconds)
    else:
        synchronized_print(f"目录不存在: {BENIGN_SOURCE_DIR}")

if __name__ == "__main__":
    # 确保目标目录存在
    os.makedirs(MALWARE_TARGET_DIR, exist_ok=True)
    os.makedirs(BENIGN_TARGET_DIR, exist_ok=True)
    os.makedirs(DOMAIN_PACKAGE_DIR, exist_ok=True)
    # 不再设置domain_package目录权限
   # os.system(f"chmod -R 777 {DOMAIN_PACKAGE_DIR}")
    
    # 设置多进程启动方法（如果在Windows上运行）
    if os.name == 'nt':
        multiprocessing.set_start_method('spawn')
    
    main()


# python detect_trace.py --only-docker-setup --containers 3
# python detect_trace.py --parallel --containers 40 --skip-docker-setup --timeout 600