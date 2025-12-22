#!/usr/bin/env python3
"""
RQ3: Malware Detection Rate Analysis Over Time
Analyzes how detection rates have changed over time for different malware detection tools.
Publication-quality visualizations for academic papers.
"""

import pandas as pd
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from collections import defaultdict
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Get the base directory
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent  # Experiment/RQ3/code -> NPMAnalysis

# Input paths
TIMESTAMP_CSV = PROJECT_ROOT / "Core" / "Data" / "timecollect" / "time" / "malware_time.csv"
STATS_OUTPUT_DIR = PROJECT_ROOT / "Core" / "ToolDetection" / "DetectionResults"

# Output paths
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic"

# Tool display names (more readable for papers)
TOOL_DISPLAY_NAMES = {
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

# Publication-quality color palette
COLORS = {
    'primary': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B',
                '#95190C', '#610345', '#107E7D', '#044B7F', '#6B2737'],
    'heatmap': 'RdYlGn',
    'detected': '#2E7D32',
    'missed': '#C62828',
    'bar': '#1976D2'
}


class MalwareDetectionAnalyzer:
    def __init__(self, csv_path, stats_output_dir, output_dir):
        self.csv_path = Path(csv_path)
        self.stats_output_dir = Path(stats_output_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.time_data = None
        self.detection_data = {}
        self.combined_data = {}

    def load_time_data(self):
        """Load and process the timestamp data from CSV"""
        print("Loading timestamp data...")
        self.time_data = pd.read_csv(self.csv_path)

        # Create package identifier
        self.time_data['package_id'] = self.time_data['package_name'] + '/' + self.time_data['version'].astype(str)

        # Parse timestamps and extract year
        self.time_data['timestamp'] = pd.to_datetime(self.time_data['timestamp'], errors='coerce')
        self.time_data['year'] = self.time_data['timestamp'].dt.year

        # Group years according to requirements
        def group_years(year):
            if pd.isna(year):
                return 'Unknown'
            elif year <= 2020:
                return '2011-2020'
            elif year == 2021:
                return '2021'
            elif year == 2022:
                return '2022'
            elif year == 2023:
                return '2023'
            elif year >= 2024:
                return '2024-2025'
            else:
                return 'Unknown'

        self.time_data['year_group'] = self.time_data['year'].apply(group_years)

        print(f"Loaded {len(self.time_data)} timestamp records")
        print(f"Year distribution:")
        print(self.time_data['year_group'].value_counts().sort_index())

    def load_detection_data(self):
        """Load detection results from all tools"""
        print("\nLoading detection data...")

        tool_dirs = [d for d in os.listdir(self.stats_output_dir)
                    if os.path.isdir(os.path.join(self.stats_output_dir, d))]

        for tool in tool_dirs:
            tool_path = os.path.join(self.stats_output_dir, tool)

            fn_path = os.path.join(tool_path, 'false_negatives.json')
            malicious_path = os.path.join(tool_path, 'malicious_reports.json')

            tool_data = {
                'false_negatives': {},
                'true_positives': {}
            }

            if os.path.exists(fn_path):
                with open(fn_path, 'r') as f:
                    tool_data['false_negatives'] = json.load(f)

            if os.path.exists(malicious_path):
                with open(malicious_path, 'r') as f:
                    malicious_data = json.load(f)
                    for pkg_id, info in malicious_data.items():
                        if isinstance(info, dict) and info.get('actual') == 'malware' and info.get('prediction') == 'malware':
                            tool_data['true_positives'][pkg_id] = info

            self.detection_data[tool] = tool_data

            print(f"Tool {tool}: {len(tool_data['false_negatives'])} FN, "
                  f"{len(tool_data['true_positives'])} TP")

    def combine_data(self):
        """Combine detection data with timestamp data"""
        print("\nCombining detection and timestamp data...")

        for tool, tool_data in self.detection_data.items():
            combined_tool_data = defaultdict(lambda: defaultdict(lambda: {'detected': 0, 'missed': 0, 'total': 0}))

            for pkg_id in tool_data['false_negatives']:
                clean_pkg_id = pkg_id.replace('##', '/')
                time_match = self.time_data[self.time_data['package_id'] == clean_pkg_id]
                if not time_match.empty:
                    year_group = time_match.iloc[0]['year_group']
                    combined_tool_data[year_group]['malware']['missed'] += 1
                    combined_tool_data[year_group]['malware']['total'] += 1
                else:
                    combined_tool_data['Unknown']['malware']['missed'] += 1
                    combined_tool_data['Unknown']['malware']['total'] += 1

            for pkg_id in tool_data['true_positives']:
                clean_pkg_id = pkg_id.replace('##', '/')
                time_match = self.time_data[self.time_data['package_id'] == clean_pkg_id]
                if not time_match.empty:
                    year_group = time_match.iloc[0]['year_group']
                    combined_tool_data[year_group]['malware']['detected'] += 1
                    combined_tool_data[year_group]['malware']['total'] += 1
                else:
                    combined_tool_data['Unknown']['malware']['detected'] += 1
                    combined_tool_data['Unknown']['malware']['total'] += 1

            self.combined_data[tool] = dict(combined_tool_data)

        print("Data combination completed")

    def calculate_detection_rates(self):
        """Calculate detection rates for each tool and year group"""
        detection_rates = {}

        for tool, tool_data in self.combined_data.items():
            detection_rates[tool] = {}

            for year_group, categories in tool_data.items():
                if 'malware' in categories:
                    stats = categories['malware']
                    total = stats['total']
                    detected = stats['detected']

                    if total > 0:
                        detection_rate = (detected / total) * 100
                        detection_rates[tool][year_group] = {
                            'detection_rate': detection_rate,
                            'detected': detected,
                            'missed': stats['missed'],
                            'total': total
                        }

        return detection_rates

    def _setup_plot_style(self):
        """Setup publication-quality plot style"""
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica'],
            'font.size': 12,
            'axes.labelsize': 14,
            'axes.titlesize': 16,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'legend.fontsize': 11,
            'figure.titlesize': 18,
            'axes.linewidth': 1.2,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'savefig.facecolor': 'white',
            'savefig.edgecolor': 'white',
            'savefig.bbox': 'tight',
            'savefig.pad_inches': 0.1
        })

    def _get_tool_display_name(self, tool):
        """Get display name for tool"""
        return TOOL_DISPLAY_NAMES.get(tool, tool)

    def create_heatmap(self, detection_rates):
        """Create publication-quality heatmap"""
        self._setup_plot_style()

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        # Sort tools by average detection rate
        tool_avg_rates = {}
        for tool in detection_rates.keys():
            rates = [detection_rates[tool].get(yg, {'detection_rate': 0})['detection_rate']
                    for yg in year_groups]
            tool_avg_rates[tool] = np.mean(rates)

        sorted_tools = sorted(tool_avg_rates.keys(), key=lambda x: tool_avg_rates[x], reverse=True)

        # Build rate matrix
        rate_matrix = []
        tool_labels = []
        for tool in sorted_tools:
            tool_rates = [detection_rates[tool].get(yg, {'detection_rate': 0})['detection_rate']
                         for yg in year_groups]
            rate_matrix.append(tool_rates)
            tool_labels.append(self._get_tool_display_name(tool))

        fig, ax = plt.subplots(figsize=(10, 7))

        # Create heatmap
        im = ax.imshow(rate_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
        cbar.set_label('Detection Rate (%)', fontsize=14, fontweight='bold')
        cbar.ax.tick_params(labelsize=12)

        # Set ticks and labels
        ax.set_xticks(np.arange(len(year_groups)))
        ax.set_yticks(np.arange(len(tool_labels)))
        ax.set_xticklabels(year_groups, fontsize=13, fontweight='medium')
        ax.set_yticklabels(tool_labels, fontsize=13, fontweight='medium')

        # Add text annotations
        for i in range(len(tool_labels)):
            for j in range(len(year_groups)):
                value = rate_matrix[i][j]
                text_color = 'white' if value < 40 or value > 75 else 'black'
                ax.text(j, i, f'{value:.1f}', ha='center', va='center',
                       color=text_color, fontsize=12, fontweight='bold')

        ax.set_xlabel('Time Period', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_ylabel('Detection Tool', fontsize=14, fontweight='bold', labelpad=10)

        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_heatmap_detection_rates.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved heatmap to {self.output_dir}/fig_heatmap_detection_rates.[png/pdf/svg]")

        plt.close()

    def create_line_plot(self, detection_rates):
        """Create publication-quality line plot"""
        import matplotlib as mpl

        # Publication-quality settings
        mpl.rcParams['font.family'] = 'serif'
        mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
        mpl.rcParams['font.size'] = 12
        mpl.rcParams['axes.linewidth'] = 1.0
        mpl.rcParams['pdf.fonttype'] = 42
        mpl.rcParams['ps.fonttype'] = 42

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        # Sort tools by average detection rate
        tool_avg_rates = {}
        for tool in detection_rates.keys():
            rates = [detection_rates[tool].get(yg, {'detection_rate': 0})['detection_rate']
                    for yg in year_groups]
            tool_avg_rates[tool] = np.mean(rates)

        sorted_tools = sorted(tool_avg_rates.keys(), key=lambda x: tool_avg_rates[x], reverse=True)

        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

        # Professional color palette - more distinguishable
        colors = ['#1E88E5', '#D81B60', '#FFC107', '#004D40', '#7B1FA2',
                  '#FF5722', '#00ACC1', '#5D4037', '#43A047']
        markers = ['o', 's', '^', 'D', 'v', 'p', 'h', '*', 'X']
        line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-']

        for i, tool in enumerate(sorted_tools):
            rates = [detection_rates[tool].get(yg, {'detection_rate': 0})['detection_rate']
                    for yg in year_groups]

            ax.plot(year_groups, rates,
                   marker=markers[i % len(markers)],
                   linestyle=line_styles[i % len(line_styles)],
                   linewidth=2.2,
                   markersize=9,
                   markeredgewidth=1.5,
                   markeredgecolor='white',
                   color=colors[i % len(colors)],
                   label=self._get_tool_display_name(tool),
                   alpha=0.9)

        ax.set_xlabel('Time Period', fontsize=13, fontweight='medium', labelpad=10)
        ax.set_ylabel('Detection Rate (%)', fontsize=13, fontweight='medium', labelpad=10)

        ax.set_ylim(0, 105)
        ax.set_yticks(range(0, 101, 20))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x)}'))

        # X-axis tick styling
        ax.tick_params(axis='x', labelsize=11)
        ax.tick_params(axis='y', labelsize=11)

        # Subtle grid
        ax.grid(True, linestyle='--', alpha=0.4, zorder=0, color='gray')
        ax.set_axisbelow(True)

        # Clean spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['bottom'].set_linewidth(0.8)

        # Legend - outside, no border
        legend = ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1),
                          frameon=False,
                          fontsize=10,
                          handlelength=2.5,
                          labelspacing=0.8)

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_line_detection_trends.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved line plot to {self.output_dir}/fig_line_detection_trends.[png/pdf/svg]")

        plt.close()

    def create_bar_samples_by_year(self, detection_rates):
        """Create bar chart of sample distribution by year"""
        self._setup_plot_style()

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        # Use actual time data for accurate counts
        year_totals = {}
        for yg in year_groups:
            count = len(self.time_data[self.time_data['year_group'] == yg])
            year_totals[yg] = count

        fig, ax = plt.subplots(figsize=(10, 6))

        bars = ax.bar(year_groups, [year_totals[yg] for yg in year_groups],
                     color=COLORS['bar'], alpha=0.85, edgecolor='white', linewidth=1.5)

        # Add value labels on bars
        for bar, yg in zip(bars, year_groups):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 20,
                   f'{int(height):,}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_xlabel('Time Period', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_ylabel('Number of Malware Samples', fontsize=14, fontweight='bold', labelpad=10)

        ax.set_ylim(0, max(year_totals.values()) * 1.15)

        # Grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_bar_samples_distribution.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved bar chart to {self.output_dir}/fig_bar_samples_distribution.[png/pdf/svg]")

        plt.close()

    def create_pie_samples_by_year(self):
        """Create publication-quality pie chart of sample distribution by year"""
        import matplotlib as mpl

        # Publication-quality settings
        mpl.rcParams['font.family'] = 'serif'
        mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
        mpl.rcParams['font.size'] = 11
        mpl.rcParams['pdf.fonttype'] = 42
        mpl.rcParams['ps.fonttype'] = 42

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        # Use actual time data for accurate counts
        year_totals = {}
        for yg in year_groups:
            count = len(self.time_data[self.time_data['year_group'] == yg])
            year_totals[yg] = count

        # Data
        labels = year_groups
        sizes = [year_totals[yg] for yg in year_groups]
        total = sum(sizes)

        # Professional color palette
        colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']

        # Create figure
        fig, ax = plt.subplots(figsize=(9, 7), dpi=300)

        # Create pie chart with slight explosion for emphasis
        explode = (0.02, 0.02, 0.02, 0.02, 0.02)

        wedges, texts, autotexts = ax.pie(
            sizes,
            explode=explode,
            labels=None,  # We'll add custom labels
            colors=colors,
            autopct=lambda pct: f'{pct:.1f}%',
            startangle=90,
            pctdistance=0.75,
            wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2),
            textprops=dict(fontsize=12, fontweight='medium')
        )

        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')

        # Add center circle for donut effect
        centre_circle = plt.Circle((0, 0), 0.40, fc='white')
        ax.add_patch(centre_circle)

        # Add total in center
        ax.text(0, 0.05, f'{total:,}', ha='center', va='center',
                fontsize=20, fontweight='bold', color='#333333')
        ax.text(0, -0.12, 'Total Samples', ha='center', va='center',
                fontsize=10, color='#666666')

        # Create custom legend with counts
        legend_labels = [f'{label} ({year_totals[label]:,})' for label in labels]
        legend = ax.legend(wedges, legend_labels,
                          title='Time Period',
                          loc='center left',
                          bbox_to_anchor=(1.0, 0.5),
                          fontsize=11,
                          frameon=False,
                          title_fontsize=12)
        legend.get_title().set_fontweight('bold')

        ax.set_aspect('equal')

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_pie_samples_distribution.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        print(f"Saved pie chart to {self.output_dir}/fig_pie_samples_distribution.[png/pdf/svg]")

        plt.close()

    def create_detected_vs_missed(self, detection_rates):
        """Create stacked bar chart of detected vs missed"""
        self._setup_plot_style()

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        # Use one tool's data for this visualization
        first_tool = list(detection_rates.keys())[0]

        detected_counts = []
        missed_counts = []

        for yg in year_groups:
            if yg in detection_rates[first_tool]:
                detected_counts.append(detection_rates[first_tool][yg]['detected'])
                missed_counts.append(detection_rates[first_tool][yg]['missed'])
            else:
                detected_counts.append(0)
                missed_counts.append(0)

        fig, ax = plt.subplots(figsize=(10, 6))

        x = np.arange(len(year_groups))
        width = 0.6

        bars1 = ax.bar(x, detected_counts, width, label='Detected',
                      color=COLORS['detected'], alpha=0.85, edgecolor='white', linewidth=1.5)
        bars2 = ax.bar(x, missed_counts, width, bottom=detected_counts, label='Missed',
                      color=COLORS['missed'], alpha=0.85, edgecolor='white', linewidth=1.5)

        # Add percentage labels
        for i, (det, mis) in enumerate(zip(detected_counts, missed_counts)):
            total = det + mis
            if total > 0:
                pct = det / total * 100
                ax.text(i, total + 20, f'{pct:.1f}%',
                       ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax.set_xlabel('Time Period', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_ylabel('Number of Samples', fontsize=14, fontweight='bold', labelpad=10)

        ax.set_xticks(x)
        ax.set_xticklabels(year_groups)
        ax.set_ylim(0, max([d + m for d, m in zip(detected_counts, missed_counts)]) * 1.15)

        # Legend
        ax.legend(loc='upper right', frameon=True, fancybox=False,
                 edgecolor='#CCCCCC', framealpha=1.0)

        # Grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_stacked_detected_vs_missed.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved stacked bar to {self.output_dir}/fig_stacked_detected_vs_missed.[png/pdf/svg]")

        plt.close()

    def create_avg_detection_rate(self, detection_rates):
        """Create bar chart of average detection rate by year"""
        self._setup_plot_style()

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        avg_rates = []
        for yg in year_groups:
            rates = []
            for tool in detection_rates.keys():
                if yg in detection_rates[tool]:
                    rates.append(detection_rates[tool][yg]['detection_rate'])
            avg_rates.append(np.mean(rates) if rates else 0)

        fig, ax = plt.subplots(figsize=(10, 6))

        # Color bars based on value
        colors = ['#2E7D32' if r >= 80 else '#FFA000' if r >= 60 else '#C62828' for r in avg_rates]

        bars = ax.bar(year_groups, avg_rates, color=colors, alpha=0.85,
                     edgecolor='white', linewidth=1.5)

        # Add value labels
        for bar, rate in zip(bars, avg_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{rate:.1f}%',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_xlabel('Time Period', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_ylabel('Average Detection Rate (%)', fontsize=14, fontweight='bold', labelpad=10)

        ax.set_ylim(0, 100)
        ax.set_yticks(range(0, 101, 20))

        # Add reference lines
        ax.axhline(y=80, color='#2E7D32', linestyle='--', alpha=0.5, linewidth=1.5)
        ax.axhline(y=60, color='#FFA000', linestyle='--', alpha=0.5, linewidth=1.5)

        # Grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_bar_avg_detection_rate.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved avg rate chart to {self.output_dir}/fig_bar_avg_detection_rate.[png/pdf/svg]")

        plt.close()

    def create_tool_comparison_boxplot(self, detection_rates):
        """Create box plot comparing tools"""
        self._setup_plot_style()

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025']

        # Prepare data
        data = []
        for tool in detection_rates.keys():
            for yg in year_groups:
                if yg in detection_rates[tool]:
                    data.append({
                        'Tool': self._get_tool_display_name(tool),
                        'Detection Rate': detection_rates[tool][yg]['detection_rate']
                    })

        df = pd.DataFrame(data)

        # Sort by median
        tool_medians = df.groupby('Tool')['Detection Rate'].median().sort_values(ascending=False)
        tool_order = tool_medians.index.tolist()

        fig, ax = plt.subplots(figsize=(12, 6))

        # Create boxplot
        box_colors = COLORS['primary'][:len(tool_order)]

        bp = ax.boxplot([df[df['Tool'] == tool]['Detection Rate'].values for tool in tool_order],
                       labels=tool_order, patch_artist=True, widths=0.6)

        # Color boxes
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Style medians
        for median in bp['medians']:
            median.set_color('black')
            median.set_linewidth(2)

        ax.set_xlabel('Detection Tool', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_ylabel('Detection Rate (%)', fontsize=14, fontweight='bold', labelpad=10)

        ax.set_ylim(0, 105)
        ax.set_yticks(range(0, 101, 20))

        # Rotate x labels
        plt.xticks(rotation=30, ha='right')

        # Grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=0)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Save
        for fmt in ['png', 'pdf', 'svg']:
            output_file = self.output_dir / f'fig_boxplot_tool_comparison.{fmt}'
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved boxplot to {self.output_dir}/fig_boxplot_tool_comparison.[png/pdf/svg]")

        plt.close()

    def create_visualizations(self, detection_rates):
        """Create all visualizations separately"""
        print("\nCreating publication-quality visualizations...")

        # Create each figure separately
        self.create_heatmap(detection_rates)
        self.create_line_plot(detection_rates)
        self.create_bar_samples_by_year(detection_rates)
        self.create_pie_samples_by_year()  # New pie chart
        self.create_detected_vs_missed(detection_rates)
        self.create_avg_detection_rate(detection_rates)
        self.create_tool_comparison_boxplot(detection_rates)

        print("\nAll visualizations created!")

    def generate_summary_report(self, detection_rates):
        """Generate a comprehensive summary report"""
        print("\nGenerating summary report...")

        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("MALWARE DETECTION RATE ANALYSIS REPORT (RQ3)")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        total_tools = len(detection_rates)
        total_samples = 0
        total_detected = 0

        for tool, tool_data in detection_rates.items():
            for year_group, stats in tool_data.items():
                total_samples += stats['total']
                total_detected += stats['detected']

        overall_rate = (total_detected / total_samples * 100) if total_samples > 0 else 0

        report_lines.append("OVERALL STATISTICS")
        report_lines.append("-" * 40)
        report_lines.append(f"Total tools analyzed: {total_tools}")
        report_lines.append(f"Total malware samples: {total_samples}")
        report_lines.append(f"Total detected: {total_detected}")
        report_lines.append(f"Overall detection rate: {overall_rate:.2f}%")
        report_lines.append("")

        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025', 'Unknown']

        report_lines.append("YEAR-WISE ANALYSIS")
        report_lines.append("-" * 40)

        for year_group in year_groups:
            year_total = 0
            year_detected = 0
            tools_with_data = 0

            for tool, tool_data in detection_rates.items():
                if year_group in tool_data:
                    year_total += tool_data[year_group]['total']
                    year_detected += tool_data[year_group]['detected']
                    tools_with_data += 1

            if year_total > 0:
                year_rate = (year_detected / year_total) * 100
                report_lines.append(f"{year_group}:")
                report_lines.append(f"  Samples: {year_total}")
                report_lines.append(f"  Detected: {year_detected}")
                report_lines.append(f"  Detection Rate: {year_rate:.2f}%")
                report_lines.append("")

        report_lines.append("TOOL-WISE ANALYSIS")
        report_lines.append("-" * 40)

        for tool, tool_data in detection_rates.items():
            tool_total = sum(stats['total'] for stats in tool_data.values())
            tool_detected = sum(stats['detected'] for stats in tool_data.values())
            tool_rate = (tool_detected / tool_total * 100) if tool_total > 0 else 0

            report_lines.append(f"{self._get_tool_display_name(tool)}:")
            report_lines.append(f"  Total samples: {tool_total}")
            report_lines.append(f"  Total detected: {tool_detected}")
            report_lines.append(f"  Overall detection rate: {tool_rate:.2f}%")

            for year_group in year_groups:
                if year_group in tool_data:
                    stats = tool_data[year_group]
                    report_lines.append(f"    {year_group}: {stats['detection_rate']:.2f}% "
                                      f"({stats['detected']}/{stats['total']})")
            report_lines.append("")

        report_lines.append("=" * 80)

        report_file = self.output_dir / 'detection_rate_summary_report.txt'
        with open(report_file, 'w') as f:
            f.write('\n'.join(report_lines))

        print(f"Saved report to {report_file}")
        print('\n'.join(report_lines))

        return report_lines

    def save_detection_rates_csv(self, detection_rates):
        """Save detection rates to CSV for further analysis"""
        rows = []
        for tool, tool_data in detection_rates.items():
            for year_group, stats in tool_data.items():
                rows.append({
                    'tool': tool,
                    'tool_display': self._get_tool_display_name(tool),
                    'year_group': year_group,
                    'detection_rate': stats['detection_rate'],
                    'detected': stats['detected'],
                    'missed': stats['missed'],
                    'total': stats['total']
                })

        df = pd.DataFrame(rows)
        csv_file = self.output_dir / 'detection_rates_by_year.csv'
        df.to_csv(csv_file, index=False)
        print(f"Saved CSV to {csv_file}")

    def run_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting malware detection rate analysis (RQ3)...")
        print(f"Timestamp CSV: {self.csv_path}")
        print(f"Stats output dir: {self.stats_output_dir}")
        print(f"Output dir: {self.output_dir}")

        self.load_time_data()
        self.load_detection_data()
        self.combine_data()

        detection_rates = self.calculate_detection_rates()

        self.save_detection_rates_csv(detection_rates)
        self.create_visualizations(detection_rates)
        self.generate_summary_report(detection_rates)

        print("\nAnalysis completed!")
        print(f"Files generated in: {self.output_dir}")

        return detection_rates


def main():
    """Main function to run the analysis"""
    print("RQ3: Malware Detection Rate Analysis Over Time")
    print("=" * 50)

    if not TIMESTAMP_CSV.exists():
        print(f"Error: Timestamp CSV file not found at {TIMESTAMP_CSV}")
        return

    if not STATS_OUTPUT_DIR.exists():
        print(f"Error: Stats output directory not found at {STATS_OUTPUT_DIR}")
        return

    analyzer = MalwareDetectionAnalyzer(TIMESTAMP_CSV, STATS_OUTPUT_DIR, OUTPUT_DIR)
    detection_rates = analyzer.run_analysis()

    return detection_rates


if __name__ == "__main__":
    detection_rates = main()
