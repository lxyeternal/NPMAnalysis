#!/usr/bin/env python3
"""
RQ3: Radar Charts for Detection Tools by Category (1x4 layout)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
from math import pi

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic"
DATA_FILE = OUTPUT_DIR / "detection_rates_by_year.csv"

TOOL_CATEGORIES = {
    'Static-Based': {
        'tools': ['ossgadget', 'guarddog', 'genie', 'packj_static'],
        'colors': ['#1e88e5', '#fb8c00', '#e53935', '#8e24aa'],
    },
    'Dynamic-Based': {
        'tools': ['packj_trace'],
        'colors': ['#5e35b1'],
    },
    'ML-Based': {
        'tools': ['sap_DT', 'sap_RF', 'sap_XGB', 'cerebro',
                  'malpacdetector_mlp', 'malpacdetector_nb', 'malpacdetector_svm'],
        'colors': ['#43a047', '#00897b', '#00acc1', '#ff7043', '#7e57c2', '#26a69a', '#ec407a'],
    },
    'LLM-Based': {
        'tools': ['socketai'],
        'colors': ['#d81b60'],
    }
}

TOOL_NAMES = {
    'guarddog': 'GuardDog', 'ossgadget': 'OSSGadget',
    'sap_DT': 'SAP-DT', 'sap_RF': 'SAP-RF', 'sap_XGB': 'SAP-XGB',
    'genie': 'GENIE', 'packj_static': 'Packj-Static', 'packj_trace': 'Packj-Trace',
    'socketai': 'SocketAI', 'cerebro': 'Cerebro',
    'malpacdetector_mlp': 'MalPac-MLP', 'malpacdetector_nb': 'MalPac-NB',
    'malpacdetector_svm': 'MalPac-SVM'
}

TITLE_COLORS = {
    'Static-Based': '#1565c0', 'Dynamic-Based': '#6a1b9a',
    'ML-Based': '#2e7d32', 'LLM-Based': '#c2185b'
}


def create_radar_chart():
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    df = pd.read_csv(DATA_FILE)

    time_periods = ['2011-2020', '2021', '2022', '2023', '2024-2025']
    short_labels = ["'11-20", "'21", "'22", "'23", "'24-25"]
    num_vars = len(time_periods)

    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, axes = plt.subplots(1, 4, figsize=(22, 6.5), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')

    markers = ['o', 's', '^', 'D', 'v', 'p', 'h']

    for idx, (category, info) in enumerate(TOOL_CATEGORIES.items()):
        ax = axes[idx]
        tools = info['tools']
        colors = info['colors']

        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(short_labels, fontsize=16, fontweight='bold', color='#1a1a1a')
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=12, color='#666666')
        ax.grid(color='#d0d0d0', linestyle='-', linewidth=1, alpha=0.9)
        ax.spines['polar'].set_color('#aaaaaa')
        ax.spines['polar'].set_linewidth(1.5)
        ax.set_facecolor('#f8f9fa')

        for i, tool in enumerate(tools):
            tool_data = df[df['tool'] == tool]
            values = []
            for period in time_periods:
                rate_row = tool_data[tool_data['year_group'] == period]
                values.append(rate_row['detection_rate'].values[0] if not rate_row.empty else 0)
            values += values[:1]
            color = colors[i % len(colors)]

            ax.plot(angles, values, linewidth=3.5, color=color, label=TOOL_NAMES[tool],
                    marker=markers[i % len(markers)], markersize=11,
                    markerfacecolor=color, markeredgecolor='white', markeredgewidth=2.5, zorder=3)
            ax.fill(angles, values, color=color, alpha=0.12)

        ax.set_title(category, fontsize=22, fontweight='bold',
                     color=TITLE_COLORS[category], pad=22, y=1.10)

        ncol = min(len(tools), 4)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                  fontsize=11, frameon=False, ncol=ncol,
                  columnspacing=0.5, handletextpad=0.3)

    plt.tight_layout(pad=1.5)
    plt.subplots_adjust(wspace=0.32, bottom=0.18)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'fig_radar_beautiful.{fmt}'
        plt.savefig(output_file, dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")

    plt.close()


if __name__ == "__main__":
    print("Creating radar chart...")
    create_radar_chart()
    print("Done!")
