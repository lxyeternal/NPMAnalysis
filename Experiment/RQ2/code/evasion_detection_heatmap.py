#!/usr/bin/env python3
"""
RQ2: Publication-Quality Evasion Detection Heatmap
Generates a professional heatmap showing tool detection rates for evasion categories.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib as mpl
from pathlib import Path

# Configure matplotlib for publication quality
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_CSV = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "data" / "tool_detection_by_category_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "figures"

# Professional tool names
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
    'Packj-Static', 'Packj-Trace'                     # Hybrid
]

# Short category names for better display
CATEGORY_SHORT_NAMES = {
    'String_Obfuscation': 'String Obfusc.',
    'Encoding_Obfuscation': 'Encoding Obfusc.',
    'Silent_Error_Handling': 'Silent Error',
    'Hook_Abuse': 'Hook Abuse',
    'Code_Structure_Obfuscation': 'Code Struct.',
    'Stealth_Execution': 'Stealth Exec.',
    'Module_Abuse': 'Module Abuse',
    'Network_Communication_Hiding': 'Net. Hiding',
    'Environment_Detection': 'Env. Detection',
    'Anti_Analysis': 'Anti-Analysis',
    'Trace_Cleanup': 'Trace Cleanup',
    'Dependency_Confusion': 'Dep. Confusion',
    'Typosquatting': 'Typosquatting',
    'Runtime_Caching': 'Runtime Cache'
}

# Category order (by average detection difficulty - hardest first)
CATEGORY_ORDER = [
    'Anti-Analysis', 'Trace Cleanup', 'Env. Detection', 'Stealth Exec.',
    'String Obfusc.', 'Silent Error', 'Code Struct.', 'Net. Hiding',
    'Encoding Obfusc.', 'Hook Abuse', 'Module Abuse',
    'Typosquatting', 'Runtime Cache', 'Dep. Confusion'
]


def load_data():
    """Load and process detection rate data"""
    df = pd.read_csv(INPUT_CSV)

    # Create pivot table
    pivot_data = {}

    for _, row in df.iterrows():
        tool = TOOL_NAMES.get(row['tool'], row['tool'])
        category = CATEGORY_SHORT_NAMES.get(row['category'], row['category'])
        detection_rate = row['detection_rate']

        if tool not in pivot_data:
            pivot_data[tool] = {}
        pivot_data[tool][category] = detection_rate

    # Create DataFrame
    result_df = pd.DataFrame(pivot_data).T

    return result_df


def create_publication_heatmap(df):
    """Create publication-quality heatmap"""

    # Reorder tools and categories
    tools_ordered = [t for t in TOOL_ORDER if t in df.index]
    cats_ordered = [c for c in CATEGORY_ORDER if c in df.columns]

    df = df.reindex(tools_ordered)
    df = df[cats_ordered]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

    # Create custom colormap (more distinct colors)
    cmap = sns.diverging_palette(10, 133, s=80, l=55, as_cmap=True)

    # Create heatmap
    hm = sns.heatmap(
        df,
        annot=True,
        fmt='.2f',
        cmap='RdYlGn',
        vmin=0,
        vmax=1,
        center=0.5,
        linewidths=0.5,
        linecolor='white',
        cbar_kws={
            'label': 'Detection Rate',
            'shrink': 0.8,
            'aspect': 25
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
    cbar.set_label('Detection Rate', size=10, weight='medium')

    # Customize axes
    ax.set_xlabel('Evasion Technique Category', fontsize=11, fontweight='medium', labelpad=10)
    ax.set_ylabel('Detection Tool', fontsize=11, fontweight='medium', labelpad=10)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)

    # Add tool type separators (horizontal lines)
    ax.axhline(y=4, color='black', linewidth=1.5)  # After rule-based tools
    ax.axhline(y=7, color='black', linewidth=1.5)  # After ML-based tools

    # Tight layout
    plt.tight_layout()

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / 'evasion_detection_heatmap.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(OUTPUT_DIR / 'evasion_detection_heatmap.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {OUTPUT_DIR / 'evasion_detection_heatmap.png'}")
    print(f"Saved: {OUTPUT_DIR / 'evasion_detection_heatmap.pdf'}")

    plt.close()
    return fig


def create_simplified_heatmap(df):
    """Create a cleaner version without annotations for small print"""

    # Reorder tools and categories
    tools_ordered = [t for t in TOOL_ORDER if t in df.index]
    cats_ordered = [c for c in CATEGORY_ORDER if c in df.columns]

    df = df.reindex(tools_ordered)
    df = df[cats_ordered]

    # Create figure - smaller for paper
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    # Create heatmap without annotations
    hm = sns.heatmap(
        df,
        annot=False,
        cmap='RdYlGn',
        vmin=0,
        vmax=1,
        center=0.5,
        linewidths=0.3,
        linecolor='white',
        cbar_kws={
            'label': 'Detection Rate',
            'shrink': 0.8,
            'aspect': 20,
            'ticks': [0, 0.25, 0.5, 0.75, 1.0]
        },
        ax=ax
    )

    # Customize colorbar
    cbar = hm.collections[0].colorbar
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('Detection Rate', size=9, weight='medium')
    cbar.ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])

    # Customize axes
    ax.set_xlabel('Evasion Technique Category', fontsize=10, fontweight='medium', labelpad=8)
    ax.set_ylabel('Detection Tool', fontsize=10, fontweight='medium', labelpad=8)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)

    # Add tool type separators
    ax.axhline(y=4, color='black', linewidth=1.2)
    ax.axhline(y=7, color='black', linewidth=1.2)

    plt.tight_layout()

    # Save
    fig.savefig(OUTPUT_DIR / 'evasion_detection_heatmap_clean.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(OUTPUT_DIR / 'evasion_detection_heatmap_clean.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {OUTPUT_DIR / 'evasion_detection_heatmap_clean.png'}")
    print(f"Saved: {OUTPUT_DIR / 'evasion_detection_heatmap_clean.pdf'}")

    plt.close()
    return fig


def main():
    print("Loading data...")
    df = load_data()

    print(f"Loaded data for {len(df)} tools and {len(df.columns)} categories")

    print("\nGenerating publication-quality heatmaps...")

    print("\n1. Creating annotated heatmap...")
    create_publication_heatmap(df)

    print("\n2. Creating clean heatmap (no annotations)...")
    create_simplified_heatmap(df)

    print("\n" + "="*60)
    print("All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
