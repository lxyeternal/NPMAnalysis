#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从原始工具输出分析有安装脚本的包的误报情况

分析guarddog、ossgadget、genie三个工具的原始检测结果，
找出包含preinstall、postinstall、install脚本的包，
并统计这些包的误报率
"""

import os
import re
import json
import time
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class ScriptFalsePositiveAnalyzer:
    def __init__(self):
        self.tool_output_dir = "Codes/tool_detect/tool_output"
        self.tools = ["guarddog", "ossgadget", "genie"]
        
        # 存储结果
        self.script_packages = {}  # 工具 -> 脚本类型 -> {malware: set, benign: set}
        self.summary_stats = {}    # 工具 -> 统计信息
        
    def parse_detection_result(self, result_file: str) -> Dict:
        """
        解析单个检测结果文件
        """
        script_info = {
            'preinstall': False,
            'postinstall': False,
            'install': False,
            'has_scripts': False
        }
        
        try:
            with open(result_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 查找npm-install-script相关的行
                if 'npm-install-script' in content or 'install script' in content.lower():
                    script_info['has_scripts'] = True
                    
                    # 查找具体的脚本类型
                    if 'preinstall' in content.lower():
                        script_info['preinstall'] = True
                    if 'postinstall' in content.lower():
                        script_info['postinstall'] = True
                    if '"install"' in content.lower() or 'install script' in content.lower():
                        script_info['install'] = True
                        
        except Exception as e:
            print(f"读取文件失败 {result_file}: {e}")
            
        return script_info
    
    def scan_tool_output(self, tool_name: str) -> Dict:
        """
        扫描单个工具的所有检测结果
        """
        tool_dir = os.path.join(self.tool_output_dir, tool_name)
        results = {
            'malware': {
                'preinstall': set(),
                'postinstall': set(), 
                'install': set(),
                'any_script': set()
            },
            'benign': {
                'preinstall': set(),
                'postinstall': set(),
                'install': set(), 
                'any_script': set()
            },
            'processed_packages': 0,
            'script_packages_count': 0
        }
        
        if not os.path.exists(tool_dir):
            print(f"工具目录不存在: {tool_dir}")
            return results
            
        print(f"\n扫描 {tool_name} 的检测结果...")
        
        for label in ['malware', 'benign']:
            label_dir = os.path.join(tool_dir, label)
            if not os.path.exists(label_dir):
                continue
                
            print(f"  扫描 {label} 目录...")
            package_count = 0
            
            for package_name in os.listdir(label_dir):
                package_dir = os.path.join(label_dir, package_name)
                if not os.path.isdir(package_dir):
                    continue
                    
                package_count += 1
                if package_count % 100 == 0:
                    print(f"    已处理 {package_count} 个包...")
                
                # 扫描包的所有版本
                for version in os.listdir(package_dir):
                    version_dir = os.path.join(package_dir, version)
                    if not os.path.isdir(version_dir):
                        continue
                        
                    result_file = os.path.join(version_dir, 'result.txt')
                    if not os.path.exists(result_file):
                        # 有些工具可能有不同的输出文件名
                        possible_files = [
                            os.path.join(version_dir, f'{package_name}-{version}.csv'),
                            os.path.join(version_dir, 'result.json'),
                            os.path.join(version_dir, 'output.txt')
                        ]
                        result_file = None
                        for pf in possible_files:
                            if os.path.exists(pf):
                                result_file = pf
                                break
                        if not result_file:
                            continue
                    
                    # 解析检测结果
                    script_info = self.parse_detection_result(result_file)
                    results['processed_packages'] += 1
                    
                    package_key = f"{package_name}/{version}"
                    
                    if script_info['has_scripts']:
                        results['script_packages_count'] += 1
                        results[label]['any_script'].add(package_key)
                        
                        if script_info['preinstall']:
                            results[label]['preinstall'].add(package_key)
                        if script_info['postinstall']:
                            results[label]['postinstall'].add(package_key)
                        if script_info['install']:
                            results[label]['install'].add(package_key)
                            
                        print(f"    发现脚本包: {package_key} ({label}) - "
                              f"preinstall:{script_info['preinstall']}, "
                              f"postinstall:{script_info['postinstall']}, "
                              f"install:{script_info['install']}")
            
            print(f"  {label} 目录完成，处理了 {package_count} 个包")
        
        return results
    
    def calculate_false_positive_rates(self, results: Dict) -> Dict:
        """
        计算误报率
        """
        stats = {}
        
        for script_type in ['preinstall', 'postinstall', 'install', 'any_script']:
            malware_count = len(results['malware'][script_type])
            benign_count = len(results['benign'][script_type])
            total_count = malware_count + benign_count
            
            # 误报 = 被预测为恶意但实际是良性的包
            false_positives = results['benign'][script_type]  # 在benign目录但被工具检测的包都是误报
            false_positive_count = len(false_positives)
            
            # 误报率 = 误报数 / 总的良性包数
            false_positive_rate = (false_positive_count / benign_count * 100) if benign_count > 0 else 0
            
            # 检测率 = 正确检测的恶意包数 / 总的恶意包数  
            detection_rate = (malware_count / (malware_count + 0) * 100) if malware_count > 0 else 0
            
            stats[script_type] = {
                'total_packages': total_count,
                'malware_packages': malware_count,
                'benign_packages': benign_count,
                'false_positives': false_positive_count,
                'false_positive_rate': false_positive_rate,
                'detection_rate': detection_rate,
                'sample_false_positives': list(false_positives)[:10]  # 前10个示例
            }
        
        return stats
    
    def analyze_all_tools(self):
        """
        分析所有工具
        """
        print("开始分析所有工具的安装脚本误报情况")
        print("=" * 60)
        
        for tool_name in self.tools:
            results = self.scan_tool_output(tool_name)
            self.script_packages[tool_name] = results
            self.summary_stats[tool_name] = self.calculate_false_positive_rates(results)
            
            print(f"\n{tool_name} 扫描完成:")
            print(f"  总处理包数: {results['processed_packages']}")
            print(f"  有脚本包数: {results['script_packages_count']}")
    
    def generate_report(self) -> str:
        """
        生成分析报告
        """
        report = []
        report.append("=" * 80)
        report.append("三大工具安装脚本包误报分析报告")
        report.append("=" * 80)
        report.append("")
        
        # 总体统计
        report.append("总体统计:")
        report.append("-" * 60)
        report.append(f"{'工具':<12} {'总包数':<10} {'有脚本包':<10} {'脚本包占比':<12}")
        report.append("-" * 60)
        
        for tool_name in self.tools:
            if tool_name in self.script_packages:
                results = self.script_packages[tool_name]
                total_packages = results['processed_packages']
                script_packages = results['script_packages_count']
                script_ratio = (script_packages / total_packages * 100) if total_packages > 0 else 0
                
                report.append(f"{tool_name:<12} {total_packages:<10} {script_packages:<10} {script_ratio:<12.2f}%")
        
        report.append("")
        
        # 按脚本类型分析误报
        script_types = ['preinstall', 'postinstall', 'install', 'any_script']
        script_names = {
            'preinstall': 'preinstall脚本',
            'postinstall': 'postinstall脚本',
            'install': 'install脚本', 
            'any_script': '任意脚本'
        }
        
        for script_type in script_types:
            report.append(f"{script_names[script_type]} 包分析:")
            report.append("-" * 70)
            report.append(f"{'工具':<12} {'总数':<8} {'恶意':<8} {'良性':<8} {'误报数':<8} {'误报率':<10}")
            report.append("-" * 70)
            
            for tool_name in self.tools:
                if tool_name in self.summary_stats and script_type in self.summary_stats[tool_name]:
                    stats = self.summary_stats[tool_name][script_type]
                    report.append(f"{tool_name:<12} {stats['total_packages']:<8} "
                                f"{stats['malware_packages']:<8} {stats['benign_packages']:<8} "
                                f"{stats['false_positives']:<8} {stats['false_positive_rate']:<10.2f}%")
                else:
                    report.append(f"{tool_name:<12} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<10}")
            
            report.append("")
        
        # 关键发现
        report.append("关键发现:")
        report.append("-" * 30)
        
        for script_type in ['preinstall', 'postinstall', 'install']:
            script_name = script_names[script_type]
            min_fp_rate = float('inf')
            max_fp_rate = 0
            min_tool = None
            max_tool = None
            
            for tool_name in self.tools:
                if (tool_name in self.summary_stats and 
                    script_type in self.summary_stats[tool_name]):
                    fp_rate = self.summary_stats[tool_name][script_type]['false_positive_rate']
                    if fp_rate < min_fp_rate:
                        min_fp_rate = fp_rate
                        min_tool = tool_name
                    if fp_rate > max_fp_rate:
                        max_fp_rate = fp_rate
                        max_tool = tool_name
            
            if min_tool and max_tool:
                report.append(f"- {script_name}误报率最低: {min_tool} ({min_fp_rate:.2f}%)")
                report.append(f"- {script_name}误报率最高: {max_tool} ({max_fp_rate:.2f}%)")
        
        report.append("")
        
        # 误报示例
        report.append("误报包示例:")
        report.append("-" * 30)
        
        for tool_name in self.tools:
            if tool_name in self.summary_stats:
                report.append(f"\n{tool_name} 误报包示例:")
                for script_type in ['preinstall', 'postinstall', 'install']:
                    if script_type in self.summary_stats[tool_name]:
                        examples = self.summary_stats[tool_name][script_type]['sample_false_positives']
                        if examples:
                            example_names = [pkg.split('/')[0] for pkg in examples[:3]]
                            report.append(f"  {script_names[script_type]}: {', '.join(example_names)}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, report: str):
        """
        保存分析结果
        """
        # 保存详细数据
        try:
            # 转换set为list以便JSON序列化
            save_data = {}
            for tool_name, tool_data in self.script_packages.items():
                save_data[tool_name] = {
                    'processed_packages': tool_data['processed_packages'],
                    'script_packages_count': tool_data['script_packages_count']
                }
                for label in ['malware', 'benign']:
                    save_data[tool_name][label] = {}
                    for script_type, packages in tool_data[label].items():
                        save_data[tool_name][label][script_type] = list(packages)
            
            results = {
                'script_packages': save_data,
                'summary_stats': self.summary_stats,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open("script_false_positive_analysis_results.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print("详细结果已保存到: script_false_positive_analysis_results.json")
            
        except Exception as e:
            print(f"保存详细结果时出错: {e}")
        
        # 保存报告
        try:
            with open("script_false_positive_analysis_report.txt", 'w', encoding='utf-8') as f:
                f.write(report)
            print("报告已保存到: script_false_positive_analysis_report.txt")
        except Exception as e:
            print(f"保存报告时出错: {e}")
    
    def run_analysis(self):
        """
        运行完整分析
        """
        # 1. 分析所有工具
        self.analyze_all_tools()
        
        # 2. 生成报告
        report = self.generate_report()
        print("\n" + report)
        
        # 3. 保存结果
        self.save_results(report)
        
        print("\n分析完成!")


def main():
    """
    主函数
    """
    analyzer = ScriptFalsePositiveAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main() 