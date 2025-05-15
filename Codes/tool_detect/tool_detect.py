#!/usr/bin/env python3
import os
import sys
import subprocess
import multiprocessing
from pathlib import Path
import glob
import time
import signal

# 直接在代码中设置参数
NUM_PROCESSES = 24  # 并行处理的进程数
TOOL_TIMEOUT = 120   # 每个工具的超时时间（秒）

# 添加超时处理函数
def run_with_timeout(cmd, timeout=TOOL_TIMEOUT):
    """运行命令，如果超过超时时间则终止进程"""
    start_time = time.time()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return_code = process.returncode
        execution_time = time.time() - start_time
        return (return_code, stdout, stderr, execution_time)
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            process.wait(timeout=5)  # 给进程一点时间来终止
        except:
            pass  # 如果等待也超时，直接忽略
        return (-1, f"Command timed out after {timeout} seconds", "", timeout)

class NPMToolDetector:
    def __init__(self):
        # 定义数据路径
        self.base_path = "/home2/wenbo/Documents/NPMAnalysis/Dataset"
        self.zip_benign_path = os.path.join(self.base_path, "zip_benign")
        self.zip_malicious_path = os.path.join(self.base_path, "zip_malware")
        self.unzip_benign_path = os.path.join(self.base_path, "unzip_benign")
        self.unzip_malicious_path = os.path.join(self.base_path, "unzip_malware")
        
        # 定义输出路径
        self.output_base = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output"
        self.output_paths = {
            "guarddog": {
                "benign": os.path.join(self.output_base, "guarddog/benign"),
                "malware": os.path.join(self.output_base, "guarddog/malware")
            },
            "ossgadget": {
                "benign": os.path.join(self.output_base, "ossgadget/benign"),
                "malware": os.path.join(self.output_base, "ossgadget/malware")
            }
        }
        
        # 确保所有输出目录存在
        self._ensure_output_dirs()
        
        # 记录已处理的包
        self.processed_count = 0
        self.skipped_count = 0
        
    def _ensure_output_dirs(self):
        """确保所有输出目录存在"""
        for tool in self.output_paths:
            for category in self.output_paths[tool]:
                os.makedirs(self.output_paths[tool][category], exist_ok=True)
    
    def _create_output_path(self, tool, category, package_name, version):
        """创建输出文件路径"""
        base_dir = self.output_paths[tool][category]
        
        # 创建包名文件夹
        package_dir = os.path.join(base_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        
        # 创建版本文件夹
        version_dir = os.path.join(package_dir, version)
        os.makedirs(version_dir, exist_ok=True)
        
        # 创建结果文件路径
        return os.path.join(version_dir, "result.txt")
    
    def run_guarddog(self, zip_file_path, package_name, version, category):
        """运行Guarddog工具并保存结果"""
        output_file = self._create_output_path("guarddog", category, package_name, version)
        
        # 检查输出文件是否已存在
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"跳过已处理的Guarddog检测: {package_name}@{version}")
            return None
            
        cmd = ["guarddog", "npm", "scan", zip_file_path]
        print(f"开始Guarddog检测: {package_name}@{version}")
        return_code, stdout, stderr, execution_time = run_with_timeout(cmd)
        
        if return_code == -1:  # 超时
            print(f"Guarddog检测超时: {package_name}@{version}, 跳过")
            return None
        else:
            output = stdout if stdout.strip() else "benign"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Guarddog检测完成: {package_name}@{version}, 用时: {execution_time:.2f}秒")
            return output
    
    def run_ossgadget(self, unzip_dir_path, package_name, version, category):
        """运行OSS Gadget工具并保存结果"""
        output_file = self._create_output_path("ossgadget", category, package_name, version)
        
        # 检查输出文件是否已存在
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"跳过已处理的OSSGadget检测: {package_name}@{version}")
            return None
            
        cmd = ["/home2/wenbo/Documents/NPMAnalysis/Tools/OSSGadget/oss-detect-backdoor", unzip_dir_path]
        print(f"开始OSSGadget检测: {package_name}@{version}")
        return_code, stdout, stderr, execution_time = run_with_timeout(cmd)
        
        if return_code == -1:  # 超时
            print(f"OSSGadget检测超时: {package_name}@{version}, 跳过")
            return None
        else:
            output = stdout if stdout.strip() else "benign"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"OSSGadget检测完成: {package_name}@{version}, 用时: {execution_time:.2f}秒")
            return output
    
    def process_package(self, category, package_name):
        """处理单个包的所有版本"""
        try:
            # 确定路径
            if category == "benign":
                zip_package_path = os.path.join(self.zip_benign_path, package_name)
                unzip_package_path = os.path.join(self.unzip_benign_path, package_name)
            else:
                zip_package_path = os.path.join(self.zip_malicious_path, package_name)
                unzip_package_path = os.path.join(self.unzip_malicious_path, package_name)
            
            # 检查路径是否存在
            if not os.path.exists(zip_package_path) or not os.path.exists(unzip_package_path):
                print(f"警告: 找不到包 {package_name} 的路径")
                return
            
            # 获取所有版本目录
            versions = os.listdir(zip_package_path)
            
            for version in versions:
                zip_version_path = os.path.join(zip_package_path, version)
                unzip_version_path = os.path.join(unzip_package_path, version)
                
                # 检查是否为目录
                if not os.path.isdir(zip_version_path) or not os.path.isdir(unzip_version_path):
                    continue
                
                print(f"正在处理 {category}/{package_name} (版本: {version})...")
                
                # 找到压缩包文件
                zip_files = [f for f in os.listdir(zip_version_path) if f.endswith(('.tgz', '.tar.gz', '.zip'))]
                if not zip_files:
                    print(f"警告: 在 {zip_version_path} 中找不到压缩包")
                    continue
                
                # 使用第一个找到的压缩包
                zip_file_path = os.path.join(zip_version_path, zip_files[0])
                
                # 运行Guarddog工具 (使用压缩包)
                guarddog_result = self.run_guarddog(zip_file_path, package_name, version, category)
                
                # 运行OSSGadget工具 (使用解压路径)
                ossgadget_result = self.run_ossgadget(unzip_version_path, package_name, version, category)
                
                # 如果两个工具都已处理过，则跳过计数
                if guarddog_result is None and ossgadget_result is None:
                    self.skipped_count += 1
                else:
                    self.processed_count += 1
                    
                print(f"完成处理 {category}/{package_name} (版本: {version})")
                
        except Exception as e:
            print(f"处理 {category}/{package_name} 时出错: {str(e)}")
    
    def process_all_packages(self, num_processes=NUM_PROCESSES):
        """使用多进程处理所有包"""
        # 获取所有包名
        benign_packages = os.listdir(self.zip_benign_path)
        malicious_packages = os.listdir(self.zip_malicious_path)
        
        # 创建任务列表
        tasks = []
        for package in benign_packages:
            tasks.append(("benign", package))
        for package in malicious_packages:
            tasks.append(("malware", package))
        
        print(f"共找到 {len(benign_packages)} 个良性包和 {len(malicious_packages)} 个恶意包")
        
        # 使用多进程处理任务
        if num_processes > 1 and tasks:
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.starmap(self.process_package, tasks)
        else:
            # 单进程模式
            for task in tasks:
                self.process_package(*task)
        
        print(f"所有包处理完成！新处理: {self.processed_count} 个，跳过已处理: {self.skipped_count} 个")

if __name__ == "__main__":
    # 清理可能的僵尸进程
    try:
        print("清理可能的僵尸进程...")
        cleanup_cmd = """
        pkill -f guarddog || true
        pkill -f oss-detect-backdoor || true
        """
        subprocess.call(cleanup_cmd, shell=True)
        print("清理完成")
    except:
        print("清理进程时出错，继续执行...")
    
    print(f"使用 {NUM_PROCESSES} 个进程进行检测，工具超时时间: {TOOL_TIMEOUT}秒")
    
    detector = NPMToolDetector()
    detector.process_all_packages()
