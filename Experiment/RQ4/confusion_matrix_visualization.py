#!/usr/bin/env python3
"""
RQ4: Confusion Matrix Visualization.
Creates heatmap visualizations for TP, TN, FP, FN across all tool combinations.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd

# Get the base directory
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Experiment/RQ4 -> NPMAnalysis

# Input/Output paths
COMPLEMENT_DIR = SCRIPT_DIR / "complement"
STATS_OUTPUT_DIR = PROJECT_ROOT / "Core" / "ToolDetection" / "DetectionResults"
OUTPUT_DIR = SCRIPT_DIR / "pic"


class ConfusionMatrixVisualizer:
    def __init__(self, data_dir, stats_dir):
        """
        Initialize the confusion matrix visualizer

        Args:
            data_dir: Directory containing the tool combination results
            stats_dir: Directory containing individual tool statistics
        """
        self.data_dir = Path(data_dir)
        self.stats_dir = Path(stats_dir)
        self.tools = ['genie', 'guarddog', 'ossgadget', 'packj_static', 'packj_trace', 'sap_DT', 'sap_RF', 'sap_XGB', 'socketai']

        # Load combination statistics from JSON file
        stats_file = self.data_dir / 'combination_statistics.json'
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                self.combination_stats = json.load(f)
        else:
            self.combination_stats = []
            print(f"Warning: {stats_file} not found. Run tool_complement_analysis.py first.")

        # Create lookup dictionary for quick access
        self.stats_lookup = {}
        for stat in self.combination_stats:
            key = (stat['tool1'], stat['tool2'], stat['strategy'])
            self.stats_lookup[key] = stat

    def get_combination_values(self, tool1, tool2, strategy):
        """Get confusion matrix values for a tool combination"""
        # Try both orders
        key1 = (tool1, tool2, strategy)
        key2 = (tool2, tool1, strategy)

        if key1 in self.stats_lookup:
            stat = self.stats_lookup[key1]
        elif key2 in self.stats_lookup:
            stat = self.stats_lookup[key2]
        else:
            return {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

        return {
            'TP': stat['tp'],
            'TN': stat['tn'],
            'FP': stat['fp'],
            'FN': stat['fn']
        }

    def load_individual_tool_data(self, tool_name):
        """Load individual tool performance data"""
        stats_dir = self.stats_dir / tool_name
        if not stats_dir.exists():
            return {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

        data = {}
        files = ['benign_reports.json', 'false_negatives.json', 'false_positives.json', 'malicious_reports.json']

        for file_name in files:
            file_path = stats_dir / file_name
            if file_path.exists():
                with open(file_path, 'r') as f:
                    data[file_name] = json.load(f)
            else:
                data[file_name] = {}

        tp = len(data['malicious_reports.json'])  # True Positives
        tn = len(data['benign_reports.json'])     # True Negatives
        fp = len(data['false_positives.json'])    # False Positives
        fn = len(data['false_negatives.json'])    # False Negatives

        return {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn}

    def create_confusion_matrix_grid(self, strategy='intersection'):
        """Create confusion matrix grid for all tool combinations"""
        n_tools = len(self.tools)

        # Initialize matrices for each metric
        tp_matrix = np.zeros((n_tools, n_tools))
        tn_matrix = np.zeros((n_tools, n_tools))
        fp_matrix = np.zeros((n_tools, n_tools))
        fn_matrix = np.zeros((n_tools, n_tools))

        for i, tool1 in enumerate(self.tools):
            for j, tool2 in enumerate(self.tools):
                if i == j:
                    # Diagonal - individual tool performance
                    values = self.load_individual_tool_data(tool1)
                else:
                    # Off-diagonal - tool combination
                    values = self.get_combination_values(tool1, tool2, strategy)

                tp_matrix[i, j] = values['TP']
                tn_matrix[i, j] = values['TN']
                fp_matrix[i, j] = values['FP']
                fn_matrix[i, j] = values['FN']

        return tp_matrix, tn_matrix, fp_matrix, fn_matrix

    def plot_confusion_matrix_grid(self, strategy='intersection'):
        """Plot the complete confusion matrix grid"""
        tp_matrix, tn_matrix, fp_matrix, fn_matrix = self.create_confusion_matrix_grid(strategy)

        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))

        # Define colormaps and titles
        plot_configs = [
            (tp_matrix, 'True Positives (TP)', 'Greens', axes[0, 0]),
            (tn_matrix, 'True Negatives (TN)', 'Blues', axes[0, 1]),
            (fp_matrix, 'False Positives (FP)', 'Reds', axes[1, 0]),
            (fn_matrix, 'False Negatives (FN)', 'Oranges', axes[1, 1])
        ]

        for matrix, title, cmap, ax in plot_configs:
            # Create heatmap
            im = ax.imshow(matrix, cmap=cmap, aspect='auto')

            # Add colorbar without border
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.ax.tick_params(labelsize=16)
            cbar.outline.set_visible(False)  # Remove colorbar border

            # Set title
            ax.set_title(title, fontsize=20, fontweight='bold', pad=20)

            # Remove axes spines (borders)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            # Set ticks and labels
            ax.set_xticks(range(len(self.tools)))
            ax.set_yticks(range(len(self.tools)))
            ax.set_xticklabels(self.tools, rotation=45, ha='right', fontsize=16)
            ax.set_yticklabels(self.tools, rotation=45, ha='right', fontsize=16)

            # Add text annotations
            for i in range(len(self.tools)):
                for j in range(len(self.tools)):
                    value = int(matrix[i, j])
                    text_color = 'white' if matrix[i, j] > matrix.max() * 0.5 else 'black'
                    ax.text(j, i, str(value),
                           ha='center', va='center',
                           color=text_color, fontweight='bold', fontsize=14)

        plt.tight_layout()

        # Create pic directory if it doesn't exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Save the figure
        filename = OUTPUT_DIR / f'confusion_matrix_{strategy}.png'
        plt.savefig(str(filename), dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved confusion matrix visualization to {filename}")

        # Also save as PDF
        pdf_filename = OUTPUT_DIR / f'confusion_matrix_{strategy}.pdf'
        plt.savefig(str(pdf_filename), dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Saved PDF to {pdf_filename}")

        return fig

    def create_both_visualizations(self):
        """Create both intersection and union visualizations"""
        print("Creating confusion matrix visualizations...")

        # Create intersection visualization
        print("\nCreating intersection strategy visualization...")
        fig_intersection = self.plot_confusion_matrix_grid('intersection')

        # Create union visualization
        print("\nCreating union strategy visualization...")
        fig_union = self.plot_confusion_matrix_grid('union')

        print("\nBoth visualizations completed!")

        return fig_intersection, fig_union


def main():
    print(f"Complement dir: {COMPLEMENT_DIR}")
    print(f"Stats output dir: {STATS_OUTPUT_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")

    # Check if combination_statistics.json exists
    stats_file = COMPLEMENT_DIR / 'combination_statistics.json'
    if not stats_file.exists():
        print(f"\nError: {stats_file} not found.")
        print("Please run tool_complement_analysis.py first to generate the data.")
        return

    # Create visualizer
    visualizer = ConfusionMatrixVisualizer(COMPLEMENT_DIR, STATS_OUTPUT_DIR)

    # Generate both visualizations
    visualizer.create_both_visualizations()

    print(f"\nAll visualizations saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
