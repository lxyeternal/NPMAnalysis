#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析NPM恶意包中两个逃避技术同时出现的组合频率
"""

import pandas as pd
import os
from collections import Counter
from itertools import combinations
import json

def analyze_evade_combinations():
    """分析两个evade技术的组合频率"""
    from pathlib import Path

    # 文件路径 - 使用相对路径
    script_dir = Path(__file__).parent.resolve()
    input_file = script_dir.parent / "statistic" / "input" / "package_category_summary.csv"
    output_dir = script_dir.parent / "statistic" / "evasion_analysis" / "data"
    
    # 读取数据
    print("正在读取数据...")
    df = pd.read_csv(input_file)
    print(f"总共读取 {len(df)} 条记录")
    
    # 筛选出恰好有两个分类的记录
    two_category_df = df[df['category_count'] == 2].copy()
    print(f"筛选出 {len(two_category_df)} 条恰好有两个分类的记录")
    
    # 统计组合频率
    combination_counter = Counter()
    
    for _, row in two_category_df.iterrows():
        categories = row['categories'].split(';')
        # 确保只有两个分类
        if len(categories) == 2:
            # 对分类进行排序，确保组合的一致性（如 A;B 和 B;A 被认为是同一组合）
            combo = tuple(sorted(categories))
            combination_counter[combo] += 1
    
    # 按频次排序
    sorted_combinations = combination_counter.most_common()
    
    # 输出结果
    print("\n=== 两个逃避技术组合频率统计 ===")
    print(f"总共找到 {len(sorted_combinations)} 种不同的组合")
    print("\n排名前20的组合：")
    print("-" * 80)
    
    for i, ((cat1, cat2), count) in enumerate(sorted_combinations[:20], 1):
        percentage = (count / len(two_category_df)) * 100
        print(f"{i:2d}. {cat1} + {cat2}")
        print(f"    出现次数: {count}, 占比: {percentage:.2f}%")
        print()
    
    # 保存详细结果到文件
    results = {
        "total_two_category_packages": len(two_category_df),
        "total_combinations": len(sorted_combinations),
        "combinations": []
    }
    
    for (cat1, cat2), count in sorted_combinations:
        percentage = (count / len(two_category_df)) * 100
        results["combinations"].append({
            "category1": cat1,
            "category2": cat2,
            "count": count,
            "percentage": round(percentage, 2)
        })
    
    # 保存为JSON格式
    output_file = os.path.join(output_dir, "two_evade_combinations_analysis.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # 保存为CSV格式便于查看
    csv_output_file = os.path.join(output_dir, "two_evade_combinations_analysis.csv")
    combinations_df = pd.DataFrame([
        {
            "Category1": cat1,
            "Category2": cat2,
            "Count": count,
            "Percentage": round((count / len(two_category_df)) * 100, 2)
        }
        for (cat1, cat2), count in sorted_combinations
    ])
    combinations_df.to_csv(csv_output_file, index=False, encoding='utf-8')
    
    print(f"\n结果已保存到:")
    print(f"- JSON格式: {output_file}")
    print(f"- CSV格式: {csv_output_file}")
    
    # 分析最常见的分类
    print("\n=== 在两分类组合中最常出现的单个分类 ===")
    single_category_counter = Counter()
    for (cat1, cat2), count in sorted_combinations:
        single_category_counter[cat1] += count
        single_category_counter[cat2] += count
    
    print("排名前10的单个分类:")
    for i, (category, count) in enumerate(single_category_counter.most_common(10), 1):
        print(f"{i:2d}. {category}: {count} 次")
    
    return results

if __name__ == "__main__":
    analyze_evade_combinations() 