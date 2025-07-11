import os
import json
import shutil
from pathlib import Path
from socketai import SocketAI
from config import Config
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataset_analysis.log'),
        logging.StreamHandler()
    ]
)

class DatasetAnalyzer:
    def __init__(self):
        # 数据集路径
        self.benign_dataset = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign"
        self.malware_dataset = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
        
        # 输出路径
        self.benign_output = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/socketai/benign"
        self.malware_output = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/socketai/malware"
        
        # 创建输出目录（如果不存在）
        os.makedirs(self.benign_output, exist_ok=True)
        os.makedirs(self.malware_output, exist_ok=True)
        
        # 初始化SocketAI
        self.socketai = SocketAI()
        
        # 文件大小限制 (175KB)
        self.max_file_size = 175 * 1024
        
        # 每个包最多检测的JS文件数
        self.max_js_files = 25

    def get_package_versions(self, dataset_path):
        """获取数据集中所有的包和版本"""
        package_versions = []
        
        # 遍历数据集目录
        for package_name in os.listdir(dataset_path):
            package_path = os.path.join(dataset_path, package_name)
            if os.path.isdir(package_path):
                # 遍历包的所有版本
                for version in os.listdir(package_path):
                    version_path = os.path.join(package_path, version)
                    if os.path.isdir(version_path):
                        package_versions.append((package_name, version, version_path))
        
        return package_versions

    def collect_js_files(self, version_path):
        """收集版本目录中的JS文件，优先考虑package.json和index.js"""
        js_files = []
        priority_files = []
        
        # 首先查找package.json和index.js
        package_json = os.path.join(version_path, "package.json")
        if os.path.isfile(package_json) and os.path.getsize(package_json) <= self.max_file_size:
            priority_files.append(package_json)
        
        index_js = os.path.join(version_path, "index.js")
        if os.path.isfile(index_js) and os.path.getsize(index_js) <= self.max_file_size:
            priority_files.append(index_js)
        
        # 然后遍历所有其他JS文件
        for root, _, files in os.walk(version_path):
            for file in files:
                if file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    
                    # 检查文件大小
                    if os.path.getsize(file_path) > self.max_file_size:
                        continue
                    
                    # 如果不是已经添加的优先文件
                    if file_path not in priority_files:
                        js_files.append(file_path)
        
        # 合并优先文件和其他JS文件，并限制总数
        return priority_files + js_files[:self.max_js_files - len(priority_files)]

    def analyze_file(self, file_path, output_dir, package_name, version):
        """分析单个文件并保存结果"""
        try:
            # 创建输出目录
            relative_path = os.path.basename(file_path)
            file_output_dir = os.path.join(output_dir, package_name, version, relative_path)
            os.makedirs(file_output_dir, exist_ok=True)
            
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            logging.info(f"分析文件: {file_path}")
            
            # 执行三步分析
            # Step 1: 初始报告
            initial_reports = self.socketai.step1_initial_reports(code)
            
            # 保存初始报告
            for i, report in enumerate(initial_reports):
                report_path = os.path.join(file_output_dir, f"step1_report_{i+1}.txt")
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Step 2: 关键报告
            critical_reports = self.socketai.step2_critical_reports(initial_reports, code)
            
            # 保存关键报告
            for i, report in enumerate(critical_reports):
                report_path = os.path.join(file_output_dir, f"step2_report_{i+1}.txt")
                with open(report_path, 'w', encoding='utf-8') as f:
                    json.dump(report, f, indent=2, ensure_ascii=False)
            
            # Step 3: 最终报告
            final_report = self.socketai.step3_final_report(critical_reports, code)
            
            # 保存最终报告
            final_report_path = os.path.join(file_output_dir, "step3_final_report.txt")
            with open(final_report_path, 'w', encoding='utf-8') as f:
                json.dump(final_report, f, indent=2, ensure_ascii=False)
            
            # 保存综合信息
            summary = {
                "file_path": file_path,
                "is_malicious": final_report.get('malware', 0) > Config.MALWARE_THRESHOLD,
                "malware_score": final_report.get('malware', 0),
                "security_risk": final_report.get('securityRisk', 0),
                "obfuscated": final_report.get('obfuscated', 0),
                "confidence": final_report.get('confidence', 0),
                "conclusion": final_report.get('conclusion', '')
            }
            
            summary_path = os.path.join(file_output_dir, "summary.txt")
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            return summary
            
        except Exception as e:
            logging.error(f"分析文件 {file_path} 时出错: {str(e)}")
            return {
                "file_path": file_path,
                "error": str(e),
                "is_malicious": False
            }

    def analyze_dataset(self):
        """分析整个数据集"""
        # 处理良性数据集
        logging.info("开始处理良性数据集...")
        benign_packages = self.get_package_versions(self.benign_dataset)
        self._process_packages(benign_packages, self.benign_output, "benign")
        
        # 处理恶意数据集
        logging.info("开始处理恶意数据集...")
        malware_packages = self.get_package_versions(self.malware_dataset)
        self._process_packages(malware_packages, self.malware_output, "malware")
        
        logging.info("数据集分析完成")

    def _process_packages(self, packages, output_dir, dataset_type):
        """处理包列表"""
        total = len(packages)
        
        for i, (package_name, version, version_path) in enumerate(packages):
            try:
                logging.info(f"处理 {dataset_type} 包 [{i+1}/{total}]: {package_name}@{version}")
                
                # 收集JS文件
                js_files = self.collect_js_files(version_path)
                logging.info(f"找到 {len(js_files)} 个JS文件进行分析")
                
                # 创建包版本输出目录
                package_version_dir = os.path.join(output_dir, package_name, version)
                os.makedirs(package_version_dir, exist_ok=True)
                
                # 分析每个文件
                results = []
                for file_path in js_files:
                    result = self.analyze_file(file_path, output_dir, package_name, version)
                    results.append(result)
                
                # 保存包级别摘要
                malicious_files = [r for r in results if r.get('is_malicious', False)]
                package_summary = {
                    "package_name": package_name,
                    "version": version,
                    "total_files": len(js_files),
                    "analyzed_files": len(results),
                    "malicious_files": len(malicious_files),
                    "is_malicious": len(malicious_files) > 0,
                    "analysis_date": datetime.now().isoformat()
                }
                
                summary_path = os.path.join(package_version_dir, "package_summary.txt")
                with open(summary_path, 'w', encoding='utf-8') as f:
                    json.dump(package_summary, f, indent=2, ensure_ascii=False)
                
            except Exception as e:
                logging.error(f"处理包 {package_name}@{version} 时出错: {str(e)}")


def main():
    logging.info("开始数据集分析")
    analyzer = DatasetAnalyzer()
    analyzer.analyze_dataset()
    logging.info("数据集分析完成")


if __name__ == "__main__":
    main() 