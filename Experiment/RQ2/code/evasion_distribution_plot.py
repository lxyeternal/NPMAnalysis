#!/usr/bin/env python3
"""
RQ2: Publication-Quality Evasion Technique Distribution Plot
Generates a professional horizontal bar chart showing evasion technique distribution.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from pathlib import Path

# Configure matplotlib for publication quality
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "evasion_analysis" / "figures"

# Evasion technique data (from category_statistics.txt)
EVASION_DATA = {
    'String_Obfuscation': 541,
    'Encoding_Obfuscation': 374,
    'Silent_Error_Handling': 366,
    'Hook_Abuse': 352,
    'Code_Structure_Obfuscation': 325,
    'Stealth_Execution': 263,
    'Module_Abuse': 175,
    'Network_Communication_Hiding': 144,
    'Environment_Detection': 117,
    'Anti_Analysis': 54,
    'Trace_Cleanup': 30,
    'Dependency_Confusion': 6,
    'Typosquatting': 4,
    'Runtime_Caching': 4
}

# Clean display names (remove underscores, more readable)
DISPLAY_NAMES = {
    'String_Obfuscation': 'String Obfuscation',
    'Encoding_Obfuscation': 'Encoding Obfuscation',
    'Silent_Error_Handling': 'Silent Error Handling',
    'Hook_Abuse': 'Hook Abuse',
    'Code_Structure_Obfuscation': 'Code Structure Obfusc.',
    'Stealth_Execution': 'Stealth Execution',
    'Module_Abuse': 'Module Abuse',
    'Network_Communication_Hiding': 'Network Comm. Hiding',
    'Environment_Detection': 'Environment Detection',
    'Anti_Analysis': 'Anti-Analysis',
    'Trace_Cleanup': 'Trace Cleanup',
    'Dependency_Confusion': 'Dependency Confusion',
    'Typosquatting': 'Typosquatting',
    'Runtime_Caching': 'Runtime Caching'
}


def create_horizontal_bar_chart():
    """Create a publication-quality horizontal bar chart"""

    # Prepare data
    techniques = list(EVASION_DATA.keys())
    counts = list(EVASION_DATA.values())
    total = sum(counts)
    percentages = [c / total * 100 for c in counts]

    # Sort by count (ascending for horizontal bar - highest at top)
    sorted_data = sorted(zip(techniques, counts, percentages), key=lambda x: x[1])
    techniques, counts, percentages = zip(*sorted_data)

    # Get display names
    display_names = [DISPLAY_NAMES[t] for t in techniques]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    # Create color gradient (darker blue for higher values)
    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(counts)))

    # Create horizontal bars
    y_pos = np.arange(len(display_names))
    bars = ax.barh(y_pos, counts, color=colors, edgecolor='#2c3e50', linewidth=0.5, height=0.7)

    # Add value labels (count and percentage)
    for i, (bar, count, pct) in enumerate(zip(bars, counts, percentages)):
        # Position label inside or outside bar based on bar length
        if count > 100:
            # Inside the bar (white text)
            ax.text(count - 5, bar.get_y() + bar.get_height()/2,
                   f'{count}',
                   ha='right', va='center', fontsize=9, fontweight='medium', color='white')
        else:
            # Outside the bar (dark text)
            ax.text(count + 8, bar.get_y() + bar.get_height()/2,
                   f'{count} ({pct:.1f}%)',
                   ha='left', va='center', fontsize=8, color='#2c3e50')

    # Customize axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(display_names, fontsize=10)
    ax.set_xlabel('Number of Packages', fontsize=11, fontweight='medium')
    ax.set_xlim(0, max(counts) * 1.15)

    # Add subtle grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    # Tight layout
    plt.tight_layout()

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / 'evasion_distribution_horizontal.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(OUTPUT_DIR / 'evasion_distribution_horizontal.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {OUTPUT_DIR / 'evasion_distribution_horizontal.png'}")
    print(f"Saved: {OUTPUT_DIR / 'evasion_distribution_horizontal.pdf'}")

    plt.close()
    return fig


def create_lollipop_chart():
    """Create a lollipop chart (dot + line) - elegant alternative"""

    # Prepare data
    techniques = list(EVASION_DATA.keys())
    counts = list(EVASION_DATA.values())
    total = sum(counts)
    percentages = [c / total * 100 for c in counts]

    # Sort by count (ascending - highest at top)
    sorted_data = sorted(zip(techniques, counts, percentages), key=lambda x: x[1])
    techniques, counts, percentages = zip(*sorted_data)

    # Get display names
    display_names = [DISPLAY_NAMES[t] for t in techniques]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    y_pos = np.arange(len(display_names))

    # Create color based on count
    norm_counts = np.array(counts) / max(counts)
    colors = plt.cm.RdYlGn(norm_counts)  # Red (low) to Green (high)

    # Draw lines (stems)
    for i, (y, count) in enumerate(zip(y_pos, counts)):
        ax.hlines(y=y, xmin=0, xmax=count, color='#bdc3c7', linewidth=1.5, zorder=1)

    # Draw dots
    scatter = ax.scatter(counts, y_pos, c=colors, s=80, zorder=2, edgecolors='#2c3e50', linewidth=0.5)

    # Add value labels
    for i, (count, pct) in enumerate(zip(counts, percentages)):
        ax.text(count + 15, i, f'{count}', ha='left', va='center', fontsize=9, fontweight='medium')

    # Customize axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(display_names, fontsize=10)
    ax.set_xlabel('Number of Packages', fontsize=11, fontweight='medium')
    ax.set_xlim(0, max(counts) * 1.15)

    # Add subtle grid
    ax.xaxis.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.set_axisbelow(True)

    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_linewidth(0.5)

    # Tight layout
    plt.tight_layout()

    # Save
    fig.savefig(OUTPUT_DIR / 'evasion_distribution_lollipop.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(OUTPUT_DIR / 'evasion_distribution_lollipop.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {OUTPUT_DIR / 'evasion_distribution_lollipop.png'}")
    print(f"Saved: {OUTPUT_DIR / 'evasion_distribution_lollipop.pdf'}")

    plt.close()
    return fig


def create_grouped_category_chart():
    """Create a grouped chart by evasion category type"""

    # Group evasion techniques by category
    categories = {
        'Obfuscation': ['String_Obfuscation', 'Encoding_Obfuscation', 'Code_Structure_Obfuscation'],
        'Execution Hiding': ['Silent_Error_Handling', 'Stealth_Execution', 'Hook_Abuse'],
        'Anti-Detection': ['Anti_Analysis', 'Environment_Detection', 'Trace_Cleanup'],
        'Module/Network': ['Module_Abuse', 'Network_Communication_Hiding', 'Runtime_Caching'],
        'Supply Chain': ['Dependency_Confusion', 'Typosquatting']
    }

    # Calculate totals per category
    category_totals = {}
    for cat, techniques in categories.items():
        category_totals[cat] = sum(EVASION_DATA.get(t, 0) for t in techniques)

    # Sort by total
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    # Create figure
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

    # Colors for each category
    cat_colors = {
        'Obfuscation': '#3498db',
        'Execution Hiding': '#e74c3c',
        'Anti-Detection': '#9b59b6',
        'Module/Network': '#2ecc71',
        'Supply Chain': '#f39c12'
    }

    x_offset = 0
    x_ticks = []
    x_labels = []

    for cat, total in sorted_cats:
        techniques = categories[cat]
        technique_counts = [(t, EVASION_DATA.get(t, 0)) for t in techniques]
        technique_counts = sorted(technique_counts, key=lambda x: x[1], reverse=True)

        for i, (tech, count) in enumerate(technique_counts):
            bar = ax.bar(x_offset, count, width=0.8, color=cat_colors[cat],
                        edgecolor='white', linewidth=0.5, alpha=0.85)

            # Add count label on top
            if count > 20:
                ax.text(x_offset, count + 10, str(count), ha='center', va='bottom',
                       fontsize=8, fontweight='medium')

            x_ticks.append(x_offset)
            # Shortened technique name
            short_name = DISPLAY_NAMES[tech].replace(' Obfuscation', '').replace(' Obfusc.', '')
            short_name = short_name.replace('Network Comm. Hiding', 'Net. Hiding')
            x_labels.append(short_name)
            x_offset += 1

        # Add separator between categories
        x_offset += 0.5

    # Customize axes
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Number of Packages', fontsize=11, fontweight='medium')
    ax.set_ylim(0, max(EVASION_DATA.values()) * 1.15)

    # Add legend
    legend_patches = [mpl.patches.Patch(color=cat_colors[cat], label=cat)
                     for cat, _ in sorted_cats]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9, frameon=True,
             fancybox=False, edgecolor='gray')

    # Grid and spines
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save
    fig.savefig(OUTPUT_DIR / 'evasion_distribution_grouped.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    fig.savefig(OUTPUT_DIR / 'evasion_distribution_grouped.pdf', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')

    print(f"Saved: {OUTPUT_DIR / 'evasion_distribution_grouped.png'}")
    print(f"Saved: {OUTPUT_DIR / 'evasion_distribution_grouped.pdf'}")

    plt.close()
    return fig


def main():
    print("Generating publication-quality evasion distribution plots...\n")

    print("1. Creating horizontal bar chart...")
    create_horizontal_bar_chart()

    print("\n2. Creating lollipop chart...")
    create_lollipop_chart()

    print("\n3. Creating grouped category chart...")
    create_grouped_category_chart()

    print("\n" + "="*60)
    print("All figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
