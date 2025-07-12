#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恶意安装脚本检测工具性能分析

这个脚本分析preinstall、postinstall、install等脚本类别在guarddog、ossgadget、genie三个工具中的检测准确率和误报情况。
"""

import json
import re
import os
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter


class MaliciousScriptAnalyzer:
    def __init__(self):
        self.script_analysis_file = "Codes/code_snipptes/malicious_install_scripts_analysis.txt"
        self.tool_reports = {
            "guarddog": "Codes/tool_detect/tool_output_statistic/reports/stats_output/guarddog/malicious_reports.json",
            "ossgadget": "Codes/tool_detect/tool_output_statistic/reports/stats_output/ossgadget/malicious_reports.json", 
            "genie": "Codes/tool_detect/tool_output_statistic/reports/stats_output/genie/malicious_reports.json"
        }
        
        # 存储分析结果
        self.script_categories = {}  # 类别 -> 包集合
        self.tool_detections = {}    # 工具名 -> 包检测结果
        
    def parse_script_categories(self) -> Dict[str, Set[str]]:
        """
        解析恶意安装脚本分析文件，提取各类别的包信息
        """
        categories = {}
        current_category = None
        
        print("正在解析恶意脚本分析文件...")
        
        try:
            with open(self.script_analysis_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # 匹配类别标题行
                    category_match = re.match(r'(\d+)\.\s+(\w+)\s+脚本\s+\(总计:\s*(\d+)个\)', line)
                    if category_match:
                        category_name = category_match.group(2)
                        total_count = int(category_match.group(3))
                        current_category = category_name
                        categories[current_category] = set()
                        print(f"发现类别: {category_name} ({total_count}个包)")
                        continue
                    
                    # 匹配包信息行
                    if current_category and line.startswith('- '):
                        # 解析包名和版本，格式: "- package_name@version - /path/to/file"
                        # 使用更精确的正则表达式匹配包名@版本直到 " - " 分隔符
                        package_match = re.match(r'-\s+(.+?)\s+-\s+', line)
                        if package_match:
                            package_version_str = package_match.group(1)
                            # 在包名@版本字符串中查找最后一个@符号来分割包名和版本
                            at_index = package_version_str.rfind('@')
                            if at_index != -1:
                                package_name = package_version_str[:at_index]
                                version = package_version_str[at_index + 1:]
                                # 使用包名/版本作为唯一标识符，与工具报告格式保持一致
                                package_key = f"{package_name}/{version}"
                                categories[current_category].add(package_key)
                            else:
                                print(f"无法找到@符号的行: {line[:100]}...")
                        else:
                            # 调试输出，查看无法匹配的行
                            print(f"无法匹配的行: {line[:100]}...")  # 只显示前100个字符
                            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {self.script_analysis_file}")
            return {}
        except Exception as e:
            print(f"解析脚本分析文件时出错: {e}")
            return {}
            
        return categories
    
    def load_tool_reports(self) -> Dict[str, Dict]:
        """
        加载三个工具的检测报告
        """
        reports = {}
        
        for tool_name, report_file in self.tool_reports.items():
            print(f"正在加载 {tool_name} 的检测报告...")
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    reports[tool_name] = json.load(f)
                print(f"成功加载 {tool_name} 报告，包含 {len(reports[tool_name])} 个包")
            except FileNotFoundError:
                print(f"警告: 找不到 {tool_name} 的报告文件: {report_file}")
                reports[tool_name] = {}
            except Exception as e:
                print(f"加载 {tool_name} 报告时出错: {e}")
                reports[tool_name] = {}
                
        return reports
    
    def analyze_tool_performance(self, categories: Dict[str, Set[str]], 
                                tool_reports: Dict[str, Dict]) -> Dict:
        """
        分析每个工具对各脚本类别的检测性能
        """
        results = {}
        
        print("\n开始分析工具性能...")
        
        for tool_name, tool_data in tool_reports.items():
            print(f"\n分析 {tool_name} 的性能:")
            results[tool_name] = {}
            
            for category, packages in categories.items():
                print(f"  分析类别: {category}")
                
                # 统计该类别的检测情况
                total_packages = len(packages)
                detected_as_malware = 0
                not_detected = 0
                false_negatives = []  # 未检测到的恶意包
                
                for package in packages:
                    if package in tool_data:
                        # 检查预测结果
                        prediction = tool_data[package].get('prediction', '').lower()
                        actual = tool_data[package].get('actual', '').lower()
                        
                        if prediction == 'malware':
                            detected_as_malware += 1
                        else:
                            not_detected += 1
                            false_negatives.append(package)
                    else:
                        # 工具没有检测这个包
                        not_detected += 1
                        false_negatives.append(package)
                
                # 计算检测率
                detection_rate = (detected_as_malware / total_packages * 100) if total_packages > 0 else 0
                
                results[tool_name][category] = {
                    'total_packages': total_packages,
                    'detected_as_malware': detected_as_malware,
                    'not_detected': not_detected,
                    'detection_rate': detection_rate,
                    'false_negatives': false_negatives[:10]  # 只保存前10个作为示例
                }
                
                print(f"    总包数: {total_packages}")
                print(f"    检测为恶意: {detected_as_malware}")
                print(f"    未检测到: {not_detected}")
                print(f"    检测率: {detection_rate:.2f}%")
        
        return results
    
    def generate_comparison_report(self, analysis_results: Dict) -> str:
        """
        生成工具比较报告
        """
        report = []
        report.append("=" * 80)
        report.append("恶意安装脚本检测工具性能比较报告")
        report.append("=" * 80)
        report.append("")
        
        # 获取所有类别
        categories = set()
        for tool_results in analysis_results.values():
            categories.update(tool_results.keys())
        
        categories = sorted(list(categories))
        
        # 按类别比较
        for category in categories:
            report.append(f"{category} 脚本检测结果比较:")
            report.append("-" * 60)
            
            # 表头
            report.append(f"{'工具':<12} {'总包数':<8} {'检测到':<8} {'未检测':<8} {'检测率':<10}")
            report.append("-" * 60)
            
            for tool_name in ['guarddog', 'ossgadget', 'genie']:
                if tool_name in analysis_results and category in analysis_results[tool_name]:
                    result = analysis_results[tool_name][category]
                    report.append(f"{tool_name:<12} {result['total_packages']:<8} "
                                f"{result['detected_as_malware']:<8} {result['not_detected']:<8} "
                                f"{result['detection_rate']:<10.2f}%")
                else:
                    report.append(f"{tool_name:<12} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'N/A':<10}")
            
            report.append("")
        
        # 总体比较
        report.append("总体性能比较:")
        report.append("-" * 60)
        report.append(f"{'工具':<12} {'平均检测率':<12} {'最佳类别':<15} {'最差类别':<15}")
        report.append("-" * 60)
        
        for tool_name in ['guarddog', 'ossgadget', 'genie']:
            if tool_name in analysis_results:
                rates = [result['detection_rate'] for result in analysis_results[tool_name].values()]
                if rates:
                    avg_rate = sum(rates) / len(rates)
                    
                    # 找到最佳和最差类别
                    best_category = max(analysis_results[tool_name].items(), 
                                      key=lambda x: x[1]['detection_rate'])[0]
                    worst_category = min(analysis_results[tool_name].items(), 
                                       key=lambda x: x[1]['detection_rate'])[0]
                    
                    report.append(f"{tool_name:<12} {avg_rate:<12.2f}% {best_category:<15} {worst_category:<15}")
                else:
                    report.append(f"{tool_name:<12} {'N/A':<12} {'N/A':<15} {'N/A':<15}")
            else:
                report.append(f"{tool_name:<12} {'N/A':<12} {'N/A':<15} {'N/A':<15}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_detailed_results(self, analysis_results: Dict, filename: str = "detailed_analysis_results.json"):
        """
        保存详细的分析结果到JSON文件
        """
        try:
            # 转换集合为列表以便JSON序列化
            serializable_results = {}
            for tool_name, tool_results in analysis_results.items():
                serializable_results[tool_name] = {}
                for category, result in tool_results.items():
                    serializable_results[tool_name][category] = {
                        'total_packages': result['total_packages'],
                        'detected_as_malware': result['detected_as_malware'],
                        'not_detected': result['not_detected'],
                        'detection_rate': result['detection_rate'],
                        'false_negatives_sample': result['false_negatives']
                    }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_results, f, ensure_ascii=False, indent=2)
            print(f"详细结果已保存到: {filename}")
            
        except Exception as e:
            print(f"保存详细结果时出错: {e}")
    
    def run_analysis(self):
        """
        运行完整的分析流程
        """
        print("开始恶意安装脚本检测工具性能分析")
        print("=" * 50)
        
        # 1. 解析脚本类别
        categories = self.parse_script_categories()
        if not categories:
            print("错误: 无法解析脚本类别，分析终止")
            return
        
        print(f"\n成功解析 {len(categories)} 个脚本类别:")
        for category, packages in categories.items():
            print(f"  {category}: {len(packages)} 个包")
        
        # 2. 加载工具报告
        tool_reports = self.load_tool_reports()
        if not tool_reports:
            print("错误: 无法加载工具报告，分析终止")
            return
        
        # 3. 分析工具性能
        analysis_results = self.analyze_tool_performance(categories, tool_reports)
        
        # 4. 生成比较报告
        comparison_report = self.generate_comparison_report(analysis_results)
        print("\n" + comparison_report)
        
        # 5. 保存详细结果
        self.save_detailed_results(analysis_results)
        
        # 6. 保存比较报告
        report_file = "malicious_script_detection_comparison_report.txt"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(comparison_report)
            print(f"\n比较报告已保存到: {report_file}")
        except Exception as e:
            print(f"保存比较报告时出错: {e}")
        
        print("\n分析完成!")


def main():
    """
    主函数
    """
    analyzer = MaliciousScriptAnalyzer()
    analyzer.run_analysis()


if __name__ == "__main__":
    main()
