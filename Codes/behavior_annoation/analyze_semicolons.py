#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import glob
import re
from collections import Counter
import logging
from tqdm import tqdm
import pandas as pd

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BehaviorSummaryAnalyzer:
    def __init__(self):
        self.base_dir = "/home2/wenbo/Documents/NPMAnalysis"
        self.malware_snippets_dir = os.path.join(self.base_dir, "Codes/code_snipptes/malware_snippets")
        self.package_label_dir = os.path.join(self.base_dir, "Codes/dataclean/package_label")
        
        # 存储所有收集到的behavior summaries
        self.summaries = []
        # 存储每个summary的元信息
        self.metadata = []
        
        # 统计分号信息
        self.semicolon_stats = {
            "total_summaries": 0,
            "summaries_with_semicolons": 0,
            "total_semicolons": 0,
            "semicolons_per_summary": Counter(),
            "summaries_by_source": {"malware_snippets": 0, "package_label": 0},
            "semicolons_by_source": {"malware_snippets": 0, "package_label": 0}
        }
    
    def collect_from_malware_snippets(self):
        """收集malware_snippets目录下的behavior summaries"""
        logger.info("正在收集malware_snippets目录下的behavior summaries...")
        
        result_files = glob.glob(f"{self.malware_snippets_dir}/**/*.json", recursive=True)
        
        for file_path in tqdm(result_files, desc="处理malware_snippets文件"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "malicious_snippets" in data:
                    for snippet in data["malicious_snippets"]:
                        if "behavior_summary" in snippet and snippet["behavior_summary"]:
                            summary = snippet["behavior_summary"]
                            self.summaries.append(summary)
                            
                            # 收集元数据
                            package_name = data.get("metadata", {}).get("package_name", "unknown")
                            version = data.get("metadata", {}).get("version", "unknown")
                            file_name = snippet.get("file", "unknown")
                            type_name = snippet.get("type", "unknown")
                            
                            # 计算分号数量
                            semicolon_count = summary.count(';')
                            
                            self.metadata.append({
                                "source": "malware_snippets",
                                "package_name": package_name,
                                "version": version,
                                "file": file_name,
                                "type": type_name,
                                "summary": summary,
                                "semicolon_count": semicolon_count
                            })
                            
                            # 更新统计信息
                            self.semicolon_stats["total_summaries"] += 1
                            self.semicolon_stats["summaries_by_source"]["malware_snippets"] += 1
                            if semicolon_count > 0:
                                self.semicolon_stats["summaries_with_semicolons"] += 1
                                self.semicolon_stats["total_semicolons"] += semicolon_count
                                self.semicolon_stats["semicolons_by_source"]["malware_snippets"] += semicolon_count
                                self.semicolon_stats["semicolons_per_summary"][semicolon_count] += 1
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
    
    def collect_from_package_label(self):
        """收集package_label目录下的behavior summaries"""
        logger.info("正在收集package_label目录下的behavior summaries...")
        
        analysis_files = glob.glob(f"{self.package_label_dir}/**/*analysis.json", recursive=True)
        
        for file_path in tqdm(analysis_files, desc="处理package_label文件"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "behavior_summaries" in data:
                    for file_path, summary in data["behavior_summaries"].items():
                        if summary:
                            self.summaries.append(summary)
                            
                            # 收集元数据
                            package_name = data.get("package_name", "unknown")
                            version = data.get("version", "unknown")
                            
                            # 计算分号数量
                            semicolon_count = summary.count(';')
                            
                            self.metadata.append({
                                "source": "package_label",
                                "package_name": package_name,
                                "version": version,
                                "file": file_path,
                                "type": "unknown",
                                "summary": summary,
                                "semicolon_count": semicolon_count
                            })
                            
                            # 更新统计信息
                            self.semicolon_stats["total_summaries"] += 1
                            self.semicolon_stats["summaries_by_source"]["package_label"] += 1
                            if semicolon_count > 0:
                                self.semicolon_stats["summaries_with_semicolons"] += 1
                                self.semicolon_stats["total_semicolons"] += semicolon_count
                                self.semicolon_stats["semicolons_by_source"]["package_label"] += semicolon_count
                                self.semicolon_stats["semicolons_per_summary"][semicolon_count] += 1
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
    
    def analyze_semicolons(self):
        """分析分号使用情况"""
        print("\n===== 分号使用情况分析 =====")
        
        # 计算百分比
        if self.semicolon_stats["total_summaries"] > 0:
            semicolon_percentage = (self.semicolon_stats["summaries_with_semicolons"] / 
                                   self.semicolon_stats["total_summaries"]) * 100
        else:
            semicolon_percentage = 0
            
        print(f"总共分析了 {self.semicolon_stats['total_summaries']} 个behavior summaries")
        print(f"其中 {self.semicolon_stats['summaries_with_semicolons']} 个包含分号 ({semicolon_percentage:.2f}%)")
        print(f"总共发现 {self.semicolon_stats['total_semicolons']} 个分号")
        
        # 按来源统计
        print("\n按来源统计:")
        for source, count in self.semicolon_stats["summaries_by_source"].items():
            semicolon_count = self.semicolon_stats["semicolons_by_source"][source]
            if count > 0:
                avg_semicolons = semicolon_count / count
            else:
                avg_semicolons = 0
            print(f"来源 {source}: {count} 个summaries, {semicolon_count} 个分号, 平均每个summary {avg_semicolons:.2f} 个分号")
        
        # 分号数量分布
        print("\n分号数量分布:")
        for count, frequency in sorted(self.semicolon_stats["semicolons_per_summary"].items()):
            print(f"  {count} 个分号: {frequency} 个summaries")
    
    def extract_semicolon_patterns(self):
        """提取分号使用的模式"""
        print("\n===== 分号使用模式分析 =====")
        
        # 只分析包含分号的summaries
        summaries_with_semicolons = [s for s in self.summaries if ';' in s]
        
        # 提取分号前后的上下文
        contexts = []
        for summary in summaries_with_semicolons:
            # 将summary分割成句子
            sentences = re.split(r'[.!?]', summary)
            for sentence in sentences:
                if ';' in sentence:
                    # 查找所有分号位置
                    for match in re.finditer(';', sentence):
                        pos = match.start()
                        # 提取分号前后各20个字符作为上下文
                        start = max(0, pos - 20)
                        end = min(len(sentence), pos + 20)
                        context = sentence[start:end].strip()
                        contexts.append(context)
        
        print(f"\n已提取 {len(contexts)} 个分号上下文样本")
        if contexts:
            print("\n示例上下文:")
            for i, context in enumerate(contexts[:10], 1):  # 显示前10个
                print(f"  {i}. ...{context}...")
    
    def print_summaries_with_semicolons(self):
        """打印包含分号的summaries"""
        print("\n===== 包含分号的Behavior Summaries =====")
        
        # 过滤出包含分号的元数据
        semicolon_metadata = [m for m in self.metadata if m["semicolon_count"] > 0]
        
        # 按分号数量排序
        semicolon_metadata.sort(key=lambda x: x["semicolon_count"], reverse=True)
        
        # 打印前10个包含最多分号的summaries
        print(f"\n包含最多分号的前10个summaries:")
        for i, data in enumerate(semicolon_metadata[:10], 1):
            print(f"\n{i}. 包名: {data['package_name']}, 版本: {data['version']}")
            print(f"   文件: {data['file']}")
            print(f"   分号数量: {data['semicolon_count']}")
            print(f"   摘要: {data['summary'][:200]}..." if len(data['summary']) > 200 else f"   摘要: {data['summary']}")
            print("-" * 80)
    
    def run_analysis(self):
        """运行完整的分析流程"""
        # 收集数据
        self.collect_from_malware_snippets()
        self.collect_from_package_label()
        
        if not self.summaries:
            print("未收集到任何behavior summaries")
            return
        
        # 分析分号
        self.analyze_semicolons()
        
        # 提取分号使用模式
        self.extract_semicolon_patterns()
        
        # 打印包含分号的summaries
        self.print_summaries_with_semicolons()
        
        print("\n分析完成")

if __name__ == "__main__":
    analyzer = BehaviorSummaryAnalyzer()
    analyzer.run_analysis() 