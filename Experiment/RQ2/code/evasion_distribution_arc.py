#!/usr/bin/env python3
"""
RQ2: Distribution of Evasion Techniques Arc Diagram
Generates evasion_distribution_arc.png/pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from pathlib import Path as FilePath

SCRIPT_DIR = FilePath(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "data" / "category_distribution_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "figures"

SHORT_NAMES = {
    'String_Obfuscation': 'String\nObfusc.',
    'Encoding_Obfuscation': 'Encoding\nObfusc.',
    'Silent_Error_Handling': 'Silent\nError',
    'Hook_Abuse': 'Hook\nAbuse',
    'Code_Structure_Obfuscation': 'Code\nStruct.',
    'Stealth_Execution': 'Stealth\nExec.',
    'Module_Abuse': 'Module\nAbuse',
    'Network_Communication_Hiding': 'Network\nHiding',
    'Environment_Detection': 'Env.\nDetect.',
    'Anti_Analysis': 'Anti-\nAnalysis',
    'Trace_Cleanup': 'Trace\nCleanup',
    'Dependency_Confusion': 'Dep.\nConfusion',
    'Typosquatting': 'Typo-\nsquatting',
    'Runtime_Caching': 'Runtime\nCache'
}


def create_distribution_arc():
    df = pd.read_csv(DATA_PATH)
    df = df.sort_values('count', ascending=False)

    total = df['count'].sum()
    df['pct'] = df['count'] / total * 100

    fig, ax = plt.subplots(figsize=(14, 11))

    n_cats = len(df)
    angles = np.linspace(np.pi, 0, n_cats)
    radius = 4

    positions = {}
    for i, (_, row) in enumerate(df.iterrows()):
        cat = row['category']
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        positions[cat] = (x, y, angles[i])

    colors = plt.cm.Set3(np.linspace(0, 1, n_cats))
    cat_colors = {row['category']: colors[i] for i, (_, row) in enumerate(df.iterrows())}

    max_count = df['count'].max()
    min_count = df['count'].min()

    origin_x, origin_y = 0, 0.5

    for i, (_, row) in enumerate(df.iterrows()):
        cat = row['category']
        count = row['count']
        x, y, angle = positions[cat]

        mid_angle = (np.arctan2(y - origin_y, x - origin_x) + angle) / 2
        dist = np.sqrt((x - origin_x)**2 + (y - origin_y)**2)
        ctrl_radius = dist * 0.4
        ctrl_x = origin_x + ctrl_radius * np.cos(mid_angle)
        ctrl_y = origin_y + ctrl_radius * np.sin(mid_angle)

        norm_count = (count - min_count) / (max_count - min_count) if max_count > min_count else 0.5
        linewidth = 2 + norm_count * 12
        alpha = 0.4 + norm_count * 0.45

        verts = [(origin_x, origin_y), (ctrl_x, ctrl_y), (x, y)]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)

        patch = mpatches.PathPatch(path, facecolor='none', edgecolor=cat_colors[cat],
                                   linewidth=linewidth, alpha=alpha, capstyle='round')
        ax.add_patch(patch)

    node_size = 900
    for i, (_, row) in enumerate(df.iterrows()):
        cat = row['category']
        x, y, angle = positions[cat]
        ax.scatter(x, y, s=node_size, c=[cat_colors[cat]], edgecolors='white',
                   linewidths=2.5, zorder=10)

        label_radius = radius * 1.18
        label_x = label_radius * np.cos(angle)
        label_y = label_radius * np.sin(angle)

        ha = 'center'
        if angle > np.pi * 0.6:
            ha = 'right'
        elif angle < np.pi * 0.4:
            ha = 'left'

        ax.text(label_x, label_y, SHORT_NAMES.get(cat, cat),
                ha=ha, va='center', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=cat_colors[cat], alpha=0.95, linewidth=1.5))

    label_offsets = [
        (0.3, -0.4), (-0.4, 0.3), (0.4, 0.25), (0.0, 0.3), (0.0, -0.25)
    ]

    for i, (_, row) in enumerate(df.head(5).iterrows()):
        cat = row['category']
        pct = row['pct']
        x, y, angle = positions[cat]

        t = 0.55
        mid_x = (1-t)**2 * origin_x + 2*(1-t)*t * (origin_x + (x - origin_x) * 0.4) + t**2 * x
        mid_y = (1-t)**2 * origin_y + 2*(1-t)*t * (origin_y + (y - origin_y) * 0.4) + t**2 * y

        offset_x, offset_y = label_offsets[i]
        ax.annotate(f"{pct:.1f}%",
                    xy=(mid_x + offset_x, mid_y + offset_y),
                    fontsize=12, fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                              edgecolor=cat_colors[cat], alpha=0.95, linewidth=2),
                    zorder=15)

    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-1, 5.8)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'evasion_distribution_arc.{fmt}'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")

    plt.close()


def main():
    print("RQ2: Evasion Distribution Arc Diagram")
    print("=" * 60)
    create_distribution_arc()
    print("Done!")


if __name__ == "__main__":
    main()
