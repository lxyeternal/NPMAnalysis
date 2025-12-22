#!/usr/bin/env python3
"""
RQ2: Detection Accuracy Table Generator
Generates detection accuracy tables for malware classification analysis.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# Get the base directory
SCRIPT_DIR = Path(__file__).parent.resolve()

# Input/Output paths
INPUT_CSV = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "data" / "combined_malware_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "data"


def load_and_process_data(csv_file):
    """加载并处理恶意软件分析数据"""
    df = pd.read_csv(csv_file)

    # 计算每个工具和分类的检测率
    detection_rates = []

    for tool in df['tool'].unique():
        tool_data = df[df['tool'] == tool]

        for classification in tool_data['classification'].unique():
            class_data = tool_data[tool_data['classification'] == classification]

            # 获取假阴性和恶意报告计数
            fn_count = class_data[class_data['category'] == 'false_negatives']['count'].values
            mr_count = class_data[class_data['category'] == 'malicious_reports']['count'].values

            if len(fn_count) > 0 and len(mr_count) > 0:
                fn = fn_count[0]
                mr = mr_count[0]
                total = fn + mr
                detection_rate = (mr / total) * 100 if total > 0 else 0

                detection_rates.append({
                    'tool': tool,
                    'classification': classification,
                    'detection_rate': detection_rate,
                    'false_negatives': fn,
                    'malicious_reports': mr,
                    'total': total
                })

    return pd.DataFrame(detection_rates)


def create_detection_rate_table(detection_df, output_file):
    """创建检测率表格并保存到文件"""
    # 获取唯一的工具和分类
    tools = sorted(detection_df['tool'].unique())
    classifications = sorted(detection_df['classification'].unique())

    # 创建空的DataFrame作为表格 - 一个用于比例，一个用于数量
    rate_df = pd.DataFrame(index=tools, columns=classifications)
    count_df = pd.DataFrame(index=tools, columns=classifications)

    # 填充表格数据
    for _, row in detection_df.iterrows():
        tool = row['tool']
        classification = row['classification']
        detection_rate = row['detection_rate']
        mr = row['malicious_reports']
        fn = row['false_negatives']

        # 格式化为"比例% (正确检测/总数)"
        rate_df.loc[tool, classification] = f"{detection_rate:.2f}%"
        count_df.loc[tool, classification] = f"({mr}/{mr+fn})"

    # 将NaN值替换为"N/A"
    rate_df = rate_df.fillna("N/A")
    count_df = count_df.fillna("N/A")

    # 保存为文本文件
    with open(output_file, 'w') as f:
        # 写入标题
        f.write("Detection Rate Table for Tools and Malware Behaviors\n")
        f.write("=" * 80 + "\n\n")
        f.write("Format: Detection Rate% (Correctly Detected/Total Samples)\n\n")

        # 写入表格
        # 计算每列的最大宽度 (考虑到比例和数量的组合)
        col_widths = []
        for c in classifications:
            max_width = len(str(c))
            for t in tools:
                rate_str = str(rate_df.loc[t, c]) if pd.notna(rate_df.loc[t, c]) else "N/A"
                count_str = str(count_df.loc[t, c]) if pd.notna(count_df.loc[t, c]) else "N/A"
                combined_str = f"{rate_str} {count_str}"
                max_width = max(max_width, len(combined_str))
            col_widths.append(max_width)

        tool_width = max([len(t) for t in tools])

        # 写入表头
        f.write(f"{'':<{tool_width}} | ")
        for i, c in enumerate(classifications):
            f.write(f"{c:<{col_widths[i]}} | ")
        f.write("\n")

        # 写入分隔线
        f.write("-" * tool_width + "-+-")
        for i in range(len(classifications)):
            f.write("-" * col_widths[i] + "-+-")
        f.write("\n")

        # 写入数据行
        for t in tools:
            f.write(f"{t:<{tool_width}} | ")
            for i, c in enumerate(classifications):
                rate_str = str(rate_df.loc[t, c]) if pd.notna(rate_df.loc[t, c]) else "N/A"
                count_str = str(count_df.loc[t, c]) if pd.notna(count_df.loc[t, c]) else "N/A"
                combined_str = f"{rate_str} {count_str}"
                f.write(f"{combined_str:<{col_widths[i]}} | ")
            f.write("\n")

        # 写入总结信息
        f.write("\n\n")
        f.write("Detection Rate Summary:\n")
        f.write("-" * 40 + "\n")

        # 计算每个工具的平均检测率和总检测数量
        for tool in tools:
            tool_data = detection_df[detection_df['tool'] == tool]
            avg_rate = tool_data['detection_rate'].mean()
            total_mr = tool_data['malicious_reports'].sum()
            total_samples = tool_data['total'].sum()
            f.write(f"{tool} Avg Detection Rate: {avg_rate:.2f}% (Total: {total_mr}/{total_samples})\n")

        f.write("\n")

        # 计算每个分类的平均检测率和总检测数量
        for classification in classifications:
            class_data = detection_df[detection_df['classification'] == classification]
            avg_rate = class_data['detection_rate'].mean()
            total_mr = class_data['malicious_reports'].sum()
            total_samples = class_data['total'].sum()
            f.write(f"{classification} Avg Detection Rate: {avg_rate:.2f}% (Total: {total_mr}/{total_samples})\n")


def create_detailed_csv(detection_df, output_file):
    """创建详细的CSV表格，包含检测率和数量"""
    # 透视表 - 检测率
    rate_pivot = detection_df.pivot(index='tool', columns='classification', values='detection_rate')
    rate_pivot = rate_pivot.round(2)

    # 透视表 - 正确检测数
    mr_pivot = detection_df.pivot(index='tool', columns='classification', values='malicious_reports')

    # 透视表 - 总样本数
    total_pivot = detection_df.pivot(index='tool', columns='classification', values='total')

    # 合并数据到一个DataFrame
    result_df = pd.DataFrame()

    # 对于每个工具和分类，创建包含检测率和数量的条目
    for tool in rate_pivot.index:
        for col in rate_pivot.columns:
            if pd.notna(rate_pivot.loc[tool, col]):
                result_df.loc[tool, f"{col}_rate"] = rate_pivot.loc[tool, col]
                result_df.loc[tool, f"{col}_correct"] = mr_pivot.loc[tool, col]
                result_df.loc[tool, f"{col}_total"] = total_pivot.loc[tool, col]

    # 保存到CSV
    result_df.to_csv(output_file)


def main():
    """主函数，运行完整分析"""
    print(f"Input CSV: {INPUT_CSV}")
    print(f"Output dir: {OUTPUT_DIR}")

    try:
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # 加载并处理数据
        print("Loading and processing data...")
        detection_df = load_and_process_data(INPUT_CSV)

        # 创建检测率表格
        print("Creating detection rate table...")
        output_file = OUTPUT_DIR / "detection_accuracy_table.txt"
        create_detection_rate_table(detection_df, output_file)

        print(f"Table saved to: {output_file}")

        # 额外创建详细的CSV格式表格，方便导入到其他工具
        csv_output_file = OUTPUT_DIR / "detection_accuracy_table.csv"
        create_detailed_csv(detection_df, csv_output_file)

        print(f"Detailed CSV table saved to: {csv_output_file}")

    except FileNotFoundError:
        print(f"Error: Could not find the input CSV file at {INPUT_CSV}")
        print("Please run classify_statistic.py first to generate the data.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
