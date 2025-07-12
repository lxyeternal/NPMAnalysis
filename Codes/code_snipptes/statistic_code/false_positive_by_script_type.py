#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按安装脚本类型分析误报

分析guarddog、ossgadget、genie三个工具的误报包中，
哪些包含preinstall、postinstall、install脚本
"""

import json
import requests
import time
from typing import Dict, List, Set
from collections import defaultdict


class FalsePositiveScriptAnalyzer:
    def __init__(self):
        self.false_positive_reports = {
            "guarddog": "Codes/tool_detect/tool_output_statistic/reports/stats_output/guarddog/false_positives.json",
            "ossgadget": "Codes/tool_detect/tool_output_statistic/reports/stats_output/ossgadget/false_positives.json",
            "genie": "Codes/tool_detect/tool_output_statistic/reports/stats_output/genie/false_positives.json"
        }
        
        # 缓存已查询的包信息，避免重复请求
        self.package_cache = {}
        
    def load_false_positive_reports(self) -> Dict[str, Dict]:
        """
        加载三个工具的误报报告
        """
        reports = {}
        
        for tool_name, report_file in self.false_positive_reports.items():
            print(f"正在加载 {tool_name} 的误报报告...")
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    reports[tool_name] = json.load(f)
                print(f"成功加载 {tool_name} 误报报告，包含 {len(reports[tool_name])} 个误报包")
            except FileNotFoundError:
                print(f"警告: 找不到 {tool_name} 的误报报告文件: {report_file}")
                reports[tool_name] = {}
            except Exception as e:
                print(f"加载 {tool_name} 误报报告时出错: {e}")
                reports[tool_name] = {}
                
        return reports
    
    def get_package_scripts(self, package_name: str, version: str) -> Dict[str, bool]:
        """
        从NPM注册表获取包的脚本信息
        """
        package_key = f"{package_name}@{version}"
        
        # 检查缓存
        if package_key in self.package_cache:
            return self.package_cache[package_key]
        
        scripts_info = {
            'preinstall': False,
            'postinstall': False,
            'install': False,
            'has_any_script': False
        }
        
        # 跳过特殊包名
        if '##' in package_name or len(package_name) > 100:
            self.package_cache[package_key] = scripts_info
            return scripts_info
        
        try:
            url = f"https://registry.npmjs.org/{package_name}/{version}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'scripts' in data:
                    scripts = data['scripts']
                    scripts_info['preinstall'] = 'preinstall' in scripts
                    scripts_info['postinstall'] = 'postinstall' in scripts
                    scripts_info['install'] = 'install' in scripts
                    scripts_info['has_any_script'] = any([
                        scripts_info['preinstall'],
                        scripts_info['postinstall'],
                        scripts_info['install']
                    ])
                    
                    # 打印发现的脚本信息
                    found_scripts = []
                    if scripts_info['preinstall']:
                        found_scripts.append('preinstall')
                    if scripts_info['postinstall']:
                        found_scripts.append('postinstall')
                    if scripts_info['install']:
                        found_scripts.append('install')
                    
                    if found_scripts:
                        print(f"  发现脚本: {package_name}@{version} -> {', '.join(found_scripts)}")
                        
            elif response.status_code == 404:
                print(f"  包不存在: {package_name}@{version}")
            else:
                print(f"  HTTP错误 {response.status_code}: {package_name}@{version}")
                
        except requests.exceptions.Timeout:
            print(f"  请求超时: {package_name}@{version}")
        except Exception as e:
            print(f"  请求错误: {package_name}@{version} - {str(e)}")
        
        # 缓存结果
        self.package_cache[package_key] = scripts_info
        return scripts_info
    
    def analyze_sample(self, false_positive_reports: Dict[str, Dict], sample_size: int = 50) -> Dict:
        """
        分析样本数据（避免过多API请求）
        """
        results = {}
        
        for tool_name, tool_data in false_positive_reports.items():
            print(f"\n分析 {tool_name} 的误报包脚本类型（样本: {sample_size}）...")
            
            # 取样本
            package_keys = list(tool_data.keys())[:sample_size]
            
            results[tool_name] = {
                'total_false_positives': len(tool_data),
                'sample_size': len(package_keys),
                'script_analysis': {
                    'preinstall': {'count': 0, 'packages': []},
                    'postinstall': {'count': 0, 'packages': []},
                    'install': {'count': 0, 'packages': []},
                    'no_install_scripts': {'count': 0, 'packages': []},
                    'multiple_scripts': {'count': 0, 'packages': []}
                },
                'processed_packages': 0
            }
            
            # 分析每个误报包
            for i, package_key in enumerate(package_keys, 1):
                if '/' in package_key:
                    package_name, version = package_key.rsplit('/', 1)
                else:
                    print(f"  跳过格式错误的包: {package_key}")
                    continue
                
                print(f"  [{i}/{len(package_keys)}] 分析包: {package_name}@{version}")
                
                # 获取脚本信息
                scripts_info = self.get_package_scripts(package_name, version)
                results[tool_name]['processed_packages'] += 1
                
                # 统计脚本类型
                script_count = 0
                if scripts_info['preinstall']:
                    results[tool_name]['script_analysis']['preinstall']['count'] += 1
                    results[tool_name]['script_analysis']['preinstall']['packages'].append(package_key)
                    script_count += 1
                
                if scripts_info['postinstall']:
                    results[tool_name]['script_analysis']['postinstall']['count'] += 1
                    results[tool_name]['script_analysis']['postinstall']['packages'].append(package_key)
                    script_count += 1
                
                if scripts_info['install']:
                    results[tool_name]['script_analysis']['install']['count'] += 1
                    results[tool_name]['script_analysis']['install']['packages'].append(package_key)
                    script_count += 1
                
                if script_count == 0:
                    results[tool_name]['script_analysis']['no_install_scripts']['count'] += 1
                    results[tool_name]['script_analysis']['no_install_scripts']['packages'].append(package_key)
                elif script_count > 1:
                    results[tool_name]['script_analysis']['multiple_scripts']['count'] += 1
                    results[tool_name]['script_analysis']['multiple_scripts']['packages'].append(package_key)
                
                # 添加延迟避免过多请求
                time.sleep(0.3)
        
        return results
    
    def generate_report(self, analysis_results: Dict) -> str:
        """
        生成分析报告
        """
        report = []
        report.append("=" * 80)
        report.append("三大工具误报包安装脚本类型分析报告")
        report.append("=" * 80)
        report.append("")
        
        # 总体统计
        report.append("总体统计:")
        report.append("-" * 60)
        report.append(f"{'工具':<12} {'总误报数':<10} {'样本数':<10} {'采样率':<10}")
        report.append("-" * 60)
        
        for tool_name, data in analysis_results.items():
            total_fp = data['total_false_positives']
            sample_size = data['sample_size']
            sampling_rate = (sample_size / total_fp * 100) if total_fp > 0 else 0
            
            report.append(f"{tool_name:<12} {total_fp:<10} {sample_size:<10} {sampling_rate:<10.1f}%")
        
        report.append("")
        
        # 按脚本类型详细分析
        report.append("按脚本类型误报分析:")
        report.append("-" * 70)
        
        script_types = ['preinstall', 'postinstall', 'install', 'no_install_scripts', 'multiple_scripts']
        script_names = {
            'preinstall': 'preinstall脚本',
            'postinstall': 'postinstall脚本', 
            'install': 'install脚本',
            'no_install_scripts': '无安装脚本',
            'multiple_scripts': '多种脚本'
        }
        
        for script_type in script_types:
            report.append(f"\n{script_names[script_type]} 误报统计:")
            report.append(f"{'工具':<12} {'误报数':<10} {'样本占比':<12} {'估计总数':<12}")
            report.append("-" * 50)
            
            for tool_name, data in analysis_results.items():
                script_data = data['script_analysis'][script_type]
                count = script_data['count']
                total_processed = data['processed_packages']
                percentage = (count / total_processed * 100) if total_processed > 0 else 0
                
                # 估计总数
                total_fp = data['total_false_positives']
                estimated_total = int((count / total_processed) * total_fp) if total_processed > 0 else 0
                
                report.append(f"{tool_name:<12} {count:<10} {percentage:<12.1f}% {estimated_total:<12}")
        
        report.append("")
        
        # 关键发现
        report.append("关键发现:")
        report.append("-" * 30)
        
        # 找出各脚本类型误报估计最多的工具
        for script_type in ['preinstall', 'postinstall', 'install']:
            script_name = script_names[script_type]
            max_estimated = 0
            max_tool = None
            
            for tool_name, data in analysis_results.items():
                script_data = data['script_analysis'][script_type]
                count = script_data['count']
                total_processed = data['processed_packages']
                total_fp = data['total_false_positives']
                
                if total_processed > 0:
                    estimated = int((count / total_processed) * total_fp)
                    if estimated > max_estimated:
                        max_estimated = estimated
                        max_tool = tool_name
            
            if max_estimated > 0:
                report.append(f"- {script_name}误报估计最多: {max_tool} (约{max_estimated}个)")
        
        report.append("")
        
        # 样本示例
        report.append("样本示例:")
        report.append("-" * 30)
        
        for tool_name, data in analysis_results.items():
            report.append(f"\n{tool_name} 有脚本的误报包示例:")
            
            for script_type in ['preinstall', 'postinstall', 'install']:
                script_data = data['script_analysis'][script_type]
                if script_data['count'] > 0:
                    examples = script_data['packages'][:3]
                    example_names = [pkg.split('/')[0] for pkg in examples]
                    report.append(f"  {script_names[script_type]}: {', '.join(example_names)}")
        
        report.append("")
        
        # 分析建议
        report.append("分析建议:")
        report.append("-" * 30)
        report.append("1. 本报告基于样本分析，如需精确数据请进行完整分析")
        report.append("2. 关注有安装脚本的误报包，可能需要调整检测规则")
        report.append("3. 考虑为不同脚本类型设置不同的检测阈值")
        report.append("4. 建议手动验证高频误报包的合法性")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_results(self, analysis_results: Dict, report: str):
        """
        保存分析结果
        """
        try:
            results = {
                'analysis_results': analysis_results,
                'package_cache_size': len(self.package_cache),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open("false_positive_script_analysis_results.json", 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print("详细结果已保存到: false_positive_script_analysis_results.json")
            
        except Exception as e:
            print(f"保存详细结果时出错: {e}")
        
        try:
            with open("false_positive_script_analysis_report.txt", 'w', encoding='utf-8') as f:
                f.write(report)
            print("报告已保存到: false_positive_script_analysis_report.txt")
        except Exception as e:
            print(f"保存报告时出错: {e}")
    
    def run_analysis(self, sample_size: int = 50):
        """
        运行分析
        """
        print("开始分析误报包的安装脚本类型")
        print("=" * 50)
        
        # 1. 加载误报报告
        false_positive_reports = self.load_false_positive_reports()
        if not false_positive_reports:
            print("错误: 无法加载误报报告，分析终止")
            return
        
        # 2. 分析样本
        print(f"\n将分析每个工具的前{sample_size}个误报包...")
        print("注意: 这将通过NPM注册表API获取包信息，可能需要几分钟时间")
        
        analysis_results = self.analyze_sample(false_positive_reports, sample_size)
        
        # 3. 生成报告
        report = self.generate_report(analysis_results)
        print("\n" + report)
        
        # 4. 保存结果
        self.save_results(analysis_results, report)
        
        print("\n分析完成!")


def main():
    """
    主函数
    """
    analyzer = FalsePositiveScriptAnalyzer()
    analyzer.run_analysis(sample_size=50)  # 分析每个工具的前50个误报包


if __name__ == "__main__":
    main() 