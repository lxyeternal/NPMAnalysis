import pandas as pd
import numpy as np

# 读取CSV文件
def analyze_detection_results(file_path):
    # 读取数据
    df = pd.read_csv(file_path)
    
    # 确保列名正确
    required_cols = ['Package Name', 'type', 'DT', 'RF', 'XGB']
    assert all(col in df.columns for col in required_cols), "缺少必要的列"
    
    # 计算总样本数
    total_samples = len(df)
    malware_samples = len(df[df['type'] == 'malware'])
    benign_samples = len(df[df['type'] == 'benign'])
    
    print(f"总样本数: {total_samples}")
    print(f"恶意样本数: {malware_samples}")
    print(f"良性样本数: {benign_samples}")
    print("-" * 50)
    
    # 计算各个算法的性能指标
    algorithms = ['DT', 'RF', 'XGB']
    results = []
    
    for algo in algorithms:
        # 计算四个基本指标
        tp = len(df[(df['type'] == 'malware') & (df[algo] == 1)])  # 真阳性：正确识别为恶意
        tn = len(df[(df['type'] == 'benign') & (df[algo] == 0)])   # 真阴性：正确识别为良性
        fp = len(df[(df['type'] == 'benign') & (df[algo] == 1)])   # 假阳性：良性被误判为恶意（误报）
        fn = len(df[(df['type'] == 'malware') & (df[algo] == 0)])  # 假阴性：恶意被误判为良性（漏报）
        
        # 计算准确率和其他指标
        accuracy = (tp + tn) / total_samples
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        results.append({
            '算法': algo,
            '准确率(Acc)': accuracy,
            '精确率(Precision)': precision,
            '召回率(Recall)': recall,
            'F1分数': f1,
            '误报(FP)数量': fp,
            '漏报(FN)数量': fn
        })
    
    # 创建结果DataFrame并打印
    results_df = pd.DataFrame(results)
    
    # 输出表格
    print("各算法性能指标:")
    print(results_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    
    # 返回结果DataFrame以便进一步分析
    return results_df

if __name__ == "__main__":
    file_path = "/home/wenbo/NPMAnalysis/Tools/sap/scripts/sap_detection_results.csv"
    try:
        results = analyze_detection_results(file_path)
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
    except Exception as e:
        print(f"错误：{e}") 