#!/usr/bin/env python3
import os
import subprocess
import shutil
from pathlib import Path
import multiprocessing
import time
import random
import argparse

# 定义源目录和目标目录
MALWARE_SOURCE_DIR = "/tmp/malicious_package/unzip_malware"
BENIGN_SOURCE_DIR = "/tmp/malicious_package/unzip_benign"
MALWARE_TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace/malware"
BENIGN_TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace/benign"
DOMAIN_PACKAGE_DIR = "/tmp/domain_package"

# Docker容器配置
DOCKER_CONTAINER_PREFIX = "packj-dev-"
NUM_DOCKER_CONTAINERS = 4  # 默认Docker容器数量，可通过命令行参数修改
DOCKER_IMAGE = "ossillate/packj:latest"
HOST_PM_UTIL_PATH = "/home2/wenbo/Documents/NPMAnalysis/Tools/packj/packj/audit/pm_util.py"
CONTAINER_PM_UTIL_PATH = "/home/ubuntu/packj/packj/audit/pm_util.py"

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
        
        print(f"正在删除现有容器: {', '.join(containers)}")
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
        print(f"正在创建 {self.num_containers} 个Docker容器...")
        for container_name in self.container_names:
            # 使用--entrypoint覆盖入口点，并运行tail命令保持容器运行
            cmd = f"docker run -d --name {container_name} --entrypoint '/bin/bash' {DOCKER_IMAGE} -c 'tail -f /dev/null'"
            print(f"创建容器: {container_name}")
            result = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                print(f"创建容器 {container_name} 失败: {result.stderr}")
            else:
                # 检查容器是否成功启动
                check_cmd = f"docker ps -q -f name={container_name}"
                check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
                if check_result.stdout.strip():
                    print(f"容器 {container_name} 成功启动")
                else:
                    print(f"警告: 容器 {container_name} 可能未成功启动")

    def set_container_permissions(self):
        """
        设置容器内的权限
        """
        print("正在设置容器权限...")
        for container_name in self.container_names:
            # 检查容器是否在运行
            check_cmd = f"docker ps -q -f name={container_name}"
            check_result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            if not check_result.stdout.strip():
                print(f"警告: 容器 {container_name} 不存在或未运行，跳过权限设置")
                continue
            
            # 设置目录所有权
            chown_cmd = f"docker exec -u 0 -it {container_name} chown -R ubuntu:ubuntu /tmp/packj"
            print(f"设置容器 {container_name} 的目录所有权: {chown_cmd}")
            chown_result = subprocess.run(chown_cmd, shell=True, stderr=subprocess.PIPE, text=True)
            
            if chown_result.returncode != 0:
                print(f"设置容器 {container_name} 的目录所有权失败: {chown_result.stderr}")
            
            # 设置目录权限
            chmod_cmd = f"docker exec -u 0 -it {container_name} chmod -R 755 /tmp/packj"
            print(f"设置容器 {container_name} 的目录权限: {chmod_cmd}")
            chmod_result = subprocess.run(chmod_cmd, shell=True, stderr=subprocess.PIPE, text=True)
            
            if chmod_result.returncode != 0:
                print(f"设置容器 {container_name} 的目录权限失败: {chmod_result.stderr}")
            else:
                print(f"容器 {container_name} 的权限设置成功")

    def copy_files_to_containers(self):
        """
        将必要的文件复制到每个容器中
        """
        print(f"正在将文件复制到容器...")
        for container_name in self.container_names:
            # 检查容器是否存在并运行
            check_cmd = f"docker ps -q -f name={container_name}"
            result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
            if not result.stdout.strip():
                print(f"警告: 容器 {container_name} 不存在或未运行，跳过文件复制")
                continue
            
            # 创建目标目录（如果不存在）
            mkdir_cmd = f"docker exec {container_name} mkdir -p /home/ubuntu/packj/packj/audit"
            subprocess.run(mkdir_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # 复制文件到容器
            cp_cmd = f"docker cp {HOST_PM_UTIL_PATH} {container_name}:{CONTAINER_PM_UTIL_PATH}"
            print(f"复制文件到 {container_name}: {cp_cmd}")
            result = subprocess.run(cp_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"警告: 复制文件到容器 {container_name} 失败: {result.stderr}")
            else:
                print(f"成功复制文件到容器 {container_name}")
    
    def setup_containers(self):
        """
        设置Docker容器：检查现有容器，删除旧容器，创建新容器，复制文件
        """
        print("开始设置Docker容器...")
        
        # 检查现有容器
        existing_containers = self.get_existing_containers()
        if existing_containers:
            print(f"发现现有容器: {', '.join(existing_containers)}")
            self.remove_containers(existing_containers)
        
        # 创建新容器
        self.create_containers()
        
        # 等待容器启动
        print("等待容器启动...")
        time.sleep(2)
        
        # 设置容器权限
        self.set_container_permissions()
        
        # 复制文件到容器
        self.copy_files_to_containers()
        
        print("Docker容器设置完成")
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

def run_packj_analysis(package_path, is_malware, source_base_dir, docker_container=None):
    """
    运行packj分析并保存结果
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
        print(f"[{docker_container}] 跳过已分析的包: {package_name}/{version}")
        return True
    
    # 处理作用域包
    analysis_path, display_name, result_name = process_domain_package(package_path, package_name, version, is_malware)
    
    # 使用原始包名/版本创建结果目录
    target_dir = os.path.join(target_base_dir, result_name, version)
    os.makedirs(target_dir, exist_ok=True)
    
    # 打印原始路径，帮助调试
    print(f"[{docker_container}] 原始路径: {package_path}")
    print(f"[{docker_container}] 处理后路径: {analysis_path}")
    
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
    print(f"[{docker_container}] Docker路径: {docker_path}")
    
    # 运行docker命令
    cmd = f"docker exec -u ubuntu -it {docker_container} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:{docker_path}"
    print(f"[{docker_container}] 执行Docker命令: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # 保存结果到文件
        result_file = os.path.join(target_dir, "result.txt")
        with open(result_file, 'w') as f:
            f.write(result.stdout)
        
        print(f"[{docker_container}] 分析完成: {result_name}/{version}, 结果保存到 {result_file}")
        return True
    except Exception as e:
        print(f"[{docker_container}] 分析失败: {analysis_path}, 错误: {str(e)}")
        return False

def worker_process(package_list, is_malware, source_base_dir, worker_id, docker_containers):
    """
    工作进程函数，处理分配给它的包列表
    """
    # 为每个工作进程分配一个Docker容器
    docker_container = docker_containers[worker_id % len(docker_containers)]
    
    print(f"工作进程 {worker_id} 使用Docker容器 {docker_container} 开始处理 {len(package_list)} 个包")
    
    for package_path in package_list:
        # 添加一个小的随机延迟，避免所有进程同时启动
        time.sleep(random.uniform(0.1, 0.5))
        run_packj_analysis(package_path, is_malware, source_base_dir, docker_container)

def process_directory(source_dir, is_malware, use_parallel=False, num_containers=1):
    """
    处理指定目录下的所有包，可选择并行处理
    """
    # 获取一级目录（包名）
    package_dirs = [os.path.join(source_dir, d) for d in os.listdir(source_dir) 
                   if os.path.isdir(os.path.join(source_dir, d))]
    
    if not use_parallel:
        # 串行处理
        for package_dir in package_dirs:
            # 查找包含package.json的最浅目录
            package_json_dir = find_package_json_dir(package_dir)
            
            if package_json_dir:
                print(f"找到package.json目录: {package_json_dir}")
                run_packj_analysis(package_json_dir, is_malware, source_dir)
            else:
                print(f"未找到package.json: {package_dir}")
    else:
        # 并行处理
        # 生成Docker容器名称列表
        docker_containers = [f"{DOCKER_CONTAINER_PREFIX}{i+1}" for i in range(num_containers)]
        print(f"使用 {num_containers} 个Docker容器进行并行处理: {', '.join(docker_containers)}")
        
        # 收集所有需要处理的包路径
        all_packages = []
        for package_dir in package_dirs:
            # 查找包含package.json的最浅目录
            package_json_dir = find_package_json_dir(package_dir)
            
            if package_json_dir:
                print(f"找到package.json目录: {package_json_dir}")
                all_packages.append(package_json_dir)
            else:
                print(f"未找到package.json: {package_dir}")
        
        if not all_packages:
            print(f"没有找到需要处理的包: {source_dir}")
            return
        
        # 将包列表分成几个子列表，每个进程处理一个子列表
        packages_per_process = [[] for _ in range(num_containers)]
        for i, package_path in enumerate(all_packages):
            container_idx = i % num_containers
            container_name = docker_containers[container_idx]
            print(f"[{container_name}] 分配包: {os.path.basename(os.path.dirname(package_path))}")
            packages_per_process[container_idx].append(package_path)
        
        # 创建并启动多个进程
        processes = []
        for i in range(num_containers):
            if packages_per_process[i]:  # 只有当有包需要处理时才创建进程
                container_name = docker_containers[i]
                print(f"[{container_name}] 启动工作进程，处理 {len(packages_per_process[i])} 个包")
                p = multiprocessing.Process(
                    target=worker_process,
                    args=(packages_per_process[i], is_malware, source_dir, i, docker_containers)
                )
                processes.append(p)
                p.start()
        
        # 等待所有进程完成
        for p in processes:
            p.join()
        
        container_summary = [f"{docker_containers[i]}: {len(packages_per_process[i])}个包" for i in range(num_containers) if packages_per_process[i]]
        print(f"所有进程已完成处理 {len(all_packages)} 个包 ({', '.join(container_summary)})")

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
    
    # 如果只执行Docker设置，强制使用并行模式
    if only_docker_setup:
        use_parallel = True
    
    # 第一步：设置Docker容器（如果需要）
    if use_parallel and not skip_docker_setup:
        docker_manager = DockerManager(DOCKER_CONTAINER_PREFIX, num_containers)
        docker_manager.setup_containers()
        
        if only_docker_setup:
            print(f"\n已完成 {num_containers} 个Docker容器的设置。")
            print(f"容器名称: {', '.join([f'{DOCKER_CONTAINER_PREFIX}{i+1}' for i in range(num_containers)])}")
            return  # 如果只执行Docker设置，此处退出
    
    # 打印运行模式
    if use_parallel:
        print(f"使用并行模式，{num_containers} 个Docker容器")
    else:
        print("使用串行模式，单Docker容器")
    
    # 第二步：处理包
    print("\n开始处理恶意包...")
    if os.path.exists(MALWARE_SOURCE_DIR):
        process_directory(MALWARE_SOURCE_DIR, True, use_parallel, num_containers)
    else:
        print(f"目录不存在: {MALWARE_SOURCE_DIR}")
    
    print("\n开始处理良性包...")
    if os.path.exists(BENIGN_SOURCE_DIR):
        process_directory(BENIGN_SOURCE_DIR, False, use_parallel, num_containers)
    else:
        print(f"目录不存在: {BENIGN_SOURCE_DIR}")

if __name__ == "__main__":
    # 确保目标目录存在
    os.makedirs(MALWARE_TARGET_DIR, exist_ok=True)
    os.makedirs(BENIGN_TARGET_DIR, exist_ok=True)
    os.makedirs(DOMAIN_PACKAGE_DIR, exist_ok=True)
    
    # 设置多进程启动方法（如果在Windows上运行）
    if os.name == 'nt':
        multiprocessing.set_start_method('spawn')
    
    main()
