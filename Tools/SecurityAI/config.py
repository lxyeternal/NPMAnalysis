import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API配置
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # 模型配置
    # mini是更强的模型（对应论文中的GPT-4）
    STRONG_MODEL = "gpt-4.1-mini"
    # nano是次强的模型（对应论文中的GPT-3）
    STANDARD_MODEL = "gpt-4.1-nano"
    
    # 报告数量配置（严格按照论文）
    # 次强模型生成更多报告（5个）
    STANDARD_MODEL_REPORTS_COUNT = 5  # nano生成5个
    # 更强模型生成较少报告（3个）
    STRONG_MODEL_REPORTS_COUNT = 3    # mini生成3个
    
    # 温度参数配置（严格按照论文）
    STEP1_PARAMS = {"temperature": 1.0, "top_p": 0.9}
    STEP2_PARAMS = {"temperature": 0.75, "top_p": 0.6}
    STEP3_PARAMS = {"temperature": 0.5, "top_p": 0.5}
    
    # 恶意评分阈值（论文中定义）
    MALWARE_THRESHOLD = 0.5
    
    # 用户提示词（严格按照论文）
    USER_PROMPT = "Analyze the above code for malicious behavior. Remember to respond in the required JSON format. Consider ALL of the code carefully. Check the beginning, middle, and end of the code. Work step-by-step to get the right answer."