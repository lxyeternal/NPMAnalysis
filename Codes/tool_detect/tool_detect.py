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
        self.base_path = "/home/wenbo/NPMAnalysis/Dataset"
        self.zip_benign_path = os.path.join(self.base_path, "zip_benign")
        self.zip_malicious_path = os.path.join(self.base_path, "zip_malware")
        
        # 定义输出路径
        self.output_base = "/home/wenbo/NPMAnalysis/Codes/tool_detect/tool_output"
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
    
    def _get_package_info_from_path(self, zip_file_path):
        """从压缩包路径获取包名、版本和路径信息"""
        parts = zip_file_path.split(os.sep)
        
        # 判断路径结构类型
        if len(parts) >= 3 and parts[-3] in ["zip_benign", "zip_malware"]:
            # 结构是 .../zip_benign/package_name/version/file.tgz
            package_name = parts[-3]
            version = parts[-2]
            file_name = parts[-1]
        else:
            # 只有文件名，直接从文件名解析
            file_name = os.path.basename(zip_file_path)
            package_name, version = self._parse_filename(file_name)
            
        return package_name, version, file_name
    
    def _parse_filename(self, file_name):
        """从文件名解析包名和版本"""
        # 移除扩展名
        if file_name.endswith('.tgz'):
            base_name = file_name[:-4]
        elif file_name.endswith('.tar.gz'):
            base_name = file_name[:-7]
        elif file_name.endswith('.zip'):
            base_name = file_name[:-4]
        else:
            base_name = file_name
            
        # 尝试分离包名和版本
        parts = base_name.rsplit('-', 1)
        if len(parts) == 2 and parts[1][0].isdigit():
            package_name, version = parts
            return package_name, version
        else:
            # 如果无法分离版本，则将整个名称作为包名
            return base_name, ""
    
    def _create_output_path(self, tool, category, package_name, version, original_filename):
        """创建输出文件路径，保持原始结构"""
        base_dir = self.output_paths[tool][category]
        
        # 创建包名文件夹
        package_dir = os.path.join(base_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        
        # 如果有版本，创建版本文件夹
        if version:
            version_dir = os.path.join(package_dir, version)
            os.makedirs(version_dir, exist_ok=True)
            
            # 输出文件名是原始文件名但扩展名改为.txt
            output_filename = os.path.splitext(original_filename)[0] + '.txt'
            return os.path.join(version_dir, output_filename)
        else:
            # 如果没有版本，直接在包名文件夹下创建文件
            output_filename = os.path.splitext(original_filename)[0] + '.txt'
            return os.path.join(package_dir, output_filename)
    
    def run_guarddog(self, zip_file_path, data_type):
        """运行Guarddog工具并保存结果"""
        package_name, version, original_filename = self._get_package_info_from_path(zip_file_path)
        output_file = self._create_output_path("guarddog", data_type, package_name, version, original_filename)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 检查输出文件是否已存在
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"跳过已处理的Guarddog检测: {original_filename}")
            return None
            
        cmd = ["guarddog", "npm", "scan", zip_file_path]
        print(f"开始Guarddog检测: {original_filename}")
        return_code, stdout, stderr, execution_time = run_with_timeout(cmd)
        
        if return_code == -1:  # 超时
            print(f"Guarddog检测超时: {original_filename}, 跳过")
            return None
        else:
            output = stdout if stdout.strip() else "benign"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Guarddog检测完成: {original_filename}, 用时: {execution_time:.2f}秒")
            return output
    
    def run_ossgadget(self, zip_file_path, data_type):
        """运行OSS Gadget工具并保存结果"""
        package_name, version, original_filename = self._get_package_info_from_path(zip_file_path)
        output_file = self._create_output_path("ossgadget", data_type, package_name, version, original_filename)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 检查输出文件是否已存在
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"跳过已处理的OSSGadget检测: {original_filename}")
            return None
            
        cmd = ["/home/wenbo/NPMAnalysis/Tools/OSSGadget/oss-detect-backdoor", zip_file_path]
        print(f"开始OSSGadget检测: {original_filename}")
        return_code, stdout, stderr, execution_time = run_with_timeout(cmd)
        
        if return_code == -1:  # 超时
            print(f"OSSGadget检测超时: {original_filename}, 跳过")
            return None
        else:
            output = stdout if stdout.strip() else "benign"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"OSSGadget检测完成: {original_filename}, 用时: {execution_time:.2f}秒")
            return output
    
    def find_all_zip_files(self, base_dir):
        """递归查找目录下所有压缩包文件"""
        zip_files = []
        
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(('.tgz', '.tar.gz', '.zip')):
                    zip_files.append(os.path.join(root, file))
                    
        return zip_files
    
    def process_zip_file(self, data_type, zip_file_path):
        """处理单个压缩包，调用所有检测工具并保存结果"""
        try:
            if not os.path.exists(zip_file_path):
                print(f"警告: 找不到压缩包 {zip_file_path}")
                return
                
            package_name, version, file_name = self._get_package_info_from_path(zip_file_path)
            print(f"正在处理 {data_type}/{package_name} (版本: {version or '未知'})...")
            
            # 运行Guarddog工具
            guarddog_result = self.run_guarddog(zip_file_path, data_type)
            
            # 运行OSSGadget工具
            ossgadget_result = self.run_ossgadget(zip_file_path, data_type)
            
            # 如果两个工具都已处理过，则跳过计数
            if guarddog_result is None and ossgadget_result is None:
                self.skipped_count += 1
            else:
                self.processed_count += 1
                
            print(f"完成处理 {data_type}/{package_name} (版本: {version or '未知'})")
            
        except Exception as e:
            print(f"处理 {zip_file_path} 时出错: {str(e)}")
    
    def process_all_zips(self, num_processes=NUM_PROCESSES):
        """使用多进程处理所有压缩包"""
        # 递归获取所有压缩包文件
        benign_zips = self.find_all_zip_files(self.zip_benign_path)
        malware_zips = self.find_all_zip_files(self.zip_malicious_path)
        
        # 创建任务列表
        tasks = []
        for zip_file in benign_zips:
            tasks.append(("benign", zip_file))
        for zip_file in malware_zips:
            tasks.append(("malware", zip_file))
        
        print(f"共找到 {len(benign_zips)} 个良性样本和 {len(malware_zips)} 个恶意样本")
        
        # 使用多进程处理任务
        if num_processes > 1 and tasks:
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.starmap(self.process_zip_file, tasks)
        else:
            # 单进程模式，可以统计处理和跳过的数量
            for task in tasks:
                self.process_zip_file(*task)
        
        print(f"所有样本处理完成！新处理: {self.processed_count} 个，跳过已处理: {self.skipped_count} 个")

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
    detector.process_all_zips()
