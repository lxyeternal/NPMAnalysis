import os
import json
import glob
import logging
import pandas as pd
from tqdm import tqdm
from collections import Counter, defaultdict
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MalwareBehaviorAnalyzer:
    def __init__(self):
        self.base_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis"
        self.malware_snippets_dir = os.path.join(self.base_dir, "Codes/code_snipptes/malware_snippets")
        self.package_label_dir = os.path.join(self.base_dir, "Codes/dataclean/package_label")
        self.output_dir = os.path.join(self.base_dir, "Codes/behavior_annoation/key_results")
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 存储所有收集到的behavior summaries
        self.summaries = []
        # 存储每个summary的元信息
        self.metadata = []
        
        # 记录处理的包信息
        self.processed_packages_snippets = set()
        self.processed_packages_labels = set()
        
        # Define behavior categories with core keywords
        # Refined based on word frequency analysis - using root words to catch variations
        self.behavior_categories = {
            "Data Exfiltration": ["exfiltrat", "steal", "collect", "send", "transmit", "leak", "fetch", "upload", "post"],
            "Command Execution": ["execut", "run", "spawn", "child_process", "shell", "subprocess", "launch", "detach"],
            "Obfuscation Techniques": ["obfuscat", "encod", "eval", "base64", "decrypt", "hidden", "shady", "concealed"],
            "Network Communication": ["webhook", "discord", "telegram", "http", "server", "endpoint", "api", "url", "fetch"],
            "Persistence Mechanisms": ["install", "preinstall", "postinstall", "persist", "startup", "autostart", "launch", "bootstrap"],
            "Credential Theft": ["credential", "token", "password", "authenticat", "login", "auth", "account"],
            "Browser Manipulation": ["iframe", "dom", "cookie", "browser", "css", "dangerouslysetinnerhtml", "xss", "inject"],
            "Malicious Payload Delivery": ["download", "payload", "dropper", "deliver", "unpack", "fetch"],
            "System Reconnaissance": ["system", "info", "hostname", "environment", "reconnaissance", "ip", "geolocation"],
            "Anti-Analysis": ["anti", "evas", "detect", "debugger", "analysis", "suppress", "hinder"],
            "Privilege Escalation": ["privilege", "sudo", "elevat", "escalat", "root", "admin", "rights"],
            "DDoS Capabilities": ["ddos", "flood", "packet", "udp", "stress", "dos"],
            "Proxy Manipulation": ["proxy", "scrape", "list", "sock", "tunnel"],
            "Prototype Pollution": ["prototype", "global", "extend", "override", "modify"],
            "File Operations": ["file", "read", "write", "delet", "disk", "local", "path"],
        }
        
        # Store classification results
        self.summary_classifications = []  # Each summary's classifications
        self.package_primary_classifications = {}  # Package-version to primary classification
        self.package_all_classifications = defaultdict(set)  # Package-version to all classifications
        
        # Track unmatched and multiple-matched summaries
        self.unmatched_summaries = []
        self.multiple_matched_summaries = []
        
    def collect_from_malware_snippets(self):
        """收集malware_snippets目录下的behavior summaries"""
        logger.info("正在收集malware_snippets目录下的behavior summaries...")
        
        result_files = glob.glob(f"{self.malware_snippets_dir}/**/*.json", recursive=True)
        logger.info(f"找到 {len(result_files)} 个malware_snippets JSON文件")
        
        snippets_count = 0
        summary_count = 0
        
        for file_path in tqdm(result_files, desc="处理malware_snippets文件"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "malicious_snippets" in data:
                    snippets_count += len(data["malicious_snippets"])
                    package_name = data.get("metadata", {}).get("package_name", "unknown")
                    self.processed_packages_snippets.add(package_name)
                    
                    for snippet in data["malicious_snippets"]:
                        if "behavior_summary" in snippet and snippet["behavior_summary"]:
                            summary_count += 1
                            self.summaries.append(snippet["behavior_summary"])
                            
                            # 收集元数据
                            version = data.get("metadata", {}).get("version", "unknown")
                            file_name = snippet.get("file", "unknown")
                            type_name = snippet.get("type", "unknown")
                            
                            self.metadata.append({
                                "source": "malware_snippets",
                                "package_name": package_name,
                                "version": version,
                                "file": file_name,
                                "type": type_name,
                                "summary": snippet["behavior_summary"]
                            })
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
        
        logger.info(f"从malware_snippets收集完成: 处理了 {len(result_files)} 个文件, {snippets_count} 个代码片段, 提取了 {summary_count} 个行为总结")
        logger.info(f"从malware_snippets中共处理了 {len(self.processed_packages_snippets)} 个不同的包")
    
    def collect_from_package_label(self):
        """收集package_label目录下的behavior summaries"""
        logger.info("正在收集package_label目录下的behavior summaries...")
        
        analysis_files = glob.glob(f"{self.package_label_dir}/**/*analysis.json", recursive=True)
        logger.info(f"找到 {len(analysis_files)} 个package_label分析文件")
        
        summaries_count = 0
        
        for file_path in tqdm(analysis_files, desc="处理package_label文件"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                package_name = data.get("package_name", "unknown")
                self.processed_packages_labels.add(package_name)
                
                if "behavior_summaries" in data:
                    file_summaries = data["behavior_summaries"]
                    summaries_count += len(file_summaries)
                    
                    for file_path, summary in file_summaries.items():
                        if summary:
                            self.summaries.append(summary)
                            
                            # 收集元数据
                            version = data.get("version", "unknown")
                            
                            self.metadata.append({
                                "source": "package_label",
                                "package_name": package_name,
                                "version": version,
                                "file": file_path,
                                "type": "unknown",
                                "summary": summary
                            })
            except Exception as e:
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
        
        logger.info(f"从package_label收集完成: 处理了 {len(analysis_files)} 个文件, 提取了 {summaries_count} 个行为总结")
        logger.info(f"从package_label中共处理了 {len(self.processed_packages_labels)} 个不同的包")
    
    def classify_summaries(self):
        """根据关键词对每个summary进行分类"""
        logger.info(f"开始对 {len(self.summaries)} 个behavior summaries进行分类...")
        
        # Track classification distribution
        classification_counts = Counter()
        
        for i, (summary, meta) in enumerate(zip(self.summaries, self.metadata)):
            # Convert to lowercase for case-insensitive matching
            summary_lower = summary.lower()
            
            # Find all matching categories
            matching_categories = []
            
            for category, keywords in self.behavior_categories.items():
                for keyword in keywords:
                    if keyword.lower() in summary_lower:
                        matching_categories.append(category)
                        break
            
            # Package identifier (name-version)
            package_id = f"{meta['package_name']}-{meta['version']}"
            
            # Store the classification result
            classification_result = {
                'summary_index': i,
                'package_name': meta['package_name'],
                'version': meta['version'],
                'package_id': package_id,
                'file': meta['file'],
                'source': meta['source'],
                'summary': summary,
                'classifications': matching_categories
            }
            
            self.summary_classifications.append(classification_result)
            
            # Track unmatched summaries
            if not matching_categories:
                self.unmatched_summaries.append(classification_result)
            
            # Track multiple matched summaries
            elif len(matching_categories) > 1:
                self.multiple_matched_summaries.append(classification_result)
            
            # Update package-level classifications
            if matching_categories:
                # Add all matching categories to this package's set
                self.package_all_classifications[package_id].update(matching_categories)
                
                # For primary classification, use most common or first found
                if package_id not in self.package_primary_classifications:
                    self.package_primary_classifications[package_id] = matching_categories[0]
                
                # Update counts
                classification_counts.update(matching_categories)
        
        # Log summary statistics
        logger.info(f"分类完成: 共 {len(self.summary_classifications)} 个summaries被分类")
        logger.info(f"有 {len(self.unmatched_summaries)} 个summaries未匹配任何类别")
        logger.info(f"有 {len(self.multiple_matched_summaries)} 个summaries匹配多个类别")
        
        # Display category distribution
        logger.info("类别分布:")
        for category, count in classification_counts.most_common():
            logger.info(f"  {category}: {count}")
        
        logger.info(f"共有 {len(self.package_primary_classifications)} 个package-version被分类到主要类别")
        logger.info(f"共有 {len(self.package_all_classifications)} 个package-version被分类到一个或多个类别")
    
    def save_classification_results(self):
        """保存分类结果到文件"""
        logger.info("正在保存分类结果...")
        
        # 1. Save all summary classifications
        summary_df = pd.DataFrame(self.summary_classifications)
        summary_df.to_csv(os.path.join(self.output_dir, "summary_classifications.csv"), index=False)
        
        # 2. Save primary classification for each package-version
        primary_records = []
        for pid, cls in self.package_primary_classifications.items():
            # Use rsplit to correctly handle package names with hyphens
            parts = pid.rsplit('-', 1)
            if len(parts) == 2:
                package_name, version = parts
            else:
                # Fallback if no version found
                package_name, version = pid, "unknown"
            
            primary_records.append({
                'package_id': pid, 
                'package_name': package_name, 
                'version': version, 
                'classification': cls
            })
        
        primary_df = pd.DataFrame(primary_records)
        primary_df.to_csv(os.path.join(self.output_dir, "package_primary_classifications.csv"), index=False)
        
        # 3. Save all classifications for each package-version
        all_records = []
        for pid, classifications in self.package_all_classifications.items():
            # Use rsplit to correctly handle package names with hyphens
            parts = pid.rsplit('-', 1)
            if len(parts) == 2:
                package_name, version = parts
            else:
                # Fallback if no version found
                package_name, version = pid, "unknown"
            
            all_records.append({
                'package_id': pid, 
                'package_name': package_name, 
                'version': version,
                'classifications': list(classifications)
            })
        
        all_df = pd.DataFrame(all_records)
        all_df.to_csv(os.path.join(self.output_dir, "package_all_classifications.csv"), index=False)
        
        # ...existing code...
        # 4. Save unmatched summaries
        if self.unmatched_summaries:
            unmatched_df = pd.DataFrame(self.unmatched_summaries)
            unmatched_df.to_csv(os.path.join(self.output_dir, "unmatched_summaries.csv"), index=False)
        
        # 5. Save multiple-matched summaries
        if self.multiple_matched_summaries:
            multiple_df = pd.DataFrame(self.multiple_matched_summaries)
            multiple_df.to_csv(os.path.join(self.output_dir, "multiple_matched_summaries.csv"), index=False)
        
        # 6. Generate summary statistics
        # Distribution of summaries by category
        summary_categories = []
        for result in self.summary_classifications:
            for category in result.get('classifications', []):
                summary_categories.append({'summary_index': result['summary_index'], 'category': category})
        
        summary_category_df = pd.DataFrame(summary_categories)
        summary_category_counts = summary_category_df['category'].value_counts().reset_index()
        summary_category_counts.columns = ['category', 'count']
        summary_category_counts.to_csv(os.path.join(self.output_dir, "summary_category_distribution.csv"), index=False)
        
        # Distribution of package-versions by primary category
        primary_category_counts = primary_df['classification'].value_counts().reset_index()
        primary_category_counts.columns = ['category', 'count']
        primary_category_counts.to_csv(os.path.join(self.output_dir, "package_primary_category_distribution.csv"), index=False)
        
        # Count packages by source
        source_counts = summary_df['source'].value_counts().reset_index()
        source_counts.columns = ['source', 'count']
        source_counts.to_csv(os.path.join(self.output_dir, "summary_source_distribution.csv"), index=False)
        
        logger.info(f"分类结果已保存到 {self.output_dir} 目录")
    
    def generate_classification_report(self):
        """生成分类报告，包括各种统计数据"""
        logger.info("正在生成分类报告...")
        
        # 1. Count summaries by category
        category_counter = Counter()
        for result in self.summary_classifications:
            for category in result.get('classifications', []):
                category_counter[category] += 1
        
        # 2. Count package-versions by category (all classifications)
        package_category_counter = Counter()
        for pid, categories in self.package_all_classifications.items():
            for category in categories:
                package_category_counter[category] += 1
        
        # 3. Count summaries by source
        source_counter = Counter()
        for meta in self.metadata:
            source_counter[meta['source']] += 1
        
        # 4. Create a comprehensive report
        report = {
            'summary_count': len(self.summaries),
            'package_version_count': len(self.package_primary_classifications),
            'unmatched_summary_count': len(self.unmatched_summaries),
            'multiple_matched_summary_count': len(self.multiple_matched_summaries),
            'summary_category_distribution': dict(category_counter),
            'package_category_distribution': dict(package_category_counter),
            'source_distribution': dict(source_counter),
        }
        
        # Save report as JSON
        with open(os.path.join(self.output_dir, "classification_report.json"), 'w') as f:
            json.dump(report, f, indent=2)
        
        # Log key statistics
        logger.info(f"总结数量: {report['summary_count']}")
        logger.info(f"包版本数量: {report['package_version_count']}")
        logger.info(f"未匹配总结: {report['unmatched_summary_count']} ({report['unmatched_summary_count']/report['summary_count']*100:.1f}%)")
        logger.info(f"多类别匹配总结: {report['multiple_matched_summary_count']} ({report['multiple_matched_summary_count']/report['summary_count']*100:.1f}%)")
        
        logger.info("总结类别分布:")
        for category, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {category}: {count} ({count/report['summary_count']*100:.1f}%)")
        
        logger.info("包版本类别分布:")
        for category, count in sorted(package_category_counter.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  {category}: {count} ({count/report['package_version_count']*100:.1f}%)")
        
        logger.info(f"分类报告已保存到 {os.path.join(self.output_dir, 'classification_report.json')}")
    
    def run_analysis(self):
        """执行完整的分析流程"""
        logger.info("开始执行恶意软件行为分析...")
        
        # 1. Collect behavior summaries from different sources
        self.collect_from_malware_snippets()
        self.collect_from_package_label()
        logger.info(f"共收集了 {len(self.summaries)} 个行为总结")
        
        # 2. Classify the summaries
        self.classify_summaries()
        
        # 3. Save classification results
        self.save_classification_results()
        
        # 4. Generate classification report
        self.generate_classification_report()
        
        logger.info("恶意软件行为分析完成")


if __name__ == "__main__":
    analyzer = MalwareBehaviorAnalyzer()
    analyzer.run_analysis()