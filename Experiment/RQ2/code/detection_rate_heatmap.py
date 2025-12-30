#!/usr/bin/env python3
"""
RQ2: Detection Rate Heatmap
Generates detection_rate_heatmap.png/pdf
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from pathlib import Path

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 11
mpl.rcParams['pdf.fonttype'] = 42

SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_CSV = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "data" / "combined_malware_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "figures"

TOOL_NAMES = {
    'genie': 'GENIE', 'guarddog': 'GuardDog', 'ossgadget': 'OSSGadget',
    'packj_static': 'Packj-Static', 'packj_trace': 'Packj-Trace',
    'sap_DT': 'SAP-DT', 'sap_RF': 'SAP-RF', 'sap_XGB': 'SAP-XGB',
    'socketai': 'SocketAI'
}

TOOL_ORDER = [
    'GENIE', 'GuardDog', 'OSSGadget', 'SocketAI',
    'SAP-DT', 'SAP-RF', 'SAP-XGB',
    'Packj-Static', 'Packj-Trace'
]

BEHAVIOR_SHORT_NAMES = {
    'Anti-Analysis': 'Anti-Analysis', 'Browser Manipulation': 'Browser Manip.',
    'Command Execution': 'Cmd Execution', 'Credential Theft': 'Credential Theft',
    'DDoS Capabilities': 'DDoS', 'Data Exfiltration': 'Data Exfil.',
    'File Operations': 'File Ops', 'Malicious Payload Delivery': 'Payload Delivery',
    'Network Communication': 'Network Comm.', 'Obfuscation Techniques': 'Obfuscation',
    'Persistence Mechanisms': 'Persistence', 'Privilege Escalation': 'Privilege Esc.',
    'Prototype Pollution': 'Proto. Pollution', 'Proxy Manipulation': 'Proxy Manip.',
    'System Reconnaissance': 'Sys Recon.'
}


def load_data(csv_file):
    df = pd.read_csv(csv_file)
    detection_rates = []

    for tool in df['tool'].unique():
        tool_data = df[df['tool'] == tool]
        for classification in tool_data['classification'].unique():
            class_data = tool_data[tool_data['classification'] == classification]
            fn_count = class_data[class_data['category'] == 'false_negatives']['count'].values
            mr_count = class_data[class_data['category'] == 'malicious_reports']['count'].values

            if len(fn_count) > 0 and len(mr_count) > 0:
                fn, mr = fn_count[0], mr_count[0]
                total = fn + mr
                detection_rate = (mr / total) * 100 if total > 0 else 0
                detection_rates.append({
                    'Tool': TOOL_NAMES.get(tool, tool),
                    'Behavior': classification,
                    'Detection Rate': detection_rate
                })

    return pd.DataFrame(detection_rates)


def create_heatmap(df):
    pivot_df = df.pivot(index='Tool', columns='Behavior', values='Detection Rate')
    pivot_df = pivot_df.reindex([t for t in TOOL_ORDER if t in pivot_df.index])

    behavior_order = pivot_df.mean().sort_values().index.tolist()
    pivot_df = pivot_df[behavior_order]
    pivot_df.columns = [BEHAVIOR_SHORT_NAMES.get(col, col) for col in pivot_df.columns]

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    sns.heatmap(
        pivot_df, annot=True, fmt='.0f', cmap='RdYlGn',
        vmin=0, vmax=100, center=50,
        linewidths=0.5, linecolor='white',
        cbar_kws={'label': 'Detection Rate (%)', 'shrink': 0.8, 'aspect': 20},
        annot_kws={'size': 8, 'weight': 'medium'},
        ax=ax
    )

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=9)
    cbar.set_label('Detection Rate (%)', size=10, weight='medium')

    ax.set_xlabel('Malicious Behavior Type', fontsize=11, fontweight='medium', labelpad=10)
    ax.set_ylabel('Detection Tool', fontsize=11, fontweight='medium', labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)

    ax.axhline(y=4, color='black', linewidth=1.5)
    ax.axhline(y=7, color='black', linewidth=1.5)

    n_cols = len(pivot_df.columns)
    ax.text(n_cols + 0.5, 2, 'Rule-based', fontsize=8, va='center', ha='left', style='italic', rotation=-90)
    ax.text(n_cols + 0.5, 5.5, 'ML-based', fontsize=8, va='center', ha='left', style='italic', rotation=-90)
    ax.text(n_cols + 0.5, 8, 'Hybrid', fontsize=8, va='center', ha='left', style='italic', rotation=-90)

    plt.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'detection_rate_heatmap.{fmt}'
        fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")

    plt.close()


def main():
    print("RQ2: Detection Rate Heatmap")
    print("=" * 60)
    df = load_data(INPUT_CSV)
    create_heatmap(df)
    print("Done!")


if __name__ == "__main__":
    main()
