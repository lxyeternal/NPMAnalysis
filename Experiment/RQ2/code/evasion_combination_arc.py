#!/usr/bin/env python3
"""
RQ2: Evasion Technique Combination Arc Diagram
Generates evasion_combination_arc.png/pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from pathlib import Path as FilePath

SCRIPT_DIR = FilePath(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "data" / "two_evade_combinations_analysis.csv"
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


def create_arc_diagram():
    df = pd.read_csv(DATA_PATH)

    categories = set()
    for _, row in df.iterrows():
        categories.add(row['Category1'])
        categories.add(row['Category2'])

    category_totals = {}
    for cat in categories:
        total = df[(df['Category1'] == cat) | (df['Category2'] == cat)]['Count'].sum()
        category_totals[cat] = total

    sorted_categories = sorted(categories, key=lambda x: category_totals[x], reverse=True)

    fig, ax = plt.subplots(figsize=(14, 11))

    n_cats = len(sorted_categories)
    angles = np.linspace(np.pi, 0, n_cats)
    radius = 4

    positions = {}
    for i, cat in enumerate(sorted_categories):
        x = radius * np.cos(angles[i])
        y = radius * np.sin(angles[i])
        positions[cat] = (x, y, angles[i])

    colors = plt.cm.Set3(np.linspace(0, 1, n_cats))
    cat_colors = {cat: colors[i] for i, cat in enumerate(sorted_categories)}

    max_count = df['Count'].max()
    min_count = df['Count'].min()
    arc_info = []

    for _, row in df.iterrows():
        cat1, cat2, count, pct = row['Category1'], row['Category2'], row['Count'], row['Percentage']
        if cat1 not in positions or cat2 not in positions:
            continue

        x1, y1, a1 = positions[cat1]
        x2, y2, a2 = positions[cat2]

        mid_angle = (a1 + a2) / 2
        ctrl_radius = radius * 0.3 * (1 - abs(a1 - a2) / np.pi)
        ctrl_x = ctrl_radius * np.cos(mid_angle)
        ctrl_y = ctrl_radius * np.sin(mid_angle)

        linewidth = 1.5 + (count - min_count) / (max_count - min_count) * 14
        alpha = 0.35 + (count - min_count) / (max_count - min_count) * 0.5

        verts = [(x1, y1), (ctrl_x, ctrl_y), (x2, y2)]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)

        color1 = np.array(cat_colors[cat1][:3])
        color2 = np.array(cat_colors[cat2][:3])
        mixed_color = (color1 + color2) / 2

        patch = mpatches.PathPatch(path, facecolor='none', edgecolor=mixed_color,
                                   linewidth=linewidth, alpha=alpha, capstyle='round')
        ax.add_patch(patch)

        t = 0.5
        label_x = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
        label_y = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2

        arc_info.append({
            'count': count, 'pct': pct, 'label_x': label_x, 'label_y': label_y,
            'color': mixed_color, 'linewidth': linewidth
        })

    arc_info_sorted = sorted(arc_info, key=lambda x: x['count'], reverse=True)
    label_offsets = [(0, -0.3), (-0.5, 0.3), (0.5, 0.3), (0, 0.2), (0, -0.15)]

    for i, info in enumerate(arc_info_sorted[:5]):
        offset_x, offset_y = label_offsets[i]
        ax.annotate(f"{info['pct']:.1f}%",
                    xy=(info['label_x'] + offset_x, info['label_y'] + offset_y),
                    fontsize=12, fontweight='bold', ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                              edgecolor=info['color'], alpha=0.95, linewidth=2),
                    zorder=15)

    node_size = 900
    for cat in sorted_categories:
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

    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-1, 5.8)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for fmt in ['png', 'pdf']:
        output_file = OUTPUT_DIR / f'evasion_combination_arc.{fmt}'
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved: {output_file}")

    plt.close()


def main():
    print("RQ2: Evasion Combination Arc Diagram")
    print("=" * 60)
    create_arc_diagram()
    print("Done!")


if __name__ == "__main__":
    main()
