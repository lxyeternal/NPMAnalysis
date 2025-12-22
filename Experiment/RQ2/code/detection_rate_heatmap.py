#!/usr/bin/env python3
"""
RQ2: Publication-Quality Heatmap for Malware Detection Rates
Generates a professional heatmap showing detection rates across tools and malware behaviors.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import matplotlib as mpl

# Configure matplotlib for publication quality
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['pdf.fonttype'] = 42  # TrueType fonts for PDF
mpl.rcParams['ps.fonttype'] = 42

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_CSV = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "data" / "combined_malware_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "figures"

# Tool display names (professional names for papers)
TOOL_NAMES = {
    'genie': 'GENIE',
    'guarddog': 'GuardDog',
    'ossgadget': 'OSSGadget',
    'packj_static': 'Packj-Static',
    'packj_trace': 'Packj-Trace',
    'sap_DT': 'SAP-DT',
    'sap_RF': 'SAP-RF',
    'sap_XGB': 'SAP-XGB',
    'socketai': 'SocketAI'
}

# Tool order (grouped by type)
TOOL_ORDER = [
    'GENIE', 'GuardDog', 'OSSGadget', 'SocketAI',  # Rule-based
    'SAP-DT', 'SAP-RF', 'SAP-XGB',                    # ML-based
    'Packj-Static', 'Packj-Trace'                     # Packj
]

# Behavior short names for better display
BEHAVIOR_SHORT_NAMES = {
    'Anti-Analysis': 'Anti-Analysis',
    'Browser Manipulation': 'Browser Manip.',
    'Command Execution': 'Cmd Execution',
    'Credential Theft': 'Credential Theft',
    'DDoS Capabilities': 'DDoS',
    'Data Exfiltration': 'Data Exfil.',
    'File Operations': 'File Ops',
    'Malicious Payload Delivery': 'Payload Delivery',
    'Network Communication': 'Network Comm.',
    'Obfuscation Techniques': 'Obfuscation',
    'Persistence Mechanisms': 'Persistence',
    'Privilege Escalation': 'Privilege Esc.',
    'Prototype Pollution': 'Proto. Pollution',
    'Proxy Manipulation': 'Proxy Manip.',
    'System Reconnaissance': 'Sys Recon.'
}


def load_and_process_data(csv_file):
    """Load and process the malware analysis data into a pivot table"""
    df = pd.read_csv(csv_file)

    detection_rates = []

    for tool in df['tool'].unique():
        tool_data = df[df['tool'] == tool]

        for classification in tool_data['classification'].unique():
            class_data = tool_data[tool_data['classification'] == classification]

            fn_count = class_data[class_data['category'] == 'false_negatives']['count'].values
            mr_count = class_data[class_data['category'] == 'malicious_reports']['count'].values

            if len(fn_count) > 0 and len(mr_count) > 0:
                fn = fn_count[0]
                mr = mr_count[0]
                total = fn + mr
                detection_rate = (mr / total) * 100 if total > 0 else 0

                # Map tool name to display name
                tool_display = TOOL_NAMES.get(tool, tool)

                detection_rates.append({
                    'Tool': tool_display,
                    'Behavior': classification,
                    'Detection Rate': detection_rate
                })

    return pd.DataFrame(detection_rates)


def create_heatmap(df, output_dir):
    """Create publication-quality heatmap"""

    # Create pivot table
    pivot_df = df.pivot(index='Tool', columns='Behavior', values='Detection Rate')

    # Reorder tools
    pivot_df = pivot_df.reindex([t for t in TOOL_ORDER if t in pivot_df.index])

    # Sort behaviors by average detection rate (hardest to easiest, left to right)
    behavior_order = pivot_df.mean().sort_values().index.tolist()
    pivot_df = pivot_df[behavior_order]

    # Rename behaviors to short names
    pivot_df.columns = [BEHAVIOR_SHORT_NAMES.get(col, col) for col in pivot_df.columns]

    # Create figure - adjusted size for single column in paper
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    # Create heatmap with custom colormap
    # RdYlGn: Red (low) -> Yellow (medium) -> Green (high)
    cmap = sns.color_palette("RdYlGn", as_cmap=True)

    # Plot heatmap
    hm = sns.heatmap(
        pivot_df,
        annot=True,
        fmt='.0f',
        cmap=cmap,
        vmin=0,
        vmax=100,
        center=50,
        linewidths=0.5,
        linecolor='white',
        cbar_kws={
            'label': 'Detection Rate (%)',
            'shrink': 0.8,
            'aspect': 20
        },
        annot_kws={
            'size': 8,
            'weight': 'medium'
        },
        ax=ax
    )

    # Customize colorbar
    cbar = hm.collections[0].colorbar
    cbar.ax.tick_params(labelsize=9)
    cbar.set_label('Detection Rate (%)', size=10, weight='medium')

    # Customize axes
    ax.set_xlabel('Malicious Behavior Type', fontsize=11, fontweight='medium', labelpad=10)
    ax.set_ylabel('Detection Tool', fontsize=11, fontweight='medium', labelpad=10)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)

    # Add tool type separators (horizontal lines)
    ax.axhline(y=4, color='black', linewidth=1.5)  # After rule-based tools
    ax.axhline(y=7, color='black', linewidth=1.5)  # After ML-based tools

    # Add tool type labels on the right side
    ax.text(len(pivot_df.columns) + 0.5, 2, 'Rule-based',
            fontsize=8, va='center', ha='left', style='italic', rotation=-90)
    ax.text(len(pivot_df.columns) + 0.5, 5.5, 'ML-based',
            fontsize=8, va='center', ha='left', style='italic', rotation=-90)
    ax.text(len(pivot_df.columns) + 0.5, 8, 'Hybrid',
            fontsize=8, va='center', ha='left', style='italic', rotation=-90)

    # Tight layout
    plt.tight_layout()

    # Save figures
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save in multiple formats
    fig.savefig(output_dir / 'detection_rate_heatmap.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(output_dir / 'detection_rate_heatmap.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {output_dir / 'detection_rate_heatmap.png'}")
    print(f"Saved: {output_dir / 'detection_rate_heatmap.pdf'}")

    return fig


def create_grouped_bar_chart(df, output_dir):
    """Create an alternative grouped bar chart visualization"""

    # Calculate average detection rate per tool
    tool_avg = df.groupby('Tool')['Detection Rate'].mean().sort_values(ascending=True)

    # Reorder tools for display
    tools_ordered = [t for t in reversed(TOOL_ORDER) if t in tool_avg.index]
    tool_avg = tool_avg.reindex(tools_ordered)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 4), dpi=300)

    # Color bars by performance
    colors = []
    for rate in tool_avg.values:
        if rate >= 80:
            colors.append('#2E7D32')  # Green - high
        elif rate >= 60:
            colors.append('#FFA000')  # Orange - medium
        else:
            colors.append('#C62828')  # Red - low

    # Create horizontal bar chart
    bars = ax.barh(range(len(tool_avg)), tool_avg.values, color=colors, edgecolor='black', linewidth=0.5)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, tool_avg.values)):
        ax.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=9)

    # Customize axes
    ax.set_yticks(range(len(tool_avg)))
    ax.set_yticklabels(tool_avg.index, fontsize=10)
    ax.set_xlabel('Average Detection Rate (%)', fontsize=11, fontweight='medium')
    ax.set_xlim(0, 105)

    # Add grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save
    fig.savefig(output_dir / 'tool_average_detection_rate.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(output_dir / 'tool_average_detection_rate.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {output_dir / 'tool_average_detection_rate.png'}")
    print(f"Saved: {output_dir / 'tool_average_detection_rate.pdf'}")

    return fig


def create_behavior_difficulty_chart(df, output_dir):
    """Create a chart showing behavior detection difficulty"""

    # Calculate average detection rate per behavior
    behavior_avg = df.groupby('Behavior')['Detection Rate'].mean().sort_values(ascending=True)

    # Apply short names
    behavior_avg.index = [BEHAVIOR_SHORT_NAMES.get(b, b) for b in behavior_avg.index]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

    # Color bars by difficulty
    colors = []
    for rate in behavior_avg.values:
        if rate >= 70:
            colors.append('#2E7D32')  # Green - easy to detect
        elif rate >= 55:
            colors.append('#FFA000')  # Orange - medium
        else:
            colors.append('#C62828')  # Red - hard to detect

    # Create horizontal bar chart
    bars = ax.barh(range(len(behavior_avg)), behavior_avg.values, color=colors,
                   edgecolor='black', linewidth=0.5)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, behavior_avg.values)):
        ax.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=9)

    # Customize axes
    ax.set_yticks(range(len(behavior_avg)))
    ax.set_yticklabels(behavior_avg.index, fontsize=10)
    ax.set_xlabel('Average Detection Rate (%)', fontsize=11, fontweight='medium')
    ax.set_xlim(0, 95)

    # Add difficulty labels
    ax.axvline(x=55, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=70, color='gray', linestyle='--', alpha=0.5)
    ax.text(45, len(behavior_avg) - 0.5, 'Hard', fontsize=8, color='#C62828', style='italic')
    ax.text(60, len(behavior_avg) - 0.5, 'Medium', fontsize=8, color='#FFA000', style='italic')
    ax.text(78, len(behavior_avg) - 0.5, 'Easy', fontsize=8, color='#2E7D32', style='italic')

    # Add grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save
    fig.savefig(output_dir / 'behavior_detection_difficulty.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(output_dir / 'behavior_detection_difficulty.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {output_dir / 'behavior_detection_difficulty.png'}")
    print(f"Saved: {output_dir / 'behavior_detection_difficulty.pdf'}")

    return fig


def main():
    print("Loading data...")
    df = load_and_process_data(INPUT_CSV)

    print("\nGenerating publication-quality figures...")

    # Create all visualizations
    print("\n1. Creating detection rate heatmap...")
    create_heatmap(df, OUTPUT_DIR)

    print("\n2. Creating tool performance comparison...")
    create_grouped_bar_chart(df, OUTPUT_DIR)

    print("\n3. Creating behavior difficulty chart...")
    create_behavior_difficulty_chart(df, OUTPUT_DIR)

    print("\n" + "="*60)
    print("All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
