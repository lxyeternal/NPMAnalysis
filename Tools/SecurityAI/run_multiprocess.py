#!/usr/bin/env python3
"""
NPM包恶意代码检测系统 - 多进程数据集分析启动脚本
"""

import os
import sys
from multiprocess_analyzer import main

if __name__ == "__main__":
    # 检查API密钥是否设置
    from config import Config
    if not Config.OPENAI_API_KEY:
        print("错误: 未设置OpenAI API密钥，请在config.py中配置")
        sys.exit(1)
    
    # 运行多进程分析
    main() 