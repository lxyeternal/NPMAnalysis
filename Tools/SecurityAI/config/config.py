import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 数据集路径
    MALWARE_DATASET_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
    BENIGN_DATASET_PATH = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign"
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GPT_MODEL = "gpt-3.5-turbo-1106"  # 或 "gpt-4-1106-preview"
    
    # 报告数量配置
    GPT3_REPORTS = 5
    GPT4_REPORTS = 3
    
    # 文件处理配置
    MAX_FILE_SIZE = 50000  # 最大文件大小（字符）
    
    # API调用配置
    API_RETRY_ATTEMPTS = 3
    API_RETRY_DELAY = 5  # 秒
    
    # 评分阈值
    MALWARE_THRESHOLD = 0.5
    SECURITY_RISK_THRESHOLD = 0.5