#!/usr/bin/env python3
"""
多进程NPM包分析工具
使用packj工具分析NPM包，支持多个Docker容器并行处理
"""

import os
import sys
import subprocess
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import time
import threading
import json

# 全局配置
DOMAIN_PACKAGE_DIR = "/tmp/domain_package"
NUM_CONTAINERS = 20  # Docker容器数量，可根据需要调整这个值
DOCKER_CONTAINERS = [f"packj-dev-{i}" for i in range(1, NUM_CONTAINERS + 1)]  # 根据NUM_CONTAINERS生成容器列表
TIMEOUT_SECONDS = 600  # 10分钟超时
OUTPUT_BASE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace"

# 线程锁用于同步输出
print_lock = threading.Lock()

def synchronized_print(*args, **kwargs):
    """线程安全的打印函数"""
    with print_lock:
        print(*args, **kwargs)
        sys.stdout.flush()

def find_package_paths():
    """
    找到所有包的路径和对应的package.json位置
    返回: [(package_type, package_name, version, package_dir), ...]
    """
    package_paths = []
    
    for package_type in ['unzip_benign', 'unzip_malware']:
        type_dir = os.path.join(DOMAIN_PACKAGE_DIR, package_type)
        if not os.path.exists(type_dir):
            synchronized_print(f"❌ 目录不存在: {type_dir}")
            continue
            
        synchronized_print(f"🔍 扫描目录: {type_dir}")
        
        # 遍历所有包
        for item in os.listdir(type_dir):
            item_path = os.path.join(type_dir, item)
            if not os.path.isdir(item_path):
                continue
                
            if item.startswith('@'):
                # 以@开头的包，有三层结构: @scope/package/version
                for package_name in os.listdir(item_path):
                    package_dir = os.path.join(item_path, package_name)
                    if not os.path.isdir(package_dir):
                        continue
                    
                    for version in os.listdir(package_dir):
                        version_dir = os.path.join(package_dir, version)
                        if not os.path.isdir(version_dir):
                            continue
                        
                        # 找到最浅的package.json
                        package_json_dir = find_deepest_package_json(version_dir)
                        if package_json_dir:
                            full_package_name = f"{item}/{package_name}"
                            package_paths.append((package_type, full_package_name, version, package_json_dir))
            else:
                # 不以@开头的包，有两层结构: package/version
                for version in os.listdir(item_path):
                    version_dir = os.path.join(item_path, version)
                    if not os.path.isdir(version_dir):
                        continue
                    
                    # 找到最浅的package.json
                    package_json_dir = find_deepest_package_json(version_dir)
                    if package_json_dir:
                        package_paths.append((package_type, item, version, package_json_dir))
    
    synchronized_print(f"📊 总共找到 {len(package_paths)} 个包需要分析")
    return package_paths

def find_deepest_package_json(start_dir, max_depth=10):
    """
    从给定目录开始，找到最浅的package.json文件所在的目录
    """
    def search_directory(current_dir, depth=0):
        if depth > max_depth:
            return None
            
        # 检查当前目录是否有package.json
        package_json_path = os.path.join(current_dir, 'package.json')
        if os.path.exists(package_json_path):
            return current_dir
        
        # 递归搜索子目录
        try:
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                if os.path.isdir(item_path):
                    result = search_directory(item_path, depth + 1)
                    if result:
                        return result
        except (PermissionError, OSError):
            pass
        
        return None
    
    return search_directory(start_dir)

def convert_to_docker_path(local_path):
    """
    将本地路径转换为Docker容器内的路径
    /tmp/domain_package/... -> /tmp/packj/domain_package/...
    """
    if local_path.startswith('/tmp/'):
        return local_path.replace('/tmp/', '/tmp/packj/', 1)
    return local_path

def create_output_path(package_type, package_name, version):
    """
    创建输出文件路径
    """
    # 确定输出目录类型
    output_type = "benign" if package_type == "unzip_benign" else "malware"
    
    # 处理包名（以@开头的包需要特殊处理）
    if package_name.startswith('@'):
        # @scope/package -> @scope##package
        package_name_formatted = package_name.replace('/', '##')
    else:
        package_name_formatted = package_name
    
    # 创建完整的输出路径
    output_dir = os.path.join(OUTPUT_BASE_DIR, output_type, package_name_formatted, version)
    os.makedirs(output_dir, exist_ok=True)
    
    return os.path.join(output_dir, "result.txt")

def run_packj_analysis(args):
    """
    在指定的Docker容器中运行packj分析
    """
    package_type, package_name, version, package_dir, docker_container = args
    
    # 转换为Docker路径
    docker_path = convert_to_docker_path(package_dir)
    
    # 创建输出文件路径
    output_file = create_output_path(package_type, package_name, version)
    
    # 检查输出文件是否已存在，如果存在则跳过
    if os.path.exists(output_file):
        synchronized_print("⏭️ " + "=" * 95)
        synchronized_print(f"⏭️ 跳过已完成的包: {package_name} v{version}")
        synchronized_print(f"⏭️ 输出文件已存在: {output_file}")
        synchronized_print("⏭️ " + "=" * 95)
        return "skipped", package_name, version, docker_container
    
    # 构建命令
    cmd = f"docker exec -u ubuntu {docker_container} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:{docker_path}"
    
    synchronized_print("🚀 " + "=" * 95)
    synchronized_print(f"🚀 开始分析包: {package_name} v{version}")
    synchronized_print(f"🚀 容器: {docker_container}")
    synchronized_print(f"🚀 路径: {package_dir}")
    synchronized_print(f"🚀 Docker路径: {docker_path}")
    synchronized_print(f"🚀 输出文件: {output_file}")
    synchronized_print("🚀 " + "=" * 95)
    
    try:
        # 执行命令
        process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # 等待进程完成，设置超时
        stdout, stderr = process.communicate(timeout=TIMEOUT_SECONDS)
        
        # 保存结果到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stdout)
            if stderr:
                f.write(f"\n\n=== STDERR ===\n{stderr}")
        
        synchronized_print("✅ " + "=" * 95)
        synchronized_print(f"✅ 分析成功完成: {package_name} v{version}")
        synchronized_print(f"✅ 容器: {docker_container}")
        synchronized_print(f"✅ 输出文件: {output_file}")
        synchronized_print("✅ " + "=" * 95)
        
        return True, package_name, version, docker_container
        
    except subprocess.TimeoutExpired:
        # 超时处理
        process.kill()
        
        # 清理可能残留的进程
        cleanup_cmd = f"docker exec {docker_container} pkill -f 'python3 /home/ubuntu/packj/main.py'"
        subprocess.run(cleanup_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 写入超时错误信息
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("ERROR: Timeout")
        
        synchronized_print("⏰ " + "=" * 95)
        synchronized_print(f"⏰ 分析超时: {package_name} v{version}")
        synchronized_print(f"⏰ 容器: {docker_container}")
        synchronized_print(f"⏰ 超时时间: {TIMEOUT_SECONDS}秒")
        synchronized_print(f"⏰ 输出文件: {output_file}")
        synchronized_print("⏰ " + "=" * 95)
        
        return False, package_name, version, docker_container
        
    except Exception as e:
        # 其他错误处理
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"ERROR: {str(e)}")
        
        synchronized_print("❌ " + "=" * 95)
        synchronized_print(f"❌ 分析出错: {package_name} v{version}")
        synchronized_print(f"❌ 容器: {docker_container}")
        synchronized_print(f"❌ 错误: {str(e)}")
        synchronized_print(f"❌ 输出文件: {output_file}")
        synchronized_print("❌ " + "=" * 95)
        
        return False, package_name, version, docker_container

def main():
    """主函数"""
    synchronized_print("🎯 开始NPM包多进程分析")
    synchronized_print(f"🎯 Docker容器数量: {len(DOCKER_CONTAINERS)}")
    synchronized_print(f"🎯 超时设置: {TIMEOUT_SECONDS}秒")
    synchronized_print(f"🎯 输出目录: {OUTPUT_BASE_DIR}")
    
    # 确保输出目录存在
    os.makedirs(os.path.join(OUTPUT_BASE_DIR, "benign"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_BASE_DIR, "malware"), exist_ok=True)
    
    # 查找所有需要分析的包
    synchronized_print("\n📂 正在扫描包目录...")
    package_paths = find_package_paths()
    
    if not package_paths:
        synchronized_print("❌ 没有找到需要分析的包")
        return
    
    # 准备任务参数
    tasks = []
    container_index = 0
    
    for package_type, package_name, version, package_dir in package_paths:
        docker_container = DOCKER_CONTAINERS[container_index % len(DOCKER_CONTAINERS)]
        container_index += 1
        
        tasks.append((package_type, package_name, version, package_dir, docker_container))
    
    synchronized_print(f"\n🚀 开始并行分析 {len(tasks)} 个包...")
    
    # 统计变量
    completed = 0
    successful = 0
    failed = 0
    timeouts = 0
    skipped = 0
    
    start_time = time.time()
    
    # 使用进程池并行执行
    with ProcessPoolExecutor(max_workers=len(DOCKER_CONTAINERS)) as executor:
        # 提交所有任务
        future_to_task = {executor.submit(run_packj_analysis, task): task for task in tasks}
        
        # 处理完成的任务
        for future in as_completed(future_to_task):
            completed += 1
            task = future_to_task[future]
            
            try:
                result, package_name, version, docker_container = future.result()
                if result == True:
                    successful += 1
                elif result == "skipped":
                    skipped += 1
                else:
                    failed += 1
                    # 检查是否是超时
                    output_file = create_output_path(task[0], task[1], task[2])
                    if os.path.exists(output_file):
                        with open(output_file, 'r', encoding='utf-8') as f:
                            if f.read().strip() == "ERROR: Timeout":
                                timeouts += 1
                
            except Exception as e:
                failed += 1
                synchronized_print(f"❌ 任务执行异常: {e}")
            
            # 显示进度
            elapsed_time = time.time() - start_time
            progress = (completed / len(tasks)) * 100
            synchronized_print(f"📊 进度: {completed}/{len(tasks)} ({progress:.1f}%) | 成功: {successful} | 跳过: {skipped} | 失败: {failed} | 超时: {timeouts} | 耗时: {elapsed_time:.1f}s")
    
    # 最终统计
    total_time = time.time() - start_time
    synchronized_print("\n" + "=" * 100)
    synchronized_print("🎉 分析完成!")
    synchronized_print(f"📊 总任务数: {len(tasks)}")
    synchronized_print(f"✅ 成功: {successful}")
    synchronized_print(f"⏭️ 跳过: {skipped}")
    synchronized_print(f"❌ 失败: {failed}")
    synchronized_print(f"⏰ 超时: {timeouts}")
    synchronized_print(f"⏱️  总耗时: {total_time:.1f}秒")
    synchronized_print(f"📁 输出目录: {OUTPUT_BASE_DIR}")
    synchronized_print("=" * 100)

if __name__ == "__main__":
    main()