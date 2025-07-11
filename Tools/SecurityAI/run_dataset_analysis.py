#!/usr/bin/env python3
"""
NPM包恶意代码检测系统 - 数据集分析启动脚本
基于论文: Leveraging Large Language Models to Detect npm Malicious Packages
"""

import os
import sys
import time
from dataset_analyzer import DatasetAnalyzer

def print_banner():
    """打印程序横幅"""
    print("="*60)
    print("SocketAI - NPM包恶意代码检测系统 - 数据集批量分析")
    print("基于论文: Leveraging Large Language Models to Detect npm Malicious Packages")
    print("="*60)
    print("\n数据集路径:")
    print("- 良性数据集: /home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign")
    print("- 恶意数据集: /home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware")
    print("\n输出路径:")
    print("- 良性结果: /home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/socketai/benign")
    print("- 恶意结果: /home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/socketai/malware")
    print("="*60)

def main():
    """主函数"""
    print_banner()
    
    # 检查OpenAI API密钥是否设置
    if not os.environ.get('OPENAI_API_KEY'):
        print("\n错误: 未设置OPENAI_API_KEY环境变量")
        print("请设置API密钥后重试，例如:")
        print("export OPENAI_API_KEY=your_api_key_here")
        return 1
    
    print("\n开始数据集分析...")
    start_time = time.time()
    
    try:
        # 创建并运行分析器
        analyzer = DatasetAnalyzer()
        analyzer.analyze_dataset()
        
        # 显示完成信息
        elapsed_time = time.time() - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print("\n分析完成!")
        print(f"总耗时: {int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
        print("结果已保存到指定目录")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n分析被用户中断")
        return 1
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 