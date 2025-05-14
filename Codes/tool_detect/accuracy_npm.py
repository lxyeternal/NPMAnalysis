#!/usr/bin/env python3
import os
import glob
import fnmatch
from collections import defaultdict

def analyze_guarddog(file_path, folder_type):
    """
    分析guarddog的检测结果
    如果txt中存在"Found 0 potentially malicious indicators"字符串，就证明检测为benign
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "Found 0 potentially malicious indicators" in content:
                return "benign"
            else:
                return "malware"
    except Exception as e:
        print(f"读取 {file_path} 出错: {e}")
        return "error"

def analyze_ossgadget(file_path, folder_type):
    """
    分析ossgadget的检测结果
    如果是"0 matches found."，证明是benign
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "0 matches found." in content:
                return "benign"
            else:
                return "malware"
    except Exception as e:
        print(f"读取 {file_path} 出错: {e}")
        return "error"

def analyze_packj(file_path, folder_type):
    """
    分析packj的检测结果
    如果文件为空或者含有"No risks found!"字符串，就证明是良性的
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if not content.strip() or "No risks found!" in content:
                return "benign"
            else:
                return "malware"
    except Exception as e:
        print(f"读取 {file_path} 出错: {e}")
        return "error"

def analyze_genie(file_path, folder_type):
    """
    分析genie的检测结果
    如果csv文件为空，就证明检测为良性的
    如果csv文件不为空，就证明检测为恶意的
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if not content.strip():
                return "benign"
            else:
                return "malware"
    except Exception as e:
        print(f"读取 {file_path} 出错: {e}")
        return "error"

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

def find_package_files(base_path, package_type):
    """递归查找所有的txt文件"""
    result = []
    package_path = os.path.join(base_path, package_type)
    
    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith('.txt') or file.endswith('.csv'):
                result.append(os.path.join(root, file))
    
    return result

def evaluate_tool(tool_name, tool_function, sub_tool=None):
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
        "malware_total": 0
    }
    
    # 处理良性样本
    benign_files = find_package_files(base_path, "benign")
    for file_path in benign_files:
        results["benign_total"] += 1
        prediction = tool_function(file_path, "benign")
        
        if prediction == "benign":
            results["true_negative"] += 1
        elif prediction == "malware":
            results["false_positive"] += 1
    
    # 处理恶意样本
    malware_files = find_package_files(base_path, "malware")
    for file_path in malware_files:
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
    # 定义工具和对应的分析函数
    basic_tools = {
        "ossgadget": analyze_ossgadget,
        "guarddog": analyze_guarddog,
        "genie": analyze_genie
    }
    
    # packj工具有两种检测方式
    packj_subtypes = ["result_static", "result_trace"]
    
    print("NPM恶意包检测工具效果统计:\n")
    print("| 工具名称 | 样本总数 | 准确率 | 精确度 | 召回率 | F1分数 |")
    print("| -------- | -------- | ------ | ------ | ------ | ------ |")
    
    # 评估基本工具
    for tool_name, tool_function in basic_tools.items():
        print(f"正在评估 {tool_name}...")
        results = evaluate_tool(tool_name, tool_function)
        
        total_samples = results["benign_total"] + results["malware_total"]
        print(
            f"| {tool_name} | {total_samples} | {results['accuracy']:.4f} | "
            f"{results['precision']:.4f} | {results['recall']:.4f} | {results['f1']:.4f} |"
        )
        
        print(f"\n{tool_name}详细结果:")
        print(f"良性样本总数: {results['benign_total']}")
        print(f"恶意样本总数: {results['malware_total']}")
        print(f"真阳性 (TP): {results['true_positive']} (正确识别恶意样本)")
        print(f"真阴性 (TN): {results['true_negative']} (正确识别良性样本)")
        print(f"假阳性 (FP): {results['false_positive']} (错误地将良性识别为恶意)")
        print(f"假阴性 (FN): {results['false_negative']} (错误地将恶意识别为良性)")
        print()
    
    # 评估packj工具的两种检测方式
    for subtype in packj_subtypes:
        tool_name = f"packj_{subtype.replace('result_', '')}"
        print(f"正在评估 {tool_name}...")
        results = evaluate_tool("packj", analyze_packj, subtype)
        
        total_samples = results["benign_total"] + results["malware_total"]
        print(
            f"| {tool_name} | {total_samples} | {results['accuracy']:.4f} | "
            f"{results['precision']:.4f} | {results['recall']:.4f} | {results['f1']:.4f} |"
        )
        
        print(f"\n{tool_name}详细结果:")
        print(f"良性样本总数: {results['benign_total']}")
        print(f"恶意样本总数: {results['malware_total']}")
        print(f"真阳性 (TP): {results['true_positive']} (正确识别恶意样本)")
        print(f"真阴性 (TN): {results['true_negative']} (正确识别良性样本)")
        print(f"假阳性 (FP): {results['false_positive']} (错误地将良性识别为恶意)")
        print(f"假阴性 (FN): {results['false_negative']} (错误地将恶意识别为良性)")
        print()

if __name__ == "__main__":
    main() 