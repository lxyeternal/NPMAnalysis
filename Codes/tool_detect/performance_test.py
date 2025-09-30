#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import json
import statistics
import random
import re
from pathlib import Path
import argparse
from datetime import datetime

class PerformanceAnalyzer:
    def __init__(self):
        # 定义数据路径
        self.base_path = "/home2/wenbo/Documents/NPMAnalysis/Dataset"
        self.zip_benign_path = os.path.join(self.base_path, "zip_benign")
        self.zip_malicious_path = os.path.join(self.base_path, "zip_malware")
        self.unzip_benign_path = os.path.join(self.base_path, "unzip_benign")
        self.unzip_malicious_path = os.path.join(self.base_path, "unzip_malware")
        
        # 性能统计数据
        self.guarddog_times = []
        self.ossgadget_times = []
        self.guarddog_timeouts = 0
        self.ossgadget_timeouts = 0
        self.guarddog_errors = 0
        self.ossgadget_errors = 0
        
        # 简化记录，只保存基本信息
        self.test_results = []
        
        # 代码统计数据
        self.code_stats = {}  # {package_name: {'files': count, 'code_lines': count, 'analysis_time': seconds}}
        
        # 超时设置
        self.timeout = 300  # 5分钟超时
        
    def run_with_timing(self, cmd, tool_name, package_info):
        """运行命令并记录时间信息，和原tool_detect.py逻辑一致"""
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=self.timeout)
            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                'tool': tool_name,
                'package': f"{package_info['package']}-{package_info['version']}",
                'category': package_info['category'],
                'execution_time': execution_time,
                'success': process.returncode == 0,
                'timeout': False,
                'error': False
            }
            
            return result
            
        except subprocess.TimeoutExpired:
            process.kill()
            try:
                process.wait(timeout=5)
            except:
                pass
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                'tool': tool_name,
                'package': f"{package_info['package']}-{package_info['version']}",
                'category': package_info['category'],
                'execution_time': execution_time,
                'success': False,
                'timeout': True,
                'error': False
            }
            
            return result
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            result = {
                'tool': tool_name,
                'package': f"{package_info['package']}-{package_info['version']}",
                'category': package_info['category'],
                'execution_time': execution_time,
                'success': False,
                'timeout': False,
                'error': True
            }
            
            return result
    
    def test_guarddog(self, zip_file_path, package_info):
        """测试Guarddog工具性能"""
        cmd = ["guarddog", "npm", "scan", zip_file_path]
        print(f"测试Guarddog: {package_info['category']}/{package_info['package']}-{package_info['version']}")
        
        result = self.run_with_timing(cmd, "guarddog", package_info)
        
        if result['timeout']:
            self.guarddog_timeouts += 1
            print(f"  ⚠️  超时 ({result['execution_time']:.2f}s)")
        elif result['error']:
            self.guarddog_errors += 1
            print(f"  ❌ 错误 ({result['execution_time']:.2f}s)")
        elif result['success']:
            self.guarddog_times.append(result['execution_time'])
            print(f"  ✅ 成功 ({result['execution_time']:.2f}s)")
        else:
            self.guarddog_errors += 1
            print(f"  ❌ 失败 ({result['execution_time']:.2f}s)")
        
        self.test_results.append(result)
        return result
    
    def test_ossgadget(self, unzip_dir_path, package_info):
        """测试OSSGadget工具性能"""
        cmd = ["/home2/wenbo/Documents/NPMAnalysis/Tools/OSSGadget/oss-detect-backdoor", unzip_dir_path]
        print(f"测试OSSGadget: {package_info['category']}/{package_info['package']}-{package_info['version']}")
        
        result = self.run_with_timing(cmd, "ossgadget", package_info)
        
        if result['timeout']:
            self.ossgadget_timeouts += 1
            print(f"  ⚠️  超时 ({result['execution_time']:.2f}s)")
        elif result['error']:
            self.ossgadget_errors += 1
            print(f"  ❌ 错误 ({result['execution_time']:.2f}s)")
        elif result['success']:
            self.ossgadget_times.append(result['execution_time'])
            print(f"  ✅ 成功 ({result['execution_time']:.2f}s)")
        else:
            self.ossgadget_errors += 1
            print(f"  ❌ 失败 ({result['execution_time']:.2f}s)")
        
        self.test_results.append(result)
        return result
    
    def get_package_code_stats(self, unzip_path, package_info):
        """获取包的代码统计信息（不计入检测时间）"""
        package_key = f"{package_info['package']}-{package_info['version']}"
        
        try:
            # 使用cloc命令分析代码
            cmd = ["cloc", unzip_path]
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60  # cloc一般很快，60秒足够
            )
            
            if process.returncode == 0:
                # 解析cloc输出，寻找SUM行
                files_count, code_lines = self.parse_cloc_output(process.stdout)
                
                # 存储代码统计信息（不包含分析时间）
                self.code_stats[package_key] = {
                    'files': files_count,
                    'code_lines': code_lines,
                    'category': package_info['category']
                }
                
                return files_count, code_lines
            else:
                return 0, 0
                
        except subprocess.TimeoutExpired:
            return 0, 0
        except Exception as e:
            return 0, 0

    def analyze_package_code(self, unzip_path, package_info):
        """使用cloc分析包的代码统计信息"""
        package_key = f"{package_info['package']}-{package_info['version']}"
        print(f"分析代码统计: {package_info['category']}/{package_key}")
        
        start_time = time.time()
        
        try:
            # 使用cloc命令分析代码
            cmd = ["cloc", unzip_path]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=60)  # cloc一般很快，60秒足够
            end_time = time.time()
            analysis_time = end_time - start_time
            
            if process.returncode == 0:
                # 解析cloc输出，寻找SUM行
                files_count, code_lines = self.parse_cloc_output(stdout)
                
                self.code_stats[package_key] = {
                    'files': files_count,
                    'code_lines': code_lines,
                    'analysis_time': analysis_time,
                    'category': package_info['category']
                }
                
                print(f"  ✅ 分析完成: {files_count}个文件, {code_lines}行代码 ({analysis_time:.2f}s)")
                return True
            else:
                print(f"  ❌ cloc分析失败 ({analysis_time:.2f}s)")
                return False
                
        except subprocess.TimeoutExpired:
            process.kill()
            end_time = time.time()
            analysis_time = end_time - start_time
            print(f"  ⚠️  cloc分析超时 ({analysis_time:.2f}s)")
            return False
            
        except Exception as e:
            end_time = time.time()
            analysis_time = end_time - start_time
            print(f"  ❌ cloc分析出错: {str(e)} ({analysis_time:.2f}s)")
            return False
    
    def parse_cloc_output(self, cloc_output):
        """解析cloc输出，提取SUM行的files和code数据"""
        lines = cloc_output.strip().split('\n')
        
        for line in lines:
            if line.startswith('SUM:'):
                # 使用正则表达式提取数字
                # SUM行格式类似: "SUM:                             4             26             10            117"
                # 我们需要提取第一个数字(files)和最后一个数字(code)
                numbers = re.findall(r'\d+', line)
                if len(numbers) >= 4:
                    files_count = int(numbers[0])
                    code_lines = int(numbers[-1])  # 最后一个数字是code行数
                    return files_count, code_lines
        
        # 如果没找到SUM行，返回0
        return 0, 0
    
    def get_sample_packages(self, category, max_packages=10):
        """随机获取样本包进行测试"""
        if category == "benign":
            base_path = self.zip_benign_path
        else:
            base_path = self.zip_malicious_path
        
        packages = []
        
        # 收集所有可用的包版本
        all_package_versions = []
        package_names = os.listdir(base_path)
        
        for package_name in package_names:
            package_path = os.path.join(base_path, package_name)
            if os.path.isdir(package_path):
                versions = os.listdir(package_path)
                for version in versions:
                    version_path = os.path.join(package_path, version)
                    if os.path.isdir(version_path):
                        # 检查是否有压缩包文件和对应的解压目录
                        zip_files = [f for f in os.listdir(version_path) if f.endswith(('.tgz', '.tar.gz', '.zip'))]
                        unzip_path = os.path.join(
                            self.unzip_benign_path if category == "benign" else self.unzip_malicious_path,
                            package_name, version
                        )
                        
                        if zip_files and os.path.exists(unzip_path):
                            all_package_versions.append({
                                'category': category,
                                'package': package_name,
                                'version': version,
                                'zip_path': os.path.join(version_path, zip_files[0]),
                                'unzip_path': unzip_path
                            })
        
        # 随机选择指定数量的包
        if len(all_package_versions) <= max_packages:
            packages = all_package_versions
        else:
            packages = random.sample(all_package_versions, max_packages)
        
        print(f"从{len(all_package_versions)}个{category}包版本中随机选择了{len(packages)}个")
        return packages
    
    def run_performance_test(self, max_benign=5, max_malicious=5, test_guarddog=True, test_ossgadget=True):
        """运行性能测试"""
        print("=" * 60)
        print("NPM工具性能测试开始")
        print("=" * 60)
        print(f"超时设置: {self.timeout}秒")
        print(f"测试范围: 最多{max_benign}个良性包, {max_malicious}个恶意包")
        
        tools_to_test = []
        if test_guarddog:
            tools_to_test.append("Guarddog")
        if test_ossgadget:
            tools_to_test.append("OSSGadget")
        print(f"测试工具: {', '.join(tools_to_test)}")
        print()
        
        # 获取测试样本
        benign_packages = self.get_sample_packages("benign", max_benign)
        malicious_packages = self.get_sample_packages("malware", max_malicious)
        
        all_packages = benign_packages + malicious_packages
        total_packages = len(all_packages)
        
        print(f"找到 {len(benign_packages)} 个良性包版本, {len(malicious_packages)} 个恶意包版本")
        print(f"总计测试 {total_packages} 个包版本")
        print()
        
        # 开始测试
        test_start_time = time.time()
        
        for i, package_info in enumerate(all_packages, 1):
            print(f"[{i}/{total_packages}] 处理: {package_info['category']}/{package_info['package']}-{package_info['version']}")
            
            # 先进行代码统计分析（不计入检测时间）
            files_count = 0
            code_lines = 0
            if os.path.exists(package_info['unzip_path']):
                print(f"  📊 分析代码统计...")
                files_count, code_lines = self.get_package_code_stats(package_info['unzip_path'], package_info)
                print(f"  📄 文件数: {files_count}个, 代码行数: {code_lines}行")
            else:
                print(f"  ⚠️  找不到解压目录进行代码统计: {package_info['unzip_path']}")
            
            # 测试Guarddog
            if test_guarddog and os.path.exists(package_info['zip_path']):
                self.test_guarddog(package_info['zip_path'], package_info)
            elif test_guarddog:
                print(f"  ⚠️  找不到压缩包: {package_info['zip_path']}")
            
            # 测试OSSGadget
            if test_ossgadget and os.path.exists(package_info['unzip_path']):
                self.test_ossgadget(package_info['unzip_path'], package_info)
            elif test_ossgadget:
                print(f"  ⚠️  找不到解压目录: {package_info['unzip_path']}")
            
            print()
        
        test_total_time = time.time() - test_start_time
        
        # 生成性能测试报告
        self.generate_performance_report(test_total_time)
        
        # 生成代码统计报告（代码统计已在检测过程中完成）
        if self.code_stats:
            successful_analysis = len(self.code_stats)
            self.generate_code_analysis_report(0, successful_analysis, total_packages)
    
    def generate_performance_report(self, total_test_time):
        """生成性能测试报告"""
        print("=" * 60)
        print("性能测试报告")
        print("=" * 60)
        
        # Guarddog统计
        print("\n🔍 Guarddog 性能统计:")
        print(f"  成功执行: {len(self.guarddog_times)} 次")
        print(f"  超时次数: {self.guarddog_timeouts} 次")
        print(f"  错误次数: {self.guarddog_errors} 次")
        
        if self.guarddog_times:
            print(f"  平均执行时间: {statistics.mean(self.guarddog_times):.2f}秒")
            print(f"  中位数执行时间: {statistics.median(self.guarddog_times):.2f}秒")
            print(f"  最短执行时间: {min(self.guarddog_times):.2f}秒")
            print(f"  最长执行时间: {max(self.guarddog_times):.2f}秒")
            if len(self.guarddog_times) > 1:
                print(f"  标准差: {statistics.stdev(self.guarddog_times):.2f}秒")
        
        # OSSGadget统计
        print("\n🛡️  OSSGadget 性能统计:")
        print(f"  成功执行: {len(self.ossgadget_times)} 次")
        print(f"  超时次数: {self.ossgadget_timeouts} 次")
        print(f"  错误次数: {self.ossgadget_errors} 次")
        
        if self.ossgadget_times:
            print(f"  平均执行时间: {statistics.mean(self.ossgadget_times):.2f}秒")
            print(f"  中位数执行时间: {statistics.median(self.ossgadget_times):.2f}秒")
            print(f"  最短执行时间: {min(self.ossgadget_times):.2f}秒")
            print(f"  最长执行时间: {max(self.ossgadget_times):.2f}秒")
            if len(self.ossgadget_times) > 1:
                print(f"  标准差: {statistics.stdev(self.ossgadget_times):.2f}秒")
        
        # 总体统计
        print(f"\n📊 总体统计:")
        print(f"  总测试时间: {total_test_time:.2f}秒")
        print(f"  测试包数量: {len(set(r['package'] for r in self.test_results))}")
        
        # 性能对比
        if self.guarddog_times and self.ossgadget_times:
            guarddog_avg = statistics.mean(self.guarddog_times)
            ossgadget_avg = statistics.mean(self.ossgadget_times)
            print(f"\n🏆 性能对比:")
            print(f"  Guarddog平均: {guarddog_avg:.2f}秒")
            print(f"  OSSGadget平均: {ossgadget_avg:.2f}秒")
            if guarddog_avg < ossgadget_avg:
                print(f"  Guarddog比OSSGadget快 {((ossgadget_avg - guarddog_avg) / ossgadget_avg * 100):.1f}%")
            else:
                print(f"  OSSGadget比Guarddog快 {((guarddog_avg - ossgadget_avg) / guarddog_avg * 100):.1f}%")
    
    def generate_code_analysis_report(self, total_analysis_time, successful_analysis, total_packages):
        """生成代码统计分析报告"""
        print("=" * 60)
        print("代码统计分析报告")
        print("=" * 60)
        
        if not self.code_stats:
            print("没有成功分析的代码统计数据")
            return
        
        # 按类别分组统计
        benign_stats = [stats for stats in self.code_stats.values() if stats['category'] == 'benign']
        malware_stats = [stats for stats in self.code_stats.values() if stats['category'] == 'malware']
        
        print(f"\n📊 总体统计:")
        print(f"  成功分析包数: {successful_analysis}/{total_packages}")
        print(f"  分析成功率: {(successful_analysis/total_packages)*100:.1f}%")
        
        # 计算总体平均统计
        all_files = [stats['files'] for stats in self.code_stats.values()]
        all_code_lines = [stats['code_lines'] for stats in self.code_stats.values()]
        
        if all_files:
            print(f"  平均每个包文件数: {statistics.mean(all_files):.1f}个")
            print(f"  平均每个包代码行数: {statistics.mean(all_code_lines):.1f}行")
        
        # 良性包统计
        if benign_stats:
            print(f"\n✅ 良性包代码统计 ({len(benign_stats)}个包):")
            self.print_code_category_stats(benign_stats)
        
        # 恶意包统计
        if malware_stats:
            print(f"\n⚠️  恶意包代码统计 ({len(malware_stats)}个包):")
            self.print_code_category_stats(malware_stats)
        
        # 对比分析
        if benign_stats and malware_stats:
            print(f"\n🔍 良性vs恶意包对比:")
            benign_avg_files = statistics.mean([s['files'] for s in benign_stats])
            malware_avg_files = statistics.mean([s['files'] for s in malware_stats])
            benign_avg_lines = statistics.mean([s['code_lines'] for s in benign_stats])
            malware_avg_lines = statistics.mean([s['code_lines'] for s in malware_stats])
            
            print(f"  良性包平均文件数: {benign_avg_files:.1f}")
            print(f"  恶意包平均文件数: {malware_avg_files:.1f}")
            print(f"  良性包平均代码行数: {benign_avg_lines:.1f}")
            print(f"  恶意包平均代码行数: {malware_avg_lines:.1f}")
        
        # 详细包信息
        print(f"\n📋 详细包信息:")
        print(f"{'包名':<35} {'类别':<8} {'文件数':<8} {'代码行数':<10}")
        print("-" * 65)
        
        total_files = 0
        total_code_lines = 0
        
        # 按类别排序显示
        sorted_stats = sorted(self.code_stats.items(), key=lambda x: (x[1]['category'], x[0]))
        for package_name, stats in sorted_stats:
            print(f"{package_name:<35} {stats['category']:<8} {stats['files']:<8} {stats['code_lines']:<10}")
            total_files += stats['files']
            total_code_lines += stats['code_lines']
        
        print("-" * 65)
        print(f"{'总计':<35} {'ALL':<8} {total_files:<8} {total_code_lines:<10}")
        
        # 额外统计信息
        print(f"\n📈 汇总统计:")
        print(f"  总分析包数: {len(self.code_stats)}个")
        print(f"  总文件数: {total_files}个")
        print(f"  总代码行数: {total_code_lines}行")
        print(f"  平均每包文件数: {total_files/len(self.code_stats):.1f}个")
        print(f"  平均每包代码行数: {total_code_lines/len(self.code_stats):.1f}行")
    
    def print_code_category_stats(self, stats_list):
        """打印某类别的代码统计信息"""
        if not stats_list:
            return
        
        files_counts = [s['files'] for s in stats_list]
        code_lines = [s['code_lines'] for s in stats_list]
        
        print(f"    文件数统计:")
        print(f"      平均: {statistics.mean(files_counts):.1f}个")
        print(f"      中位数: {statistics.median(files_counts):.1f}个")
        print(f"      最少: {min(files_counts)}个")
        print(f"      最多: {max(files_counts)}个")
        print(f"      总计: {sum(files_counts)}个")
        
        print(f"    代码行数统计:")
        print(f"      平均: {statistics.mean(code_lines):.1f}行")
        print(f"      中位数: {statistics.median(code_lines):.1f}行")
        print(f"      最少: {min(code_lines)}行")
        print(f"      最多: {max(code_lines)}行")
        print(f"      总计: {sum(code_lines)}行")
        

def main():
    parser = argparse.ArgumentParser(description='NPM工具性能测试 - 单线程版本')
    parser.add_argument('--total', type=int, help='总测试包数量，自动平分良性和恶意包 (如: --total 1000)')
    parser.add_argument('--benign', type=int, default=5, help='测试的良性包数量 (默认: 5)')
    parser.add_argument('--malicious', type=int, default=5, help='测试的恶意包数量 (默认: 5)')
    parser.add_argument('--timeout', type=int, default=300, help='超时时间(秒) (默认: 300)')
    parser.add_argument('--guarddog-only', action='store_true', help='只测试Guarddog')
    parser.add_argument('--ossgadget-only', action='store_true', help='只测试OSSGadget')
    
    args = parser.parse_args()
    
    analyzer = PerformanceAnalyzer()
    analyzer.timeout = args.timeout
    
    # 如果指定了总数量，就平分良性和恶意包
    if args.total:
        benign_count = args.total // 2
        malicious_count = args.total - benign_count  # 处理奇数情况
        print(f"总测试包数: {args.total}, 良性包: {benign_count}, 恶意包: {malicious_count}")
    else:
        benign_count = args.benign
        malicious_count = args.malicious
    
    test_guarddog = not args.ossgadget_only
    test_ossgadget = not args.guarddog_only
    
    analyzer.run_performance_test(
        max_benign=benign_count,
        max_malicious=malicious_count,
        test_guarddog=test_guarddog,
        test_ossgadget=test_ossgadget
    )

if __name__ == "__main__":
    main()
