#!/usr/bin/env python3
import os
import glob
import fnmatch
import pandas as pd
import numpy as np
from collections import defaultdict
import itertools

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
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "Found 0 potentially malicious indicators" in content:
                return "benign"
            else:
                return "malware"
    except:
        return None

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
    except:
        return None

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
    except:
        return None

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
    except:
        return None

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
    
    if not os.path.exists(package_path):
        return result
        
    for root, dirs, files in os.walk(package_path):
        for file in files:
            if file.endswith('.txt') or file.endswith('.csv'):
                result.append(os.path.join(root, file))
    
    return result

class MultiToolFusion:
    def __init__(self, malware_benign_skip_list=None, selected_benign_skip_list=None):
        # 存储每个工具在每个样本上的检测结果
        self.tool_results = {}  # {sample_id: {tool_name: prediction}}
        self.ground_truth = {}  # {sample_id: true_label}
        self.tool_names = ['ossgadget', 'guarddog', 'genie', 'packj_static', 'packj_trace']
        
        # 需要跳过的包列表
        self.malware_benign_skip_list = malware_benign_skip_list or set()
        self.selected_benign_skip_list = selected_benign_skip_list or set()
        
        # 统计跳过的样本数
        self.skipped_samples = {'malware': 0, 'benign': 0}
        
    def should_skip_sample(self, package_info, true_label):
        """判断是否需要跳过当前样本"""
        # 将包名/版本格式转换为包名$$版本格式，与原代码保持一致
        converted_package_info = package_info.replace('/', '$$')
        
        if true_label == 'malware' and converted_package_info in self.malware_benign_skip_list:
            return True
        elif true_label == 'benign' and converted_package_info in self.selected_benign_skip_list:
            return True
        return False
    
    def collect_tool_results(self, sample_id, package_info, tool_predictions, true_label):
        """收集单个样本的所有工具检测结果，包含跳过逻辑"""
        # 检查是否需要跳过
        if self.should_skip_sample(package_info, true_label):
            self.skipped_samples[true_label] += 1
            return False  # 返回False表示样本被跳过
        
        # 只收集未被跳过的样本
        self.tool_results[sample_id] = tool_predictions
        self.ground_truth[sample_id] = true_label
        return True  # 返回True表示样本被收集
    
    def calculate_single_tool_performance(self):
        """计算每个工具的单独性能"""
        performance = {}
        
        for tool in self.tool_names:
            tp = tn = fp = fn = 0
            
            for sample_id in self.tool_results:
                if tool not in self.tool_results[sample_id]:
                    continue
                    
                pred = self.tool_results[sample_id][tool]
                true = self.ground_truth[sample_id]
                
                if pred == 'malware' and true == 'malware':
                    tp += 1
                elif pred == 'benign' and true == 'benign':
                    tn += 1
                elif pred == 'malware' and true == 'benign':
                    fp += 1
                elif pred == 'benign' and true == 'malware':
                    fn += 1
            
            # 计算指标
            total = tp + tn + fp + fn
            if total > 0:
                accuracy = (tp + tn) / total
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # 误报率
                fnr = fn / (fn + tp) if (fn + tp) > 0 else 0  # 漏报率
                
                performance[tool] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1': f1,
                    'fpr': fpr,
                    'fnr': fnr,
                    'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn
                }
        
        return performance
    
    def majority_voting(self, threshold_ratio=0.5):
        """多数投票融合策略"""
        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
        threshold = max(1, int(len(self.tool_names) * threshold_ratio))
        
        for sample_id in self.tool_results:
            malware_votes = 0
            total_votes = 0
            
            for tool in self.tool_names:
                if tool in self.tool_results[sample_id] and self.tool_results[sample_id][tool] is not None:
                    total_votes += 1
                    if self.tool_results[sample_id][tool] == 'malware':
                        malware_votes += 1
            
            if total_votes == 0:
                continue
                
            # 融合决策
            fusion_pred = 'malware' if malware_votes >= threshold else 'benign'
            true_label = self.ground_truth[sample_id]
            
            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1
        
        return self._calculate_metrics(results)
    
    def weighted_voting(self, weights=None):
        """加权投票融合策略"""
        if weights is None:
            # 基于F1分数计算权重
            performance = self.calculate_single_tool_performance()
            weights = {}
            total_f1 = sum(performance[tool]['f1'] for tool in performance if performance[tool]['f1'] > 0)
            for tool in self.tool_names:
                if tool in performance and total_f1 > 0:
                    weights[tool] = performance[tool]['f1'] / total_f1
                else:
                    weights[tool] = 1/len(self.tool_names)
        
        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
        
        for sample_id in self.tool_results:
            weighted_score = 0
            total_weight = 0
            
            for tool in self.tool_names:
                if tool in self.tool_results[sample_id] and self.tool_results[sample_id][tool] is not None and tool in weights:
                    if self.tool_results[sample_id][tool] == 'malware':
                        weighted_score += weights[tool]
                    total_weight += weights[tool]
            
            if total_weight == 0:
                continue
                
            # 融合决策 (阈值为0.5)
            fusion_pred = 'malware' if weighted_score > total_weight * 0.5 else 'benign'
            true_label = self.ground_truth[sample_id]
            
            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1
        
        return self._calculate_metrics(results), weights
    
    def conservative_aggressive_fusion(self):
        """保守-激进融合策略"""
        performance = self.calculate_single_tool_performance()
        
        if not performance:
            return self._calculate_metrics({'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}), None, None
        
        # 找出误报率最低的工具（保守工具）
        conservative_tool = min(performance.keys(), key=lambda x: performance[x]['fpr'])
        # 找出召回率最高的工具（激进工具）
        aggressive_tool = max(performance.keys(), key=lambda x: performance[x]['recall'])
        
        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
        
        for sample_id in self.tool_results:
            conservative_pred = self.tool_results[sample_id].get(conservative_tool)
            aggressive_pred = self.tool_results[sample_id].get(aggressive_tool)
            
            # 融合策略：保守工具说恶意就是恶意，否则看激进工具
            if conservative_pred == 'malware':
                fusion_pred = 'malware'
            elif aggressive_pred is not None:
                fusion_pred = aggressive_pred
            else:
                fusion_pred = 'benign'
            
            true_label = self.ground_truth[sample_id]
            
            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1
        
        return self._calculate_metrics(results), conservative_tool, aggressive_tool
    
    def unanimous_voting(self):
        """一致投票：所有工具一致才做决策"""
        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0, 'uncertain': 0}
        
        for sample_id in self.tool_results:
            predictions = []
            for tool in self.tool_names:
                if tool in self.tool_results[sample_id] and self.tool_results[sample_id][tool] is not None:
                    predictions.append(self.tool_results[sample_id][tool])
            
            if len(predictions) == 0:
                continue
                
            if len(set(predictions)) == 1:  # 所有工具一致
                fusion_pred = predictions[0]
            else:  # 不一致，标记为不确定
                results['uncertain'] += 1
                continue
            
            true_label = self.ground_truth[sample_id]
            
            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1
        
        return self._calculate_metrics(results), results['uncertain']
    
    def _calculate_metrics(self, results):
        """计算性能指标"""
        tp, tn, fp, fn = results['tp'], results['tn'], results['fp'], results['fn']
        total = tp + tn + fp + fn
        
        if total == 0:
            return {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1': 0, 'fpr': 0, 'fnr': 0, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}
        
        accuracy = (tp + tn) / total
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'fpr': fpr,
            'fnr': fnr,
            'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn
        }
    
    def comprehensive_evaluation(self):
        """全面评估所有融合策略"""
        print("=" * 80)
        print("RQ4: 多工具融合策略综合评估")
        print("=" * 80)
        
        # 显示数据统计信息
        total_samples = len(self.tool_results)
        malware_samples = sum(1 for label in self.ground_truth.values() if label == 'malware')
        benign_samples = sum(1 for label in self.ground_truth.values() if label == 'benign')
        
        print(f"\n数据集统计:")
        print(f"有效样本总数: {total_samples}")
        print(f"  - 恶意样本: {malware_samples}")
        print(f"  - 良性样本: {benign_samples}")
        print(f"跳过样本总数: {sum(self.skipped_samples.values())}")
        print(f"  - 跳过恶意样本: {self.skipped_samples['malware']}")
        print(f"  - 跳过良性样本: {self.skipped_samples['benign']}")
        
        if total_samples == 0:
            print("错误：没有有效样本进行分析！")
            return
        
        # 1. 单工具性能分析
        print("\n1. 单工具性能分析:")
        print("-" * 50)
        single_performance = self.calculate_single_tool_performance()
        
        if not single_performance:
            print("错误：没有工具性能数据！")
            return
        
        print("| 工具名称 | 准确率 | 精确率 | 召回率 | F1分数 | 误报率 | 漏报率 |")
        print("| -------- | ------ | ------ | ------ | ------ | ------ | ------ |")
        for tool, metrics in single_performance.items():
            print(f"| {tool:12} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
                  f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['fpr']:.4f} | {metrics['fnr']:.4f} |")
        
        # 2. 多数投票策略
        print("\n2. 多数投票策略评估:")
        print("-" * 50)
        voting_results = {}
        thresholds = [0.2, 0.4, 0.5, 0.6, 0.8]
        
        print("| 阈值比例 | 准确率 | 精确率 | 召回率 | F1分数 | 误报率 | 漏报率 |")
        print("| -------- | ------ | ------ | ------ | ------ | ------ | ------ |")
        for threshold in thresholds:
            metrics = self.majority_voting(threshold)
            voting_results[threshold] = metrics
            print(f"| {threshold:8.1f} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
                  f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['fpr']:.4f} | {metrics['fnr']:.4f} |")
        
        # 3. 加权投票策略
        print("\n3. 加权投票策略评估:")
        print("-" * 50)
        weighted_metrics, weights = self.weighted_voting()
        print("工具权重分配:")
        for tool, weight in weights.items():
            print(f"  {tool}: {weight:.4f}")
        
        print(f"\n加权投票结果:")
        print(f"准确率: {weighted_metrics['accuracy']:.4f}")
        print(f"精确率: {weighted_metrics['precision']:.4f}")
        print(f"召回率: {weighted_metrics['recall']:.4f}")
        print(f"F1分数: {weighted_metrics['f1']:.4f}")
        print(f"误报率: {weighted_metrics['fpr']:.4f}")
        print(f"漏报率: {weighted_metrics['fnr']:.4f}")
        
        # 4. 保守-激进融合策略
        print("\n4. 保守-激进融合策略评估:")
        print("-" * 50)
        ca_metrics, conservative_tool, aggressive_tool = self.conservative_aggressive_fusion()
        if conservative_tool and aggressive_tool:
            print(f"保守工具 (最低误报率): {conservative_tool}")
            print(f"激进工具 (最高召回率): {aggressive_tool}")
            print(f"融合结果:")
            print(f"准确率: {ca_metrics['accuracy']:.4f}")
            print(f"精确率: {ca_metrics['precision']:.4f}")
            print(f"召回率: {ca_metrics['recall']:.4f}")
            print(f"F1分数: {ca_metrics['f1']:.4f}")
            print(f"误报率: {ca_metrics['fpr']:.4f}")
            print(f"漏报率: {ca_metrics['fnr']:.4f}")
        
        # 5. 一致投票策略
        print("\n5. 一致投票策略评估:")
        print("-" * 50)
        unanimous_metrics, uncertain_count = self.unanimous_voting()
        print(f"不确定样本数量: {uncertain_count}")
        print(f"一致投票结果:")
        print(f"准确率: {unanimous_metrics['accuracy']:.4f}")
        print(f"精确率: {unanimous_metrics['precision']:.4f}")
        print(f"召回率: {unanimous_metrics['recall']:.4f}")
        print(f"F1分数: {unanimous_metrics['f1']:.4f}")
        print(f"误报率: {unanimous_metrics['fpr']:.4f}")
        print(f"漏报率: {unanimous_metrics['fnr']:.4f}")
        
        # 6. 综合对比分析
        print("\n6. 融合策略综合对比:")
        print("-" * 50)
        
        # 找出最佳单工具
        best_single_tool = max(single_performance.keys(), 
                              key=lambda x: single_performance[x]['f1'])
        best_single_f1 = single_performance[best_single_tool]['f1']
        
        # 找出最佳投票阈值
        best_voting_threshold = max(voting_results.keys(), 
                                   key=lambda x: voting_results[x]['f1'])
        best_voting_f1 = voting_results[best_voting_threshold]['f1']
        
        comparison_data = [
            ("最佳单工具", best_single_f1, single_performance[best_single_tool]),
            (f"多数投票(阈值{best_voting_threshold})", best_voting_f1, voting_results[best_voting_threshold]),
            ("加权投票", weighted_metrics['f1'], weighted_metrics),
            ("一致投票", unanimous_metrics['f1'], unanimous_metrics)
        ]
        
        if conservative_tool and aggressive_tool:
            comparison_data.append(("保守-激进融合", ca_metrics['f1'], ca_metrics))
        
        # 按F1分数排序
        comparison_data.sort(key=lambda x: x[1], reverse=True)
        
        print("| 策略名称 | F1分数 | 准确率 | 精确率 | 召回率 | 误报率 | 漏报率 |")
        print("| -------- | ------ | ------ | ------ | ------ | ------ | ------ |")
        for strategy, f1, metrics in comparison_data:
            print(f"| {strategy:16} | {f1:.4f} | {metrics['accuracy']:.4f} | "
                  f"{metrics['precision']:.4f} | {metrics['recall']:.4f} | "
                  f"{metrics['fpr']:.4f} | {metrics['fnr']:.4f} |")
        
        # 7. 结论和建议
        print("\n7. RQ4回答总结:")
        print("-" * 50)
        best_strategy = comparison_data[0]
        improvement = (best_strategy[1] - best_single_f1) / best_single_f1 * 100 if best_single_f1 > 0 else 0
        
        print(f"✓ 最佳融合策略: {best_strategy[0]}")
        print(f"✓ 相比最佳单工具提升: {improvement:.2f}%")
        print(f"✓ 工具互补性: {'有效' if improvement > 5 else '有限'}")
        
        if improvement > 5:
            print(f"✓ 建议: 采用{best_strategy[0]}策略进行多工具融合检测")
        else:
            print(f"✓ 建议: 工具融合收益有限，优先优化单工具性能")
        
        return comparison_data


def collect_all_tool_results(base_path, malware_benign_skip_list, selected_benign_skip_list):
    """收集所有工具在所有样本上的检测结果"""
    
    fusion_evaluator = MultiToolFusion(malware_benign_skip_list, selected_benign_skip_list)
    
    # 定义工具和对应的分析函数
    tools = {
        "ossgadget": analyze_ossgadget,
        "guarddog": analyze_guarddog,
        "genie": analyze_genie
    }
    
    # packj工具有两种检测方式
    packj_subtypes = ["result_static", "result_trace"]
    
    print("开始收集所有工具的检测结果...")
    
    # 收集样本 - 以某个工具的结果为基准来遍历所有样本
    base_tool = "ossgadget"  # 使用ossgadget作为基准工具
    base_tool_path = os.path.join(base_path, base_tool)
    
    sample_count = 0
    
    # 处理良性样本
    benign_files = find_package_files(base_tool_path, "benign")
    for file_path in benign_files:
        package_info = extract_package_info(file_path, "benign")
        sample_id = f"benign_{package_info}"
        
        # 为这个样本收集所有工具的结果
        tool_predictions = {}
        
        # 收集基础工具结果
        for tool_name, tool_function in tools.items():
            try:
                # 构造对应工具的文件路径
                tool_file_path = file_path.replace(f"/{base_tool}/", f"/{tool_name}/")
                if os.path.exists(tool_file_path):
                    result = tool_function(tool_file_path, "benign")
                    if result is not None:
                        tool_predictions[tool_name] = result
            except Exception as e:
                continue
        
        # 收集packj工具结果
        for subtype in packj_subtypes:
            tool_key = f"packj_{subtype.replace('result_', '')}"
            try:
                packj_file_path = file_path.replace(f"/{base_tool}/", f"/packj/{subtype}/")
                if os.path.exists(packj_file_path):
                    result = analyze_packj(packj_file_path, "malware")
                    if result is not None:
                        tool_predictions[tool_key] = result
            except Exception as e:
                continue
        
        # 只有当至少有2个工具有结果时才收集这个样本
        if len(tool_predictions) >= 2:
            if fusion_evaluator.collect_tool_results(sample_id, package_info, tool_predictions, "malware"):
                sample_count += 1
    
    print(f"成功收集了 {sample_count} 个样本的多工具检测结果")
    return fusion_evaluator


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
    
    # 工具结果文件的基础路径
    base_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output"
    
    # 收集所有工具的检测结果
    fusion_evaluator = collect_all_tool_results(base_path, malware_benign_skip_list, selected_benign_skip_list)
    
    # 执行融合策略评估
    if len(fusion_evaluator.tool_results) > 0:
        fusion_results = fusion_evaluator.comprehensive_evaluation()
    else:
        print("错误：没有收集到任何有效的工具检测结果！")
        print("请检查以下内容：")
        print("1. 路径是否正确：", base_path)
        print("2. 工具输出文件是否存在")
        print("3. 文件格式是否正确")


if __name__ == "__main__":
    main()