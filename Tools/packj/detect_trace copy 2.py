#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
import argparse
import subprocess
import csv
import tarfile
import shutil
from datetime import datetime
import re
import multiprocessing
from multiprocessing import Pool, Lock
from functools import partial
import time
import json

# 在脚本开头
import os

# 创建SSH配置目录和文件
os.makedirs(os.path.expanduser('~/.ssh'), exist_ok=True)
known_hosts_path = os.path.expanduser('~/.ssh/known_hosts')
ssh_config_path = os.path.expanduser('~/.ssh/config')

# 创建或追加SSH配置
with open(ssh_config_path, 'a+') as config_file:
    config_file.seek(0)
    content = config_file.read()
    if 'StrictHostKeyChecking no' not in content:
        config_file.write("\nHost *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n")

# 确保SSH目录权限正确
try:
    os.chmod(os.path.expanduser('~/.ssh'), 0o700)
    os.chmod(ssh_config_path, 0o600)
    if os.path.exists(known_hosts_path):
        os.chmod(known_hosts_path, 0o600)
except:
    pass

# 设置Git环境变量
os.environ['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
os.environ['GIT_TERMINAL_PROMPT'] = '0'

def get_config():
    """直接设置配置参数，替代命令行解析"""
    config = argparse.Namespace()
    
    # ===== 修改以下参数 =====
    # 包含NPM压缩包的目录路径
    config.dir = "/home/kali/desktop/NPM/zip_malware/"
    #config.dir = "/home/kali/desktop/1/"
    config.github_token = "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"
    # 报告输出目录
    config.output = "/home/kali/desktop/MalDetect/tools/packj-main/packj/result_trace/malware"
    # 是否启用动态跟踪分析
    config.trace = True
    
    # Packj工具的路径
    config.packj_path = "/home/kali/desktop/MalDetect/tools/packj-main"
    
    # 并行处理的进程数 (设置为0将使用CPU核心数)
    config.workers = 6
    # ===== 修改结束 =====
    
    return config
    
def cleanup_old_dirs(base_dir):
    for root, dirs, _ in os.walk(base_dir):
        for d in dirs:
            if d.startswith("extracted_"):
                try:
                    shutil.rmtree(os.path.join(root, d))
                    print(f"已清理旧临时目录: {d}")
                except:
                    pass

def setup_environment(output_dir):
    """创建输出目录"""
    os.makedirs(output_dir, exist_ok=True)
    print(f"报告将保存在: {output_dir}")



def extract_package(tgz_file, extract_dir):
    """解压NPM包到指定目录"""
    try:
        os.makedirs(extract_dir, exist_ok=True)
        
        with tarfile.open(tgz_file, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
        return True
    except Exception as e:
        print(f"解压 {tgz_file} 失败: {e}")
        return False


def run_packj_audit(package_json_path, output_file, packj_path, use_trace=False, use_local_mode=True,github_token=None):
    """运行Packj审计工具，并自动处理所有交互提示"""
    # 设置环境变量避免Git提示
    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    env['GIT_TERMINAL_PROMPT'] = '0'
    
    cmd = ['proxychains4', sys.executable, os.path.join(packj_path, 'main.py'), 'audit']
    
    # 添加 GitHub 令牌配置
    if github_token:
        packj_config_dir = os.path.expanduser('~/.packj')
        os.makedirs(packj_config_dir, exist_ok=True)
        config_file = os.path.join(packj_config_dir, 'config.json')
        
        config_data = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
            except:
                config_data = {}
        
        config_data['github_token'] = github_token
        
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
    
    if use_trace:
        cmd.append('--trace')
    
    # 根据模式选择不同的命令行参数格式
    if use_local_mode:
        # 使用本地nodejs模式 (-p local_nodejs:路径)
        project_dir = os.path.dirname(package_json_path) if os.path.isfile(package_json_path) else package_json_path
        cmd.extend(['-p', f'local_nodejs:{project_dir}/package'])
    else:
        # 使用传统模式 (-f npm:package.json路径)
        cmd.extend(['-f', f'npm:{package_json_path}'])
        
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置超时时间，避免无限等待
        timeout = 600  # 5分钟超时
        
        if use_trace:
            with open(output_file, 'w') as f:
                process = subprocess.Popen(
                    cmd, 
                    stdout=f, 
                    stderr=subprocess.STDOUT, 
                    stdin=subprocess.PIPE,
                    universal_newlines=True,
                    env=env
                )
                # 自动回答所有提示
                try:
                    out, err = process.communicate(input='y', timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    return False, None
        else:
            with open(output_file, 'w') as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=True, env=env, timeout=timeout)
                
        return True, output_file
    except subprocess.TimeoutExpired:
        print(f"Packj审计超时: {package_json_path}")
        return False, None
    except Exception as e:
        print(f"Packj审计失败: {package_json_path}, 错误: {e}")
        return False, None

def check_results(output_file):
    """检查审计结果是否发现风险"""
    try:
        with open(output_file, 'r') as f:
            content = f.read()
        
        risk_pattern = re.compile(r'(\d+) risk\(s\) apply to you')
        match = risk_pattern.search(content)
        
        if match:
            risk_count = int(match.group(1))
            return True, f"发现 {risk_count} 个风险，包被标记为不可取!"
        
        return False, "未发现风险"
    except Exception as e:
        return False, f"检查结果时出错: {e}"


def find_tgz_files(directory):
    """递归查找目录中所有的.tgz文件"""
    tgz_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.tgz'):
                tgz_files.append(os.path.join(root, file))
    return tgz_files

from multiprocessing import Lock
print_lock = Lock()

def process_package(pkg_file, base_dir, output_dir, packj_path, use_trace=False, use_local_mode=True,github_token=None):
    """处理单个NPM包的完整流程，用于并行执行"""
    # 获取包信息
    pkg_name = os.path.basename(pkg_file)
    rel_path = os.path.relpath(pkg_file, base_dir)
    rel_dir = os.path.dirname(rel_path)
    
    # 使用锁同步输出，避免多进程打印混乱
    with print_lock:
        print(f"⚡ 开始检测: {rel_path}")
    
    # 初始化结果
    result = {
        'file': pkg_file,
        'rel_path': os.path.relpath(pkg_file, base_dir),
        'success': False,
        'has_risk': False,
        'error': None
    }
    
    
    # 在原目录下创建解压目录
    extract_dir = os.path.join(os.path.dirname(pkg_file), f"extracted_{pkg_name}")
    
    try:
        # 解压包
        if not extract_package(pkg_file, extract_dir):
            result['error'] = "解压失败"
            return result
        
        # 生成输出文件路径
        output_name = pkg_name.replace('.tgz', '.txt')
        output_path = os.path.join(rel_dir, output_name) if rel_dir else output_name
        output_file = os.path.join(output_dir, output_path)
        
        # 直接使用解压目录运行审计，不需要专门查找package.json
        success, actual_output_file = run_packj_audit(extract_dir, output_file, packj_path, use_trace, use_local_mode,github_token)
        if not success:
            result['error'] = "审计失败"
            return result
        
        # 检查结果
        has_risk, risk_info = check_results(actual_output_file if actual_output_file else output_file)
        result['success'] = True
        result['has_risk'] = has_risk
        result['risk_info'] = risk_info
        
        return result
    
    except Exception as e:
        result['error'] = str(e)
        return result
    
    finally:
        # 清理解压目录，添加错误处理
        if os.path.exists(extract_dir):
            try:
                shutil.rmtree(extract_dir)
            except PermissionError as e:
                print(f"警告: 无法删除目录 {extract_dir}: {e}")
                # 尝试修复权限后再次删除
                try:
                    # 设置可写权限
                    for root, dirs, files in os.walk(extract_dir):
                        for d in dirs:
                            dir_path = os.path.join(root, d)
                            try:
                                os.chmod(dir_path, 0o755)  # rwxr-xr-x
                            except:
                                pass
                        for f in files:
                            file_path = os.path.join(root, f)
                            try:
                                os.chmod(file_path, 0o644)  # rw-r--r--
                            except:
                                pass
                    
                    # 再次尝试删除
                    shutil.rmtree(extract_dir)
                    print(f"已清理目录 {extract_dir}")
                except Exception:
                    # 如果仍然失败，放弃并继续
                    print(f"无法清理目录 {extract_dir}，将继续处理其他包")
            except Exception as e:
                # 捕获其他可能的异常
                print(f"清理目录时出错 {extract_dir}: {e}")

def process_batch(current_batch, workers, process_func, csv_file, batch_start, total_packages,start_time):
    """处理单个批次的NPM包"""
    batch_suspicious = 0
    batch_failed = 0
    total_processed = batch_start
    
    with open(csv_file, 'a', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        
        # 使用多进程池并行处理包，但逐个接收并处理结果
        with Pool(processes=workers) as pool:
            for result in pool.imap_unordered(process_func, current_batch):
                total_processed += 1
                rel_path = result['rel_path']
                
                # 实时处理每个结果
                if not result['success']:
                    batch_failed += 1
                    csv_writer.writerow([rel_path, "0"])  # 失败，默认为非恶意
                    print(f"[{total_processed}/{total_packages}] ❌ 处理失败: {rel_path}, 原因: {result['error']}")
                elif result['has_risk']:
                    batch_suspicious += 1
                    csv_writer.writerow([rel_path, "1"])  # 标记为恶意
                    print(f"[{total_processed}/{total_packages}] ⚠️ 发现风险: {rel_path}, {result['risk_info']}")
                else:
                    csv_writer.writerow([rel_path, "0"])  # 标记为非恶意
                    print(f"[{total_processed}/{total_packages}] ✓ 未发现风险: {rel_path}")
                
                csv_f.flush()
            
                # 每处理10个包就确保写入磁盘（fsync操作较慢，不必每次都执行）
                if total_processed % 10 == 0:
                    os.fsync(csv_f.fileno())
                
                # 每处理100个包显示一次进度统计
                if total_processed % 100 == 0:
                    elapsed = time.time() - start_time
                    avg_time = elapsed / total_processed
                    remaining = avg_time * (total_packages - total_processed)
                    print(f"进度: {total_processed}/{total_packages} ({total_processed/total_packages*100:.1f}%), "
                          f"用时: {elapsed:.1f}秒, 预计剩余: {remaining:.1f}秒")
    
    return batch_suspicious, batch_failed

def main():
    # 使用硬编码配置替代命令行参数
    args = get_config()
    
    # 设置Git和SSH不进行主机验证，避免交互式提示
    os.environ['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    os.environ['GIT_TERMINAL_PROMPT'] = '0'
    
    # 预处理常见Git托管网站的主机验证
    try:
        with open(os.devnull, 'w') as devnull:
            for host in ['github.com', 'gitlab.com', 'bitbucket.org', 'gitlab.beecode.cn']:
                subprocess.run(
                    f'ssh-keyscan -H {host} >> ~/.ssh/known_hosts',
                    shell=True, 
                    stdout=devnull, 
                    stderr=devnull
                )
        print("已预处理Git主机验证")
    except:
        pass
    # 检查必需参数
    if not args.dir or not os.path.exists(args.dir):
        print(f"错误: 目录 '{args.dir}' 不存在，请在脚本中修改 config.dir 参数")
        return 1
    
    # 设置环境
    setup_environment(args.output)
    cleanup_old_dirs(args.dir)
    
    # 查找所有NPM包
    npm_packages = find_tgz_files(args.dir)
    if not npm_packages:
        print(f"错误: 在 {args.dir} 中没有找到NPM包(.tgz文件)")
        return 1
    
    # 分批处理，每批500个包
    batch_size = 500
    total_packages = len(npm_packages)
    all_suspicious = 0
    all_failed = 0
    start_time = time.time()
    
    # 准备CSV文件头
    csv_file = os.path.join(args.output, "npm_packages_analysis.csv")
    with open(csv_file, 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerow(["包路径", "恶意标识(1=恶意,0=非恶意)"])
    
    # 按批次处理
    for batch_num, batch_start in enumerate(range(0, total_packages, batch_size)):
        batch_end = min(batch_start + batch_size, total_packages)
        current_batch = npm_packages[batch_start:batch_end]
        
        print(f"\n=== 开始处理批次 {batch_num+1}/{(total_packages-1)//batch_size + 1} ===")
        print(f"批次范围: {batch_start+1}-{batch_end} (共 {len(current_batch)} 个包)")
        
        # 确定并行进程数
        workers = args.workers if args.workers > 0 else multiprocessing.cpu_count()
        
        # 每批次使用一个新的进程池
        process_func = partial(
            process_package,
            base_dir=args.dir,
            output_dir=args.output,
            packj_path=args.packj_path,
            use_trace=args.trace,
            github_token=args.github_token
        )
        
        # 处理当前批次
        batch_suspicious, batch_failed = process_batch(
            current_batch, workers, process_func, csv_file, 
            batch_start, total_packages, start_time
        )
        
        all_suspicious += batch_suspicious
        all_failed += batch_failed
        
        # 强制垃圾回收
        import gc
        gc.collect()
        print(f"批次 {batch_num+1} 完成，已强制垃圾回收")
        
    # 计算总时间并打印最终统计
    total_time = time.time() - start_time
    print("\n==== 检测完成 ====")
    print(f"总共检测: {total_packages} 个包")
    print(f"可疑包数: {all_suspicious} 个")
    print(f"失败检测: {all_failed} 个")
    print(f"总耗时: {total_time:.2f} 秒 (平均每个包 {total_time/total_packages:.2f} 秒)")
    print(f"详细报告保存在: {args.output}")
    print(f"CSV分析报告: {csv_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())