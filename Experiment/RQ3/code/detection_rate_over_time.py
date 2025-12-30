#!/usr/bin/env python3
"""
RQ3: Detection Rate Analysis Over Time
Generates detection_rates_by_year.csv and fig_pie_samples_distribution
"""

import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib.path import Path as MPath
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent
TIMESTAMP_CSV = PROJECT_ROOT / "Core" / "Data" / "timecollect" / "time" / "malware_time.csv"
STATS_OUTPUT_DIR = PROJECT_ROOT / "Core" / "ToolDetection" / "DetectionResults"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic"

TOOL_DISPLAY_NAMES = {
    'genie': 'GENIE', 'guarddog': 'GuardDog', 'ossgadget': 'OSSGadget',
    'packj_static': 'Packj-Static', 'packj_trace': 'Packj-Trace',
    'sap_DT': 'SAP-DT', 'sap_RF': 'SAP-RF', 'sap_XGB': 'SAP-XGB',
    'socketai': 'SocketAI', 'cerebro': 'Cerebro',
    'malpacdetector_mlp': 'MalPac-MLP', 'malpacdetector_nb': 'MalPac-NB',
    'malpacdetector_svm': 'MalPac-SVM'
}


def group_years(year):
    if pd.isna(year):
        return 'Unknown'
    elif year <= 2020:
        return '2011-2020'
    elif year == 2021:
        return '2021'
    elif year == 2022:
        return '2022'
    elif year == 2023:
        return '2023'
    elif year >= 2024:
        return '2024-2025'
    return 'Unknown'


def load_time_data():
    print("Loading timestamp data...")
    time_data = pd.read_csv(TIMESTAMP_CSV)
    time_data['package_id'] = time_data['package_name'] + '/' + time_data['version'].astype(str)
    time_data['timestamp'] = pd.to_datetime(time_data['timestamp'], errors='coerce')
    time_data['year'] = time_data['timestamp'].dt.year
    time_data['year_group'] = time_data['year'].apply(group_years)
    print(f"Loaded {len(time_data)} records")
    return time_data


def load_detection_data():
    print("Loading detection data...")
    detection_data = {}

    tool_dirs = [d for d in os.listdir(STATS_OUTPUT_DIR)
                if os.path.isdir(os.path.join(STATS_OUTPUT_DIR, d))]

    for tool in tool_dirs:
        tool_path = os.path.join(STATS_OUTPUT_DIR, tool)
        fn_path = os.path.join(tool_path, 'false_negatives.json')
        malicious_path = os.path.join(tool_path, 'malicious_reports.json')

        tool_data = {'false_negatives': {}, 'true_positives': {}}

        if os.path.exists(fn_path):
            with open(fn_path, 'r') as f:
                tool_data['false_negatives'] = json.load(f)

        if os.path.exists(malicious_path):
            with open(malicious_path, 'r') as f:
                malicious_data = json.load(f)
                for pkg_id, info in malicious_data.items():
                    if isinstance(info, dict) and info.get('actual') == 'malware' and info.get('prediction') == 'malware':
                        tool_data['true_positives'][pkg_id] = info

        detection_data[tool] = tool_data
        print(f"  {tool}: {len(tool_data['false_negatives'])} FN, {len(tool_data['true_positives'])} TP")

    return detection_data


def combine_data(time_data, detection_data):
    print("Combining data...")
    combined_data = {}

    for tool, tool_data in detection_data.items():
        combined_tool_data = defaultdict(lambda: defaultdict(lambda: {'detected': 0, 'missed': 0, 'total': 0}))

        for pkg_id in tool_data['false_negatives']:
            clean_pkg_id = pkg_id.replace('##', '/')
            time_match = time_data[time_data['package_id'] == clean_pkg_id]
            year_group = time_match.iloc[0]['year_group'] if not time_match.empty else 'Unknown'
            combined_tool_data[year_group]['malware']['missed'] += 1
            combined_tool_data[year_group]['malware']['total'] += 1

        for pkg_id in tool_data['true_positives']:
            clean_pkg_id = pkg_id.replace('##', '/')
            time_match = time_data[time_data['package_id'] == clean_pkg_id]
            year_group = time_match.iloc[0]['year_group'] if not time_match.empty else 'Unknown'
            combined_tool_data[year_group]['malware']['detected'] += 1
            combined_tool_data[year_group]['malware']['total'] += 1

        combined_data[tool] = dict(combined_tool_data)

    return combined_data


def calculate_detection_rates(combined_data):
    detection_rates = {}

    for tool, tool_data in combined_data.items():
        detection_rates[tool] = {}
        for year_group, categories in tool_data.items():
            if 'malware' in categories:
                stats = categories['malware']
                total = stats['total']
                if total > 0:
                    detection_rates[tool][year_group] = {
                        'detection_rate': (stats['detected'] / total) * 100,
                        'detected': stats['detected'],
                        'missed': stats['missed'],
                        'total': total
                    }

    return detection_rates


def save_detection_rates_csv(detection_rates):
    rows = []
    for tool, tool_data in detection_rates.items():
        for year_group, stats in tool_data.items():
            rows.append({
                'tool': tool,
                'tool_display': TOOL_DISPLAY_NAMES.get(tool, tool),
                'year_group': year_group,
                'detection_rate': stats['detection_rate'],
                'detected': stats['detected'],
                'missed': stats['missed'],
                'total': stats['total']
            })

    df = pd.DataFrame(rows)
    csv_file = OUTPUT_DIR / 'detection_rates_by_year.csv'
    df.to_csv(csv_file, index=False)
    print(f"Saved: {csv_file}")


def create_pie_chart(time_data):
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
    mpl.rcParams['pdf.fonttype'] = 42

    year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']
    year_totals = {yg: len(time_data[time_data['year_group'] == yg]) for yg in year_groups}
    sizes = [year_totals[yg] for yg in year_groups]
    total = sum(sizes)

    colors = ['#1a5fb4', '#26a269', '#e5a50a', '#c01c28', '#613583']

    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    fig.patch.set_facecolor('white')

    wedges, _ = ax.pie(
        sizes, colors=colors, startangle=90,
        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2),
        radius=1.0
    )

    centre_circle = plt.Circle((0, 0), 0.58, fc='white', ec='none')
    ax.add_patch(centre_circle)

    ax.text(0, 0.08, f'{total:,}', ha='center', va='center',
            fontsize=42, fontweight='bold', color='#1a1a1a', fontfamily='serif')
    ax.text(0, -0.20, 'Total Samples', ha='center', va='center',
            fontsize=16, color='#333333', fontfamily='serif')

    label_positions = {
        '2011-2020': (-1.45, 0.9, 'right'),
        '2021': (-1.45, 0.35, 'right'),
        '2022': (-1.45, -0.45, 'right'),
        '2023': (1.45, -0.45, 'left'),
        '2024-2025': (1.45, 0.5, 'left'),
    }

    for i, (wedge, label) in enumerate(zip(wedges, year_groups)):
        ang = (wedge.theta2 + wedge.theta1) / 2
        ang_rad = np.deg2rad(ang)
        pct = sizes[i] / total * 100
        count = year_totals[label]

        r_edge = 0.78
        x_start = r_edge * np.cos(ang_rad)
        y_start = r_edge * np.sin(ang_rad)
        x_end, y_end, ha = label_positions[label]

        r_ctrl = 1.15
        x_ctrl = r_ctrl * np.cos(ang_rad)
        y_ctrl = r_ctrl * np.sin(ang_rad)

        verts = [(x_start, y_start), (x_ctrl, y_ctrl), (x_end, y_end)]
        codes = [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3]
        path = MPath(verts, codes)
        patch = mpatches.PathPatch(path, facecolor='none', edgecolor=colors[i],
                                   linewidth=1.8, capstyle='round', alpha=0.8)
        ax.add_patch(patch)

        ax.scatter([x_start], [y_start], color=colors[i], s=50, zorder=5,
                  edgecolors='white', linewidths=1.5)

        box_width = 0.10
        box_x = x_end - 0.02 if ha == 'left' else x_end + 0.02 - box_width
        rect = mpatches.Rectangle((box_x, y_end - 0.15), box_width, 0.30,
                                  facecolor=colors[i], edgecolor='none', zorder=5)
        ax.add_patch(rect)

        text_x = x_end + 0.18 if ha == 'left' else x_end - 0.18
        ax.text(text_x, y_end + 0.08, label, ha=ha, va='bottom',
               fontsize=18, fontweight='bold', color='#1a1a1a', fontfamily='serif')
        ax.text(text_x, y_end - 0.08, f'{count:,} ({pct:.1f}%)', ha=ha, va='top',
               fontsize=15, fontweight='medium', color='#333333', fontfamily='serif')

    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'fig_pie_samples_distribution.{fmt}'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")

    plt.close()


def main():
    print("RQ3: Detection Rate Analysis Over Time")
    print("=" * 60)

    if not TIMESTAMP_CSV.exists():
        print(f"Error: {TIMESTAMP_CSV} not found")
        return

    if not STATS_OUTPUT_DIR.exists():
        print(f"Error: {STATS_OUTPUT_DIR} not found")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    time_data = load_time_data()
    detection_data = load_detection_data()
    combined_data = combine_data(time_data, detection_data)
    detection_rates = calculate_detection_rates(combined_data)

    save_detection_rates_csv(detection_rates)
    create_pie_chart(time_data)

    print("Done!")


if __name__ == "__main__":
    main()
