#!/usr/bin/env python3
"""
RQ2: Analyze Evasion Technique Combinations
Generates two_evade_combinations_analysis.csv/json
"""

import pandas as pd
import json
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_FILE = SCRIPT_DIR.parent / "statistic" / "input" / "package_category_summary.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "data"


def analyze_evade_combinations():
    print("Loading data...")
    df = pd.read_csv(INPUT_FILE)
    print(f"Total records: {len(df)}")

    two_category_df = df[df['category_count'] == 2].copy()
    print(f"Records with exactly 2 categories: {len(two_category_df)}")

    combination_counter = Counter()
    for _, row in two_category_df.iterrows():
        categories = row['categories'].split(';')
        if len(categories) == 2:
            combo = tuple(sorted(categories))
            combination_counter[combo] += 1

    sorted_combinations = combination_counter.most_common()

    print(f"\nFound {len(sorted_combinations)} unique combinations")
    print("\nTop 10 combinations:")
    for i, ((cat1, cat2), count) in enumerate(sorted_combinations[:10], 1):
        pct = (count / len(two_category_df)) * 100
        print(f"  {i}. {cat1} + {cat2}: {count} ({pct:.2f}%)")

    results = {
        "total_two_category_packages": len(two_category_df),
        "total_combinations": len(sorted_combinations),
        "combinations": [
            {"category1": cat1, "category2": cat2, "count": count,
             "percentage": round((count / len(two_category_df)) * 100, 2)}
            for (cat1, cat2), count in sorted_combinations
        ]
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_file = OUTPUT_DIR / "two_evade_combinations_analysis.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    csv_file = OUTPUT_DIR / "two_evade_combinations_analysis.csv"
    pd.DataFrame([
        {"Category1": cat1, "Category2": cat2, "Count": count,
         "Percentage": round((count / len(two_category_df)) * 100, 2)}
        for (cat1, cat2), count in sorted_combinations
    ]).to_csv(csv_file, index=False)

    print(f"\nSaved: {json_file}")
    print(f"Saved: {csv_file}")

    return results


if __name__ == "__main__":
    analyze_evade_combinations()
