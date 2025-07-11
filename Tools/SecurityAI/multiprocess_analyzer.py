#!/usr/bin/env python3
"""
NPM包恶意代码检测系统 - 多进程数据集分析
基于论文: Leveraging Large Language Models to Detect npm Malicious Packages
"""

import os
import json
import time
import multiprocessing
from pathlib import Path
from datetime import datetime
import logging
import random
from socketai import SocketAI
from config import Config

# 设置主日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multiprocess_analysis.log'),
        logging.StreamHandler()
    ]
)

# 获取主日志记录器
logger = logging.getLogger()

def is_analysis_complete(file_output_dir):
    """
    检查文件的分析结果是否完整
    完整的分析结果应包含：
    - 5个step1报告
    - 5个step2报告
    - 1个step3最终报告
    - 1个summary摘要
    """
    try:
        # 检查目录是否存在
        if not os.path.exists(file_output_dir):
            return False
        
        # 检查step1报告
        step1_reports = [f for f in os.listdir(file_output_dir) if f.startswith("step1_report_") and f.endswith(".txt")]
        if len(step1_reports) != 5:
            return False
        
        # 检查step2报告
        step2_reports = [f for f in os.listdir(file_output_dir) if f.startswith("step2_report_") and f.endswith(".txt")]
        if len(step2_reports) != 5:
            return False
        
        # 检查step3最终报告
        if not os.path.exists(os.path.join(file_output_dir, "step3_final_report.txt")):
            return False
        
        # 检查summary摘要
        if not os.path.exists(os.path.join(file_output_dir, "summary.txt")):
            return False
        
        # 验证文件内容是否为有效的JSON
        try:
            with open(os.path.join(file_output_dir, "step3_final_report.txt"), 'r', encoding='utf-8') as f:
                final_report = json.load(f)
            
            # 检查关键字段是否存在
            required_fields = ["malware", "securityRisk", "obfuscated", "confidence", "conclusion"]
            for field in required_fields:
                if field not in final_report:
                    return False
            
            # 分析结果完整
            return True
        
        except (json.JSONDecodeError, UnicodeDecodeError, IOError):
            # JSON解析错误或文件读取错误
            return False
    
    except Exception as e:
        logger.error(f"检查分析完整性时出错: {str(e)}")
        return False

def process_package(package_info):
    """处理单个包的函数（在独立进程中运行）"""
    package_name, version, version_path, is_malware = package_info
    
    # 确定输出目录
    output_dir = Config.MALWARE_OUTPUT_PATH if is_malware else Config.BENIGN_OUTPUT_PATH
    dataset_type = "malware" if is_malware else "benign"
    
    # 获取进程ID用于日志
    process_id = os.getpid()
    
    try:
        logger.info(f"进程 {process_id} 开始处理 {dataset_type} 包: {package_name}@{version}")
        
        # 创建包版本输出目录
        package_version_dir = os.path.join(output_dir, package_name, version)
        os.makedirs(package_version_dir, exist_ok=True)
        
        # 检查包级别摘要是否存在且完整
        package_summary_path = os.path.join(package_version_dir, "package_summary.txt")
        package_already_analyzed = False
        
        if os.path.exists(package_summary_path):
            try:
                with open(package_summary_path, 'r', encoding='utf-8') as f:
                    package_summary = json.load(f)
                
                # 检查包摘要是否包含所有必要字段
                required_fields = ["package_name", "version", "total_files", "analyzed_files", "malicious_files", "is_malicious"]
                if all(field in package_summary for field in required_fields):
                    package_already_analyzed = True
            except:
                # 包摘要文件存在但格式不正确，需要重新分析
                package_already_analyzed = False
        
        # 收集JS文件
        js_files = collect_js_files(version_path)
        logger.info(f"进程 {process_id}: 找到 {len(js_files)} 个JS文件进行分析 - {package_name}@{version}")
        
        # 如果包已经完整分析过，检查所有文件是否都已分析完成
        if package_already_analyzed:
            all_files_analyzed = True
            for file_path in js_files:
                relative_path = os.path.basename(file_path)
                file_output_dir = os.path.join(output_dir, package_name, version, relative_path)
                if not is_analysis_complete(file_output_dir):
                    all_files_analyzed = False
                    break
            
            if all_files_analyzed:
                logger.info(f"进程 {process_id}: 包 {package_name}@{version} 已完整分析，跳过")
                return package_name, version, True
            else:
                logger.info(f"进程 {process_id}: 包 {package_name}@{version} 部分文件分析不完整，继续分析")
        
        # 创建SocketAI实例（每个进程一个实例）
        socketai = SocketAI()
        
        # 分析每个文件
        results = []
        for file_path in js_files:
            try:
                # 创建输出目录
                relative_path = os.path.basename(file_path)
                file_output_dir = os.path.join(output_dir, package_name, version, relative_path)
                
                # 检查该文件是否已经完整分析
                if is_analysis_complete(file_output_dir):
                    logger.info(f"进程 {process_id}: 文件 {file_path} 已完整分析，跳过")
                    
                    # 读取已有的摘要信息
                    try:
                        with open(os.path.join(file_output_dir, "summary.txt"), 'r', encoding='utf-8') as f:
                            summary = json.load(f)
                        results.append(summary)
                        continue
                    except:
                        # 摘要读取失败，重新分析
                        logger.warning(f"进程 {process_id}: 文件 {file_path} 摘要读取失败，重新分析")
                
                # 创建输出目录
                os.makedirs(file_output_dir, exist_ok=True)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                
                logger.info(f"进程 {process_id}: 分析文件: {file_path}")
                
                # 执行三步分析
                # Step 1: 初始报告
                logger.info(f"进程 {process_id}: Step 1: 生成初始报告... - {package_name}@{version}")
                initial_reports = socketai.step1_initial_reports(code)
                
                # 保存初始报告
                for i, report in enumerate(initial_reports):
                    report_path = os.path.join(file_output_dir, f"step1_report_{i+1}.txt")
                    with open(report_path, 'w', encoding='utf-8') as f:
                        json.dump(report, f, indent=2, ensure_ascii=False)
                
                # Step 2: 关键报告
                logger.info(f"进程 {process_id}: Step 2: 生成关键报告... - {package_name}@{version}")
                critical_reports = socketai.step2_critical_reports(initial_reports, code)
                
                # 保存关键报告
                for i, report in enumerate(critical_reports):
                    report_path = os.path.join(file_output_dir, f"step2_report_{i+1}.txt")
                    with open(report_path, 'w', encoding='utf-8') as f:
                        json.dump(report, f, indent=2, ensure_ascii=False)
                
                # Step 3: 最终报告
                logger.info(f"进程 {process_id}: Step 3: 生成最终报告... - {package_name}@{version}")
                final_report = socketai.step3_final_report(critical_reports, code)
                
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
                
                results.append(summary)
                
            except Exception as e:
                logger.error(f"进程 {process_id}: 分析文件 {file_path} 时出错: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                results.append({
                    "file_path": file_path,
                    "error": str(e),
                    "is_malicious": False
                })
        
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
        
        logger.info(f"进程 {process_id}: 包 {package_name}@{version} 分析完成")
        return package_name, version, True
        
    except Exception as e:
        logger.error(f"进程 {process_id}: 处理包 {package_name}@{version} 时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return package_name, version, False

def collect_js_files(version_path):
    """收集版本目录中的JS文件，优先考虑package.json和index.js"""
    js_files = []
    priority_files = []
    
    # 首先查找package.json和index.js
    package_json = os.path.join(version_path, "package.json")
    if os.path.isfile(package_json) and os.path.getsize(package_json) <= Config.MAX_FILE_SIZE:
        priority_files.append(package_json)
    
    index_js = os.path.join(version_path, "index.js")
    if os.path.isfile(index_js) and os.path.getsize(index_js) <= Config.MAX_FILE_SIZE:
        priority_files.append(index_js)
    
    # 然后遍历所有其他JS文件
    for root, _, files in os.walk(version_path):
        for file in files:
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                
                # 检查文件大小
                if os.path.getsize(file_path) > Config.MAX_FILE_SIZE:
                    continue
                
                # 如果不是已经添加的优先文件
                if file_path not in priority_files:
                    js_files.append(file_path)
    
    # 合并优先文件和其他JS文件，并限制总数
    return priority_files + js_files[:Config.MAX_JS_FILES_PER_PACKAGE - len(priority_files)]

def get_package_versions(dataset_path):
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

def print_banner():
    """打印程序横幅"""
    print("="*60)
    print("SocketAI - NPM包恶意代码检测系统 - 多进程数据集分析")
    print("基于论文: Leveraging Large Language Models to Detect npm Malicious Packages")
    print("="*60)
    print("\n数据集路径:")
    print(f"- 良性数据集: {Config.BENIGN_DATASET_PATH}")
    print(f"- 恶意数据集: {Config.MALWARE_DATASET_PATH}")
    print("\n输出路径:")
    print(f"- 良性结果: {Config.BENIGN_OUTPUT_PATH}")
    print(f"- 恶意结果: {Config.MALWARE_OUTPUT_PATH}")
    print(f"\n并行处理: 使用 {Config.PROCESS_COUNT} 个进程同时分析")
    print("="*60)

def main():
    """主函数"""
    print_banner()
    logging.info("开始多进程数据集分析")
    
    # 创建输出目录
    os.makedirs(Config.BENIGN_OUTPUT_PATH, exist_ok=True)
    os.makedirs(Config.MALWARE_OUTPUT_PATH, exist_ok=True)
    
    start_time = time.time()
    
    try:
        # 获取所有包
        logging.info("获取良性数据集包列表...")
        benign_packages = []
        for package_name in os.listdir(Config.BENIGN_DATASET_PATH):
            package_path = os.path.join(Config.BENIGN_DATASET_PATH, package_name)
            if os.path.isdir(package_path):
                for version in os.listdir(package_path):
                    version_path = os.path.join(package_path, version)
                    if os.path.isdir(version_path):
                        benign_packages.append((package_name, version, version_path, False))
        
        logging.info(f"找到 {len(benign_packages)} 个良性包版本")
        
        logging.info("获取恶意数据集包列表...")
        malware_packages = []
        for package_name in os.listdir(Config.MALWARE_DATASET_PATH):
            package_path = os.path.join(Config.MALWARE_DATASET_PATH, package_name)
            if os.path.isdir(package_path):
                for version in os.listdir(package_path):
                    version_path = os.path.join(package_path, version)
                    if os.path.isdir(version_path):
                        malware_packages.append((package_name, version, version_path, True))
        
        logging.info(f"找到 {len(malware_packages)} 个恶意包版本")
        
        # 合并并随机打乱任务列表
        all_packages = benign_packages + malware_packages
        random.shuffle(all_packages)
        
        logging.info(f"总共 {len(all_packages)} 个包待分析，将使用 {Config.PROCESS_COUNT} 个进程并行处理")
        
        # 使用进程池处理任务
        with multiprocessing.Pool(processes=Config.PROCESS_COUNT) as pool:
            results = []
            for i, package_info in enumerate(all_packages):
                package_name, version, _, is_malware = package_info
                dataset_type = "恶意" if is_malware else "良性"
                logging.info(f"提交任务 [{i+1}/{len(all_packages)}]: {package_name}@{version} ({dataset_type})")
                
                # 异步提交任务
                result = pool.apply_async(process_package, (package_info,))
                results.append(result)
            
            # 等待所有任务完成并收集结果
            completed = 0
            for result in results:
                package_name, version, success = result.get()  # 这会阻塞直到任务完成
                status = "成功" if success else "失败"
                completed += 1
                logging.info(f"进度: [{completed}/{len(all_packages)}] 包 {package_name}@{version} 分析{status}")
        
        # 显示完成信息
        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        logging.info("所有包分析完成")
        print("\n分析完成!")
        print(f"总耗时: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
        print("结果已保存到指定目录")
        
    except KeyboardInterrupt:
        logging.warning("分析被用户中断")
        print("\n\n分析被用户中断")
    except Exception as e:
        logging.error(f"分析过程中出错: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        print(f"\n错误: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    # 设置多进程启动方法
    multiprocessing.set_start_method('spawn')
    main() 