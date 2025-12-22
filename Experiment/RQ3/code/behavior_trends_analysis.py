#!/usr/bin/env python3
"""
RQ3: Malicious Behavior Trends Analysis
Analyzes the evolution of malicious behaviors in NPM packages over time.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import ast
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent  # Experiment/RQ3/code -> NPMAnalysis

# Input paths
CLASSIFICATIONS_FILE = PROJECT_ROOT / "Core" / "Analysis" / "behavior" / "key_results" / "package_all_classifications.csv"
TIME_FILE = PROJECT_ROOT / "Core" / "Data" / "timecollect" / "time" / "malware_time.csv"

# Output paths
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "behavior_trends"


def load_and_process_data():
    """Load and merge the classification and time data"""

    print("Loading classification data...")
    classifications_df = pd.read_csv(CLASSIFICATIONS_FILE)

    print("Loading time data...")
    time_df = pd.read_csv(TIME_FILE)

    # Clean and merge data
    print("Merging datasets...")
    merged_df = pd.merge(classifications_df, time_df, on=['package_name', 'version'], how='inner')

    # Filter out rows with empty timestamps
    merged_df = merged_df[merged_df['timestamp'].notna() & (merged_df['timestamp'] != '')]

    print(f"Total packages with both classification and time data: {len(merged_df)}")

    return merged_df


def extract_behaviors(merged_df):
    """Extract and process behavior classifications"""

    print("Processing behavior classifications...")

    behaviors_data = []

    for idx, row in merged_df.iterrows():
        try:
            timestamp = pd.to_datetime(row['timestamp'])

            # Parse the classifications
            classifications_str = row['classifications'].strip('"')
            classifications = ast.literal_eval(classifications_str)

            # Group years
            if timestamp.year <= 2020:
                year_label = "2011-2020"
            elif timestamp.year >= 2024:
                year_label = "2024-2025"
            else:
                year_label = str(timestamp.year)

            for behavior in classifications:
                behaviors_data.append({
                    'package_name': row['package_name'],
                    'version': row['version'],
                    'timestamp': timestamp,
                    'behavior': behavior.strip(),
                    'year': year_label
                })

        except Exception as e:
            continue

    behaviors_df = pd.DataFrame(behaviors_data)
    print(f"Total behavior instances extracted: {len(behaviors_df)}")

    return behaviors_df


def create_behavior_trends_plot(behaviors_df, output_dir):
    """Create publication-quality line plot showing behavior trends over time"""

    # Publication-quality settings
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
    mpl.rcParams['font.size'] = 11
    mpl.rcParams['axes.linewidth'] = 0.8
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    print("Creating behavior trends visualization...")

    def sort_key(x):
        if x == "2011-2020":
            return 2019
        elif x == "2024-2025":
            return 2024.5
        else:
            return int(x)

    # Get all behaviors
    behavior_counts = behaviors_df['behavior'].value_counts()
    all_behaviors = behavior_counts.index.tolist()

    # Analyze trends by year
    yearly_trends = behaviors_df.groupby(['year', 'behavior']).size().unstack(fill_value=0)
    plot_data = yearly_trends[all_behaviors]

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8), dpi=300)

    # Professional colors
    colors = ['#1E88E5', '#D81B60', '#FFC107', '#004D40', '#7B1FA2',
              '#FF5722', '#00ACC1', '#5D4037', '#43A047', '#6D4C41',
              '#F06292', '#4DD0E1', '#AED581', '#FFB74D', '#BA68C8']
    line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--',
                   '-.', ':', '-', '--', '-.']
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '*',
               'X', 'P', '+', 'x', '|']

    years_sorted = sorted(plot_data.index, key=sort_key)

    for i, behavior in enumerate(all_behaviors):
        if behavior in plot_data.columns:
            y_values = [plot_data.loc[year, behavior] for year in years_sorted]

            ax.plot(range(len(years_sorted)), y_values,
                    color=colors[i % len(colors)],
                    linestyle=line_styles[i % len(line_styles)],
                    marker=markers[i % len(markers)],
                    markersize=8,
                    linewidth=2.2,
                    markeredgewidth=1.5,
                    markeredgecolor='white',
                    label=behavior,
                    alpha=0.9)

    ax.set_ylabel('Number of Packages', fontsize=13, fontweight='medium', labelpad=10)
    ax.set_xlabel('Time Period', fontsize=13, fontweight='medium', labelpad=10)

    ax.grid(True, linestyle='--', alpha=0.4, color='gray')
    ax.set_axisbelow(True)

    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xticks(range(len(years_sorted)))
    ax.set_xticklabels(years_sorted, fontsize=11)
    ax.tick_params(axis='y', labelsize=11)

    # Legend
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left',
              fontsize=9, frameon=False, labelspacing=0.8)

    plt.tight_layout()

    # Save
    output_dir.mkdir(parents=True, exist_ok=True)
    for fmt in ['png', 'pdf', 'svg']:
        fig.savefig(output_dir / f'malicious_behavior_trends.{fmt}',
                    dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')

    print(f"Saved behavior trends plot to {output_dir}")

    # Save data
    plot_data.to_csv(output_dir / 'behavior_trends_data.csv')

    plt.close()


def main():
    """Main function to run the analysis"""

    print("RQ3: Malicious Behavior Trends Analysis")
    print("=" * 50)

    if not CLASSIFICATIONS_FILE.exists():
        print(f"Error: Classifications file not found at {CLASSIFICATIONS_FILE}")
        return

    if not TIME_FILE.exists():
        print(f"Error: Time file not found at {TIME_FILE}")
        return

    try:
        merged_df = load_and_process_data()
        behaviors_df = extract_behaviors(merged_df)

        if len(behaviors_df) == 0:
            print("No valid behavior data found. Exiting.")
            return

        create_behavior_trends_plot(behaviors_df, OUTPUT_DIR)

        print("\n" + "=" * 50)
        print("Analysis completed successfully!")
        print(f"Results saved to: {OUTPUT_DIR}")

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
