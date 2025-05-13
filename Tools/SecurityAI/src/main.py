import os
import json
import logging
from pathlib import Path
from datetime import datetime
from detector import SocketAIDetector
from file_processor import FileProcessor
from config.config import Config

class NPMMalwareDetector:
    def __init__(self):
        self.config = Config()
        self.detector = SocketAIDetector(self.config)
        self.file_processor = FileProcessor(self.config)
        
        # 设置日志
        self.setup_logging()
        
    def setup_logging(self):
        log_dir = Path("output/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"detection_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def process_dataset(self, dataset_path, is_malware=False):
        """处理数据集目录"""
        dataset_type = "malware" if is_malware else "benign"
        results = []
        
        package_dirs = self.file_processor.scan_packages(dataset_path)
        
        for idx, package_dir in enumerate(package_dirs):
            package_name = package_dir.name
            version = self._extract_version(package_name)
            
            logging.info(f"Processing {dataset_type} package {idx+1}/{len(package_dirs)}: {package_name}")
            
            try:
                # 扫描包中的JavaScript文件
                js_files = self.file_processor.find_js_files(package_dir)
                
                package_report = {
                    "package_name": package_name,
                    "version": version,
                    "type": dataset_type,
                    "files": []
                }
                
                for js_file in js_files:
                    # 使用SocketAI检测文件
                    file_report = self.detector.analyze_file(js_file)
                    package_report["files"].append({
                        "file_path": str(js_file.relative_to(package_dir)),
                        "report": file_report
                    })
                
                # 计算包级别的评分
                package_report["package_score"] = self._calculate_package_score(package_report)
                results.append(package_report)
                
                # 保存单个包的报告
                self._save_package_report(package_report)
                
            except Exception as e:
                logging.error(f"Error processing package {package_name}: {str(e)}")
                continue
        
        return results
    
    def _extract_version(self, package_name):
        """从包名中提取版本号"""
        parts = package_name.split('-')
        if len(parts) > 1:
            return parts[-1]
        return "unknown"
    
    def _calculate_package_score(self, package_report):
        """计算包级别的恶意评分"""
        max_malware_score = 0
        max_security_score = 0
        
        for file_info in package_report["files"]:
            report = file_info["report"]
            if report and "final_report" in report:
                final_report = report["final_report"]
                max_malware_score = max(max_malware_score, final_report.get("malware", 0))
                max_security_score = max(max_security_score, final_report.get("securityRisk", 0))
        
        return {
            "malware_score": max_malware_score,
            "security_risk_score": max_security_score,
            "is_malicious": max_malware_score > 0.5
        }
    
    def _save_package_report(self, package_report):
        """保存单个包的检测报告"""
        report_dir = Path("output/reports") / package_report["type"]
        report_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{package_report['package_name']}_report.json"
        report_path = report_dir / filename
        
        with open(report_path, 'w') as f:
            json.dump(package_report, f, indent=2)
    
    def run(self):
        """运行检测流程"""
        malware_path = Path(self.config.MALWARE_DATASET_PATH)
        benign_path = Path(self.config.BENIGN_DATASET_PATH)
        
        logging.info("Starting NPM malware detection...")
        
        # 处理恶意软件数据集
        if malware_path.exists():
            logging.info(f"Processing malware dataset from {malware_path}")
            malware_results = self.process_dataset(malware_path, is_malware=True)
        else:
            logging.warning(f"Malware dataset path not found: {malware_path}")
            malware_results = []
        
        # 处理良性数据集
        if benign_path.exists():
            logging.info(f"Processing benign dataset from {benign_path}")
            benign_results = self.process_dataset(benign_path, is_malware=False)
        else:
            logging.warning(f"Benign dataset path not found: {benign_path}")
            benign_results = []
        
        # 生成汇总报告
        self._generate_summary_report(malware_results, benign_results)
        
        logging.info("Detection completed!")
    
    def _generate_summary_report(self, malware_results, benign_results):
        """生成汇总报告"""
        summary = {
            "detection_summary": {
                "total_malware_packages": len(malware_results),
                "total_benign_packages": len(benign_results),
                "correctly_detected_malware": sum(1 for r in malware_results if r["package_score"]["is_malicious"]),
                "false_positives": sum(1 for r in benign_results if r["package_score"]["is_malicious"]),
                "false_negatives": sum(1 for r in malware_results if not r["package_score"]["is_malicious"]),
                "true_negatives": sum(1 for r in benign_results if not r["package_score"]["is_malicious"])
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # 计算指标
        tp = summary["detection_summary"]["correctly_detected_malware"]
        fp = summary["detection_summary"]["false_positives"]
        fn = summary["detection_summary"]["false_negatives"]
        tn = summary["detection_summary"]["true_negatives"]
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        summary["metrics"] = {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "accuracy": (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        }
        
        # 保存汇总报告
        summary_dir = Path("output/summary")
        summary_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_path = summary_dir / f"detection_summary_{timestamp}.json"
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logging.info(f"Summary report saved to {summary_path}")
        logging.info(f"Detection metrics: Precision={precision:.3f}, Recall={recall:.3f}, F1={f1_score:.3f}")

if __name__ == "__main__":
    detector = NPMMalwareDetector()
    detector.run()