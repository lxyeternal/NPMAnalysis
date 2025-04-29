#!/usr/bin/env python3
import os
import sys
import json
import glob
import time
import logging
import multiprocessing
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from functools import partial

# 导入自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llmquery import LLMAgent

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("OpenAIDetect")

# 直接在代码中设置参数
NUM_PROCESSES = 24  # 并行处理的进程数
DETECTION_TIMEOUT = 300  # 每个包的超时时间（秒）

# 定义一个全局的LLM代理对象，用于多进程共享
# 注意：这在每个进程中都会创建自己的实例
def init_worker():
    global llm_agent
    llm_agent = LLMAgent()

# 处理单个包的独立函数 - 用于多进程
def process_package_worker(
    task: Tuple[str, str],
    unzip_benign_path: str,
    unzip_malware_path: str,
    output_paths: Dict[str, str],
    malware_detect_prompt: str
) -> None:
    """处理单个包的工作函数，用于多进程调用"""
    data_type, folder_name = task
    
    try:
        # 确定文件夹路径
        unzip_base = unzip_benign_path if data_type == "benign" else unzip_malware_path
        unzip_folder_path = os.path.join(unzip_base, folder_name)
        
        # 定义输出文件路径
        output_file = os.path.join(output_paths[data_type], f"{folder_name}.txt")
        
        # 检查是否已处理过
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            logger.info(f"跳过已处理的包: {data_type}/{folder_name}")
            return
        
        logger.info(f"开始处理 {data_type}/{folder_name}...")
        start_time = time.time()
        
        # 查找所有Python文件
        python_files = glob.glob(f"{unzip_folder_path}/**/*.py", recursive=True)
        
        if not python_files:
            logger.warning(f"包 {folder_name} 中未找到Python文件")
            # 包中没有Python文件，写入空结果
            empty_result = {
                "package_name": folder_name,
                "is_malicious": False,
                "files_analyzed": 0,
                "malicious_files": 0,
                "file_results": []
            }
            
            # 写入空结果
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(empty_result, f, ensure_ascii=False, indent=2)
                
            return
        
        # 使用GPT-4.1分析所有Python文件
        logger.info(f"使用GPT-4.1分析包: {folder_name}")
        file_results = []
        
        # 使用全局LLM代理
        global llm_agent
        
        for py_file in python_files:
            relative_path = os.path.relpath(py_file, unzip_folder_path)
            logger.info(f"GPT-4.1分析文件: {relative_path}")
            
            file_result = analyze_file(py_file, malware_detect_prompt, llm_agent)
            
            # 添加相对路径以便更好地识别文件
            file_result["relative_path"] = relative_path
            file_results.append(file_result)
        
        # 汇总GPT-4.1结果
        malicious_files = sum(1 for fr in file_results if fr["is_malicious"])
        is_package_malicious = malicious_files > 0
        
        package_result = {
            "package_name": folder_name,
            "is_malicious": is_package_malicious,
            "files_analyzed": len(file_results),
            "malicious_files": malicious_files,
            "file_results": file_results
        }
        
        # 保存GPT-4.1结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(package_result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"完成 {data_type}/{folder_name} 的分析，用时: {time.time() - start_time:.2f}秒，是否恶意: {is_package_malicious}")
            
    except Exception as e:
        logger.error(f"处理包 {data_type}/{folder_name} 时出错: {str(e)}")
        # 保存错误信息
        error_result = {
            "package_name": folder_name,
            "is_malicious": False,
            "error": str(e),
            "files_analyzed": 0,
            "malicious_files": 0,
            "file_results": []
        }
        
        # 写入错误结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)


def analyze_file(file_path: str, malware_detect_prompt: str, llm_agent: LLMAgent) -> Dict[str, Any]:
    """使用OpenAI分析单个Python文件"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()
        
        # 如果文件为空，直接返回无恶意的结果
        if not code_content.strip():
            return {
                "file_path": file_path,
                "is_malicious": False,
                "malicious_behavior": ""
            }
        
        # 准备LLM提示
        prompt = malware_detect_prompt.replace("{CODE}", code_content)
        
        # 构建消息
        messages = [
            {"role": "system", "content": "You are a professional Python malicious code analysis expert. Analyze the following code and determine if it contains malicious behavior."},
            {"role": "user", "content": prompt}
        ]
        
        # 调用OpenAI (GPT-4.1)
        response = llm_agent._openai_query(
            messages=messages,
            max_tokens=16000,
            temperature=0,
            top_p=0.3,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={"type": "json_object"},
            seed=42
        )
        
        # 解析响应
        try:
            result = json.loads(response)
            is_malicious = result.get("is_malicious", False)
            
            return {
                "file_path": file_path,
                "is_malicious": is_malicious,
                "malicious_behavior": result.get("malicious_behavior", "")
            }
        except json.JSONDecodeError:
            logger.warning(f"GPT-4.1返回的不是有效JSON: {response[:100]}...")
            return {
                "file_path": file_path,
                "is_malicious": False,
                "malicious_behavior": "GPT-4.1响应解析错误"
            }
            
    except Exception as e:
        logger.error(f"使用GPT-4.1分析文件 {file_path} 时出错: {str(e)}")
        return {
            "file_path": file_path,
            "is_malicious": False,
            "malicious_behavior": f"分析错误: {str(e)}"
        }


class OpenAIDetector:
    def __init__(self):
        # 定义数据路径
        self.base_path = "/home2/wenbo/Documents/PyPIAgent/Dataset/evaluation"
        self.unzip_benign_path = os.path.join(self.base_path, "unzip_benign")
        self.unzip_malware_path = os.path.join(self.base_path, "unzip_malware")
        
        # 定义输出路径
        self.output_base = "/home2/wenbo/Documents/PyPIAgent/Codes/tooldetect/detect_output/baselines"
        self.output_paths = {
            "benign": os.path.join(self.output_base, "gpt-4.1", "benign"),
            "malware": os.path.join(self.output_base, "gpt-4.1", "malware")
        }
        
        # 确保所有输出目录存在
        self._ensure_output_dirs()
        
        # 加载提示模板
        self.prompt_dir = "/home2/wenbo/Documents/PyPIAgent/LLMs/prompts"
        self.malware_detect_prompt = self._load_prompt("malware_detect_prompt.txt")
        
        # 初始化LLM代理 (主进程中的实例)
        self.llm_agent = LLMAgent()
        
        # 统计信息
        self.processed_count = 0
        self.skipped_count = 0
        
    def _ensure_output_dirs(self):
        """确保所有输出目录存在"""
        for category in self.output_paths:
            os.makedirs(self.output_paths[category], exist_ok=True)
    
    def _load_prompt(self, prompt_file: str) -> str:
        """加载提示模板文件"""
        prompt_path = os.path.join(self.prompt_dir, prompt_file)
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"无法加载提示文件 {prompt_path}: {e}")
            raise
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """使用全局函数分析单个Python文件的包装器方法"""
        return analyze_file(file_path, self.malware_detect_prompt, self.llm_agent)
    
    def process_package(self, data_type: str, folder_name: str) -> None:
        """单进程模式下处理单个包的方法，保留原版功能"""
        process_package_worker(
            (data_type, folder_name),
            self.unzip_benign_path,
            self.unzip_malware_path,
            self.output_paths,
            self.malware_detect_prompt
        )
        self.processed_count += 1  # 更新统计
    
    def process_all_packages(self, num_processes=NUM_PROCESSES):
        """使用多进程处理所有包"""
        # 获取良性和恶意样本的文件夹列表
        benign_folders = [f for f in os.listdir(self.unzip_benign_path) 
                          if os.path.isdir(os.path.join(self.unzip_benign_path, f))]
        malware_folders = [f for f in os.listdir(self.unzip_malware_path) 
                           if os.path.isdir(os.path.join(self.unzip_malware_path, f))]
        
        # 创建任务列表
        tasks = []
        for folder in benign_folders:
            tasks.append(("benign", folder))
        for folder in malware_folders:
            tasks.append(("malware", folder))
        
        logger.info(f"共找到 {len(benign_folders)} 个良性样本和 {len(malware_folders)} 个恶意样本")
        logger.info(f"使用 GPT-4.1 模型进行分析，启用 {num_processes} 个进程")
        logger.info(f"输出目录: {os.path.dirname(self.output_paths['benign'])}")
        
        # 初始化已处理和跳过的计数器
        self.processed_count = 0
        self.skipped_count = 0
        
        # 检查已处理过的任务数量
        for data_type, folder_name in tasks:
            output_file = os.path.join(self.output_paths[data_type], f"{folder_name}.txt")
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                self.skipped_count += 1

        # 使用多进程处理任务
        # 创建部分应用函数，将固定参数传入
        process_func = partial(
            process_package_worker,
            unzip_benign_path=self.unzip_benign_path,
            unzip_malware_path=self.unzip_malware_path,
            output_paths=self.output_paths,
            malware_detect_prompt=self.malware_detect_prompt
        )
        
        # 使用进程池并行处理
        with multiprocessing.Pool(
            processes=num_processes,
            initializer=init_worker
        ) as pool:
            # 使用imap以便获取实时进度更新
            for i, _ in enumerate(pool.imap_unordered(process_func, tasks)):
                self.processed_count += 1
                # 定期输出进度信息
                if self.processed_count % 10 == 0 or self.processed_count == len(tasks) - self.skipped_count:
                    logger.info(f"进度: {self.processed_count}/{len(tasks) - self.skipped_count} 包已处理")
        
        logger.info(f"所有样本处理完成！新处理: {self.processed_count} 个，跳过已处理: {self.skipped_count} 个")

if __name__ == "__main__":
    logger.info(f"启动OpenAI恶意代码检测，多进程版本")
    
    # 创建并运行检测器
    detector = OpenAIDetector()
    detector.process_all_packages(num_processes=NUM_PROCESSES)