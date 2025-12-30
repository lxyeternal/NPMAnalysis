#!/usr/bin/env python3
"""
RQ3: API Evolution Visualization (1x4 layout)
Generates fig_api_trends_1x4.png and fig_api_trends_1x4.pdf
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['axes.unicode_minus'] = False

API_DIR = Path("/home2/wenbo/Documents/NPMAnalysis/Experiment/RQ3/statistic/api_extraction")
TIME_CSV = Path("/home2/wenbo/Documents/NPMAnalysis/Core/Data/timecollect/time/malware_time.csv")
OUTPUT_DIR = Path("/home2/wenbo/Documents/NPMAnalysis/Experiment/RQ3/statistic")

TIME_PERIODS = ['2011-2020', '2021', '2022', '2023', '2024-2025']
CATEGORIES = ['network', 'execution', 'filesystem', 'system_info', 'process_info', 'encoding', 'crypto']

COLORS = {
    'network': '#C0392B', 'execution': '#8E44AD', 'filesystem': '#2980B9',
    'system_info': '#16A085', 'process_info': '#D35400', 'encoding': '#27AE60', 'crypto': '#2C3E50',
}

CATEGORY_LABELS = {
    'network': 'Network', 'execution': 'Execution', 'filesystem': 'FileSystem',
    'system_info': 'System Info', 'process_info': 'Process Info',
    'encoding': 'Encoding', 'crypto': 'Crypto'
}


def load_time_mapping():
    df = pd.read_csv(TIME_CSV)

    def get_year_group(timestamp):
        if pd.isna(timestamp):
            return 'Unknown'
        try:
            year = int(str(timestamp)[:4])
            if year <= 2020:
                return '2011-2020'
            elif year == 2021:
                return '2021'
            elif year == 2022:
                return '2022'
            elif year == 2023:
                return '2023'
            else:
                return '2024-2025'
        except:
            return 'Unknown'

    mapping = {}
    for _, row in df.iterrows():
        pkg = row['package_name']
        pkg_normalized = pkg.replace('##', '/')
        year_group = get_year_group(row.get('timestamp', ''))
        if year_group != 'Unknown':
            mapping[pkg] = year_group
            mapping[pkg_normalized] = year_group
    return mapping


def load_api_data(time_mapping):
    data = []
    for pkg_dir in API_DIR.iterdir():
        if not pkg_dir.is_dir() or pkg_dir.name.endswith('.json'):
            continue
        pkg_name = pkg_dir.name
        time_period = time_mapping.get(pkg_name) or time_mapping.get(pkg_name.replace('##', '/'))
        if not time_period or time_period == 'Unknown':
            continue

        for version_dir in pkg_dir.iterdir():
            if not version_dir.is_dir():
                continue
            apis_file = version_dir / "apis.json"
            if not apis_file.exists():
                continue
            try:
                with open(apis_file, 'r') as f:
                    api_data = json.load(f)
                summary = api_data.get('summary', {})
                category_counts = summary.get('category_counts', {})
                record = {
                    'package': pkg_name,
                    'version': version_dir.name,
                    'time_period': time_period,
                    'total_apis': summary.get('total_apis', 0),
                }
                for cat in CATEGORIES:
                    record[cat] = category_counts.get(cat, 0)
                record['category_diversity'] = sum(1 for cat in CATEGORIES if category_counts.get(cat, 0) > 0)
                data.append(record)
            except:
                continue
    return pd.DataFrame(data)


def generate_api_trends_figure(df):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))

    pivot = df.groupby('time_period')[CATEGORIES].sum().reindex(TIME_PERIODS)
    x = np.arange(len(TIME_PERIODS))

    groups = [
        (['network', 'filesystem'], 'Data Access vs Transfer', ['#C0392B', '#2980B9']),
        (['system_info', 'process_info'], 'System Reconnaissance', ['#16A085', '#D35400']),
        (['execution', 'crypto'], 'Code Exec & Crypto', ['#8E44AD', '#2C3E50']),
        (['encoding'], 'Data Encoding', ['#27AE60']),
    ]

    for idx, (cats, title, colors) in enumerate(groups):
        ax = axes[idx]

        for cat_idx, cat in enumerate(cats):
            values = pivot[cat].values
            ax.plot(x, values, 'o-', linewidth=3, markersize=10,
                    color=colors[cat_idx] if cat_idx < len(colors) else colors[0],
                    label=CATEGORY_LABELS[cat])
            ax.fill_between(x, 0, values, alpha=0.15,
                            color=colors[cat_idx] if cat_idx < len(colors) else colors[0])

        ax.set_xticks(x)
        ax.set_xticklabels(TIME_PERIODS, fontsize=11, rotation=15)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(fontsize=11, loc='upper left')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'fig_api_trends_1x4.{fmt}'
        plt.savefig(output_file, dpi=300 if fmt == 'png' else None,
                    bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")

    plt.close()


def main():
    print("RQ3: API Evolution Visualization")
    print("=" * 60)

    print("Loading data...")
    time_mapping = load_time_mapping()
    df = load_api_data(time_mapping)
    print(f"  {len(df)} records loaded")

    print("Generating figure...")
    generate_api_trends_figure(df)
    print("Done!")


if __name__ == "__main__":
    main()
