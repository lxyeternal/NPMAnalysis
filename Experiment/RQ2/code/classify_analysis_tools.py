#!/usr/bin/env python3
"""
RQ2: Visualization for malware detection rates by classification.
Generates detection rate comparison charts across different tools and attack types.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Get the base directory
SCRIPT_DIR = Path(__file__).parent.resolve()

# Input/Output paths
INPUT_CSV = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "data" / "combined_malware_analysis.csv"
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic" / "behavior_detection" / "figures"


def load_and_process_data(csv_file):
    """Load and process the malware analysis data"""
    df = pd.read_csv(csv_file)

    # Calculate detection rates for each tool and classification
    detection_rates = []

    for tool in df['tool'].unique():
        tool_data = df[df['tool'] == tool]

        for classification in tool_data['classification'].unique():
            class_data = tool_data[tool_data['classification'] == classification]

            # Get false negatives and malicious reports counts
            fn_count = class_data[class_data['category'] == 'false_negatives']['count'].values
            mr_count = class_data[class_data['category'] == 'malicious_reports']['count'].values

            if len(fn_count) > 0 and len(mr_count) > 0:
                fn = fn_count[0]
                mr = mr_count[0]
                total = fn + mr
                detection_rate = (mr / total) * 100 if total > 0 else 0

                detection_rates.append({
                    'tool': tool,
                    'classification': classification,
                    'detection_rate': detection_rate,
                    'false_negatives': fn,
                    'malicious_reports': mr,
                    'total': total
                })

    return pd.DataFrame(detection_rates)


def create_detection_rate_visualization(detection_df):
    """Create a comprehensive detection rate visualization"""

    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")

    # Create figure with high DPI for publication quality
    fig, ax = plt.subplots(figsize=(16, 10), dpi=300)

    # Get unique tools and classifications
    tools = detection_df['tool'].unique()
    classifications = detection_df['classification'].unique()

    # Sort classifications by average detection rate for better visualization
    avg_detection = detection_df.groupby('classification')['detection_rate'].mean().sort_values(ascending=False)
    classifications = avg_detection.index.tolist()

    # Define colors for each tool
    colors = plt.cm.Set3(np.linspace(0, 1, len(tools)))
    tool_colors = dict(zip(tools, colors))

    # Define line styles for better distinction
    line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']

    # Plot lines for each tool
    for i, tool in enumerate(tools):
        tool_data = detection_df[detection_df['tool'] == tool]

        # Prepare data points for this tool
        x_positions = []
        y_values = []

        for j, classification in enumerate(classifications):
            class_data = tool_data[tool_data['classification'] == classification]
            if not class_data.empty:
                x_positions.append(j)
                y_values.append(class_data['detection_rate'].iloc[0])

        # Plot the line
        ax.plot(x_positions, y_values,
               color=tool_colors[tool],
               linestyle=line_styles[i % len(line_styles)],
               marker=markers[i % len(markers)],
               markersize=10,  # Increased marker size
               linewidth=3,    # Increased line width
               label=tool,
               alpha=0.8,
               markerfacecolor='white',
               markeredgecolor=tool_colors[tool],
               markeredgewidth=2.5)

    # Customize the plot with larger fonts
    ax.set_xlabel('Malware Classification Types', fontsize=22, fontweight='bold')
    ax.set_ylabel('Detection Rate (%)', fontsize=22, fontweight='bold')
    ax.set_title('Malware Detection Performance Comparison Across Different Tools and Attack Types',
                fontsize=24, fontweight='bold', pad=20)

    # Set x-axis labels with larger font
    ax.set_xticks(range(len(classifications)))
    ax.set_xticklabels(classifications, rotation=45, ha='right', fontsize=18)

    # Set y-axis with larger font
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 10))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}%'))
    ax.tick_params(axis='y', labelsize=18)

    # Add grid
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Customize legend with larger font
    legend = ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
                      fontsize=18, frameon=True, fancybox=True, shadow=False)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)

    # Adjust layout
    plt.tight_layout()

    return fig, ax


def generate_summary_statistics(detection_df):
    """Generate summary statistics for the analysis"""
    print("=== Malware Detection Analysis Summary ===\n")

    # Overall statistics
    print("1. Overall Detection Rate Statistics:")
    overall_stats = detection_df.groupby('tool')['detection_rate'].agg(['mean', 'std', 'min', 'max'])
    print(overall_stats.round(2))
    print()

    # Best performing tool per category
    print("2. Best Performing Tool per Malware Category:")
    best_per_category = detection_df.loc[detection_df.groupby('classification')['detection_rate'].idxmax()]
    for _, row in best_per_category.iterrows():
        print(f"{row['classification']}: {row['tool']} ({row['detection_rate']:.1f}%)")
    print()

    # Tool ranking by average detection rate
    print("3. Tool Ranking by Average Detection Rate:")
    tool_ranking = detection_df.groupby('tool')['detection_rate'].mean().sort_values(ascending=False)
    for i, (tool, rate) in enumerate(tool_ranking.items(), 1):
        print(f"{i}. {tool}: {rate:.1f}%")
    print()

    # Category difficulty ranking
    print("4. Malware Category Detection Difficulty (Average across all tools):")
    category_difficulty = detection_df.groupby('classification')['detection_rate'].mean().sort_values(ascending=True)
    for i, (category, rate) in enumerate(category_difficulty.items(), 1):
        print(f"{i}. {category}: {rate:.1f}% (Difficulty: {'High' if rate < 50 else 'Medium' if rate < 80 else 'Low'})")


def main():
    """Main function to run the complete analysis"""
    print(f"Input CSV: {INPUT_CSV}")
    print(f"Output dir: {OUTPUT_DIR}")

    try:
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Load and process data
        detection_df = load_and_process_data(INPUT_CSV)

        # Generate summary statistics
        generate_summary_statistics(detection_df)

        # Create visualization
        fig, ax = create_detection_rate_visualization(detection_df)

        # Save the plot in multiple formats for publication
        plt.savefig(OUTPUT_DIR / 'malware_detection_rates.png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.savefig(OUTPUT_DIR / 'malware_detection_rates.pdf', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.savefig(OUTPUT_DIR / 'malware_detection_rates.svg', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')

        print(f"\n5. Visualizations saved to:")
        print(f"   - {OUTPUT_DIR}/malware_detection_rates.png")
        print(f"   - {OUTPUT_DIR}/malware_detection_rates.pdf")
        print(f"   - {OUTPUT_DIR}/malware_detection_rates.svg")

        # Save processed data
        detection_df.to_csv(OUTPUT_DIR / 'processed_detection_rates.csv', index=False)
        print(f"   - {OUTPUT_DIR}/processed_detection_rates.csv")

        # Show the plot (optional, comment out if running non-interactively)
        # plt.show()

    except FileNotFoundError:
        print(f"Error: Could not find the input CSV file at {INPUT_CSV}")
        print("Please run classify_statistic.py first to generate the data.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
