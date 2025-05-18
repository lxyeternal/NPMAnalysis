#!/usr/bin/env python3
import os
import glob
import fnmatch
import pandas as pd
import numpy as np
from collections import defaultdict

def load_skip_list(file_path):
    """加载需要跳过的包列表"""
    skip_list = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():
                    skip_list.add(line.strip())
    return skip_list

def analyze_guarddog(file_path, folder_type):
    """
    分析guarddog的检测结果
    如果txt中存在"Found 0 potentially malicious indicators"字符串，就证明检测为benign
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if "Found 0 potentially malicious indicators" in content:
            return "benign"
        else:
            return "malware"

def analyze_ossgadget(file_path, folder_type):
    """
    分析ossgadget的检测结果
    如果是"0 matches found."，证明是benign
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if "0 matches found." in content:
            return "benign"
        else:
            return "malware"

def analyze_packj(file_path, folder_type):
    """
    分析packj的检测结果
    如果文件为空或者含有"No risks found!"字符串，就证明是良性的
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if not content.strip() or "No risks found!" in content:
            return "benign"
        else:
            return "malware"

def analyze_genie(file_path, folder_type):
    """
    分析genie的检测结果
    如果csv文件为空，就证明检测为良性的
    如果csv文件不为空，就证明检测为恶意的
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if not content.strip():
            return "benign"
        else:
            return "malware"

def analyze_sap(file_path, malware_benign_skip_list, selected_benign_skip_list):
    """
    分析SAP工具的检测结果
    基于CSV文件中的结果计算各个机器学习算法的性能指标
    跳过在skip列表中的包
    """
    # 读取数据
    df = pd.read_csv(file_path)
    
    # 确保列名正确
    required_cols = ['Package Name', 'type', 'DT', 'RF', 'XGB']
    assert all(col in df.columns for col in required_cols), "缺少必要的列"
    
    # 过滤掉需要跳过的包
    original_count = len(df)
    
    # 将malware_benign_skip_list中的"包名/版本"格式转换为"包名$$版本"格式
    malware_benign_skip_converted = set()
    for item in malware_benign_skip_list:
        converted = item.replace('/', '$$')
        malware_benign_skip_converted.add(converted)
    
    # 将selected_benign_skip_list中的"包名/版本"格式转换为"包名$$版本"格式
    selected_benign_skip_converted = set()
    for item in selected_benign_skip_list:
        converted = item.replace('/', '$$')
        selected_benign_skip_converted.add(converted)
    
    # 跳过恶意样本中存在于malware_benign_skip_list的包
    skip_indices = []
    for idx, row in df.iterrows():
        package_name = row['Package Name']
        sample_type = row['type']
        
        if sample_type == 'malware' and package_name in malware_benign_skip_converted:
            skip_indices.append(idx)
        elif sample_type == 'benign' and package_name in selected_benign_skip_converted:
            skip_indices.append(idx)
    
    # 从数据中删除要跳过的行
    if skip_indices:
        df = df.drop(skip_indices)
    
    # 计算跳过的样本数
    skipped_count = original_count - len(df)
    
    # 计算总样本数
    total_samples = len(df)
    malware_samples = len(df[df['type'] == 'malware'])
    benign_samples = len(df[df['type'] == 'benign'])
    
    print(f"SAP检测结果分析:")
    print(f"总样本数: {total_samples} (跳过了 {skipped_count} 个样本)")
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
        accuracy = (tp + tn) / total_samples if total_samples > 0 else 0
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
    print("SAP各算法性能指标:")
    print(results_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    
    # 打印markdown格式的表格
    print("\nSAP算法性能指标(Markdown格式):")
    print("| 算法 | 准确率 | 精确率 | 召回率 | F1分数 | 误报数量 | 漏报数量 |")
    print("| ---- | ------ | ------ | ------ | ------ | -------- | -------- |")
    for result in results:
        print(f"| {result['算法']} | {result['准确率(Acc)']:.4f} | {result['精确率(Precision)']:.4f} | "
              f"{result['召回率(Recall)']:.4f} | {result['F1分数']:.4f} | {result['误报(FP)数量']} | {result['漏报(FN)数量']} |")
    
    return results_df

def calculate_metrics(true_positives, true_negatives, false_positives, false_negatives):
    """计算精确度、召回率、F1分数等评价指标"""
    total = true_positives + true_negatives + false_positives + false_negatives
    accuracy = (true_positives + true_negatives) / total if total > 0 else 0
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

def extract_package_info(file_path, folder_type):
    """
    从文件路径中提取包名和版本
    格式为：包名/版本
    """
    # 从文件路径提取包名和版本
    dirname = os.path.dirname(file_path)
    parts = dirname.split(os.sep)
    
    # 获取包名和版本
    package_name = None
    version = None
    
    # 尝试从路径中找到包名和版本
    for i, part in enumerate(parts):
        if part == folder_type and i + 1 < len(parts):
            package_name = parts[i + 1]
            if i + 2 < len(parts):
                version = parts[i + 2]
            break
    
    # 如果没有找到包名或版本，使用默认值
    if not package_name:
        package_name = os.path.basename(file_path).split('.')[0]
    if not version:
        version = "1.0.0"
    
    return f"{package_name}/{version}"

def find_package_files(base_path, package_type):
    """递归查找所有的txt文件"""
    result = []
    package_path = os.path.join(base_path, package_type)
    
    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith('.txt') or file.endswith('.csv'):
                result.append(os.path.join(root, file))
    
    return result

def evaluate_tool(tool_name, tool_function, malware_benign_skip_list, selected_benign_skip_list, sub_tool=None):
    """评估特定工具的检测效果"""
    base_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output"
    
    # 为packj工具添加子路径
    if sub_tool:
        base_path = os.path.join(base_path, tool_name, sub_tool)
    else:
        base_path = os.path.join(base_path, tool_name)
    
    results = {
        "true_positive": 0,  # 正确识别恶意样本
        "true_negative": 0,  # 正确识别良性样本
        "false_positive": 0,  # 错误地将良性识别为恶意
        "false_negative": 0,  # 错误地将恶意识别为良性
        "benign_total": 0,
        "malware_total": 0,
        "benign_skipped": 0,  # 跳过的良性样本数
        "malware_skipped": 0   # 跳过的恶意样本数
    }
    
    # 处理良性样本
    benign_files = find_package_files(base_path, "benign")
    for file_path in benign_files:
        package_info = extract_package_info(file_path, "benign")
        
        # 检查是否需要跳过
        if package_info in selected_benign_skip_list:
            results["benign_skipped"] += 1
            continue
        
        results["benign_total"] += 1
        prediction = tool_function(file_path, "benign")
        
        if prediction == "benign":
            results["true_negative"] += 1
        elif prediction == "malware":
            results["false_positive"] += 1
    
    # 处理恶意样本
    malware_files = find_package_files(base_path, "malware")
    for file_path in malware_files:
        package_info = extract_package_info(file_path, "malware")
        
        # 检查是否需要跳过
        if package_info in malware_benign_skip_list:
            results["malware_skipped"] += 1
            continue
        
        results["malware_total"] += 1
        prediction = tool_function(file_path, "malware")
        
        if prediction == "malware":
            results["true_positive"] += 1
        elif prediction == "benign":
            results["false_negative"] += 1
    
    # 计算评价指标
    metrics = calculate_metrics(
        results["true_positive"],
        results["true_negative"],
        results["false_positive"],
        results["false_negative"]
    )
    
    results.update(metrics)
    return results

def main():
    """主函数"""
    # 加载需要跳过的包列表
    malware_benign_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/malware_benign.txt"
    selected_benign_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"
    
    malware_benign_skip_list = load_skip_list(malware_benign_path)
    selected_benign_skip_list = load_skip_list(selected_benign_path)
    
    print(f"已加载需要跳过的恶意样本: {len(malware_benign_skip_list)} 个")
    print(f"已加载需要跳过的良性样本: {len(selected_benign_skip_list)} 个")
    print("-" * 50)
    
    # 定义工具和对应的分析函数
    basic_tools = {
        "ossgadget": analyze_ossgadget,
        "guarddog": analyze_guarddog,
        "genie": analyze_genie
    }
    
    # packj工具有两种检测方式
    packj_subtypes = ["result_static", "result_trace"]
    
    print("NPM恶意包检测工具效果统计:\n")
    print("| 工具名称 | 样本总数 | 跳过样本数 | 准确率 | 精确度 | 召回率 | F1分数 |")
    print("| -------- | -------- | ---------- | ------ | ------ | ------ | ------ |")
    
    # 评估基本工具
    for tool_name, tool_function in basic_tools.items():
        print(f"正在评估 {tool_name}...")
        results = evaluate_tool(tool_name, tool_function, malware_benign_skip_list, selected_benign_skip_list)
        
        total_samples = results["benign_total"] + results["malware_total"]
        total_skipped = results["benign_skipped"] + results["malware_skipped"]
        
        print(
            f"| {tool_name} | {total_samples} | {total_skipped} | {results['accuracy']:.4f} | "
            f"{results['precision']:.4f} | {results['recall']:.4f} | {results['f1']:.4f} |"
        )
        
        print(f"\n{tool_name}详细结果:")
        print(f"良性样本总数: {results['benign_total']} (跳过了 {results['benign_skipped']} 个)")
        print(f"恶意样本总数: {results['malware_total']} (跳过了 {results['malware_skipped']} 个)")
        print(f"真阳性 (TP): {results['true_positive']} (正确识别恶意样本)")
        print(f"真阴性 (TN): {results['true_negative']} (正确识别良性样本)")
        print(f"假阳性 (FP): {results['false_positive']} (错误地将良性识别为恶意)")
        print(f"假阴性 (FN): {results['false_negative']} (错误地将恶意识别为良性)")
        print()
    
    # 评估packj工具的两种检测方式
    for subtype in packj_subtypes:
        tool_name = f"packj_{subtype.replace('result_', '')}"
        print(f"正在评估 {tool_name}...")
        results = evaluate_tool("packj", analyze_packj, malware_benign_skip_list, selected_benign_skip_list, subtype)
        
        total_samples = results["benign_total"] + results["malware_total"]
        total_skipped = results["benign_skipped"] + results["malware_skipped"]
        
        print(
            f"| {tool_name} | {total_samples} | {total_skipped} | {results['accuracy']:.4f} | "
            f"{results['precision']:.4f} | {results['recall']:.4f} | {results['f1']:.4f} |"
        )
        
        print(f"\n{tool_name}详细结果:")
        print(f"良性样本总数: {results['benign_total']} (跳过了 {results['benign_skipped']} 个)")
        print(f"恶意样本总数: {results['malware_total']} (跳过了 {results['malware_skipped']} 个)")
        print(f"真阳性 (TP): {results['true_positive']} (正确识别恶意样本)")
        print(f"真阴性 (TN): {results['true_negative']} (正确识别良性样本)")
        print(f"假阳性 (FP): {results['false_positive']} (错误地将良性识别为恶意)")
        print(f"假阴性 (FN): {results['false_negative']} (错误地将恶意识别为良性)")
        print()
    
    # 分析SAP工具的检测结果
    print("\n分析SAP工具的检测结果...\n")
    sap_file_path = "/home2/wenbo/Documents/NPMAnalysis/Tools/sap/scripts/sap_detection_results.csv"
    analyze_sap(sap_file_path, malware_benign_skip_list, selected_benign_skip_list)

if __name__ == "__main__":
    main() 