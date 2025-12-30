#!/usr/bin/env python3
"""
RQ2: Evasion Detection Heatmap
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from pathlib import Path

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['pdf.fonttype'] = 42

SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_CSV = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "data" / "tool_detection_by_category_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "figures"

TOOL_NAMES = {
    'genie': 'GENIE', 'guarddog': 'GuardDog', 'ossgadget': 'OSSGadget',
    'packj_static': 'Packj-Static', 'packj_trace': 'Packj-Trace',
    'sap_DT': 'SAP-DT', 'sap_RF': 'SAP-RF', 'sap_XGB': 'SAP-XGB',
    'socketai': 'SocketAI', 'cerebro': 'Cerebro',
    'malpacdetector_mlp': 'MalPac-MLP', 'malpacdetector_nb': 'MalPac-NB',
    'malpacdetector_svm': 'MalPac-SVM'
}

TOOL_ORDER = [
    'OSSGadget', 'GuardDog', 'GENIE', 'Packj-Static',
    'Packj-Trace',
    'SAP-DT', 'SAP-RF', 'SAP-XGB', 'MalPac-MLP', 'MalPac-NB', 'MalPac-SVM', 'Cerebro',
    'SocketAI'
]

CATEGORY_SHORT_NAMES = {
    'String_Obfuscation': 'String Obfusc.', 'Encoding_Obfuscation': 'Encoding Obfusc.',
    'Silent_Error_Handling': 'Silent Error', 'Hook_Abuse': 'Hook Abuse',
    'Code_Structure_Obfuscation': 'Code Struct.', 'Stealth_Execution': 'Stealth Exec.',
    'Module_Abuse': 'Module Abuse', 'Network_Communication_Hiding': 'Net. Hiding',
    'Environment_Detection': 'Env. Detection', 'Anti_Analysis': 'Anti-Analysis',
    'Trace_Cleanup': 'Trace Cleanup', 'Dependency_Confusion': 'Dep. Confusion',
    'Typosquatting': 'Typosquatting', 'Runtime_Caching': 'Runtime Cache'
}

CATEGORY_ORDER = [
    'Anti-Analysis', 'Trace Cleanup', 'Env. Detection', 'Stealth Exec.',
    'String Obfusc.', 'Silent Error', 'Code Struct.', 'Net. Hiding',
    'Encoding Obfusc.', 'Hook Abuse', 'Module Abuse',
    'Typosquatting', 'Runtime Cache', 'Dep. Confusion'
]


def load_data():
    df = pd.read_csv(INPUT_CSV)
    pivot_data = {}
    for _, row in df.iterrows():
        tool = TOOL_NAMES.get(row['tool'], row['tool'])
        category = CATEGORY_SHORT_NAMES.get(row['category'], row['category'])
        if tool not in pivot_data:
            pivot_data[tool] = {}
        pivot_data[tool][category] = row['detection_rate']
    return pd.DataFrame(pivot_data).T


def create_heatmap(df):
    tools_ordered = [t for t in TOOL_ORDER if t in df.index]
    cats_ordered = [c for c in CATEGORY_ORDER if c in df.columns]
    df = df.reindex(tools_ordered)[cats_ordered]

    fig, ax = plt.subplots(figsize=(15, 8), dpi=300)

    sns.heatmap(
        df, annot=True, fmt='.0%', cmap='RdYlGn',
        vmin=0, vmax=1, center=0.5,
        linewidths=0.5, linecolor='white',
        cbar_kws={'label': 'Detection Rate (%)', 'shrink': 0.7, 'aspect': 25, 'pad': 0.15},
        annot_kws={'size': 9, 'weight': 'medium'},
        ax=ax
    )

    ax.collections[0].colorbar.ax.tick_params(labelsize=9)
    ax.set_xlabel('Evasion Technique Category', fontsize=12, fontweight='medium', labelpad=10)
    ax.set_ylabel('Detection Tool', fontsize=12, fontweight='medium', labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    # Separator lines between tool categories
    for y in [4, 5, 12]:
        ax.axhline(y=y, color='black', linewidth=2)

    # Category labels on right side
    n_cols = len(cats_ordered)
    group_info = [((0+4)/2, 'Static-Based'), ((4+5)/2, 'Dynamic-Based'),
                  ((5+12)/2, 'ML-Based'), ((12+13)/2, 'LLM-Based')]
    for center, label in group_info:
        ax.text(n_cols + 0.3, center, label, ha='left', va='center',
                fontsize=11, fontweight='bold', fontstyle='italic', rotation=-90)

    plt.tight_layout()
    plt.subplots_adjust(right=0.88)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'evasion_detection_heatmap.{fmt}'
        fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")
    plt.close()


def main():
    print("Generating evasion detection heatmap...")
    df = load_data()
    create_heatmap(df)
    print("Done!")


if __name__ == "__main__":
    main()
