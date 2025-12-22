#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Behavior Formal Analyzer

Analyze the distribution of validate_behavior_formal labels from malware snippets.
Generates statistics and publication-quality visualizations.

Output:
    - behavior_distribution.pdf: Bar chart of behavior distribution
    - behavior_cooccurrence_heatmap.pdf: Heatmap of behavior co-occurrence
    - snippet_vs_package_comparison.pdf: Comparison chart
    - behavior_pie_chart.pdf: Pie chart of top behaviors
"""

import os
import json
import glob
import logging
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Configure logging (only for this module, suppress other libraries)
logging.basicConfig(
    level=logging.WARNING,  # Set root logger to WARNING to suppress other libraries
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Our logger still shows INFO

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parents[2]

# Input directory
DEFAULT_INPUT_DIR = PROJECT_ROOT / "Core" / "Analysis" / "code_snipptes" / "malware_snippets"

# Output directory
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "results" / "behavior_formal_stats"

# Matplotlib configuration for publication quality
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['figure.dpi'] = 300

# Color palette for visualizations
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'neutral': '#C73E1D',
    'success': '#3A7D44'
}


# =============================================================================
# Data Collection
# =============================================================================

class BehaviorFormalAnalyzer:
    """Analyze validate_behavior_formal distribution from malware snippets."""

    def __init__(self, input_dir: Path = None, output_dir: Path = None, top_n: int = 15):
        self.input_dir = Path(input_dir or DEFAULT_INPUT_DIR)
        self.output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Top N behaviors to keep for visualization
        self.top_n = top_n

        # Data storage
        self.snippets = []  # All snippet data
        self.packages = {}  # package_name@version -> set of behaviors

        # Statistics (raw, all behaviors)
        self.behavior_counts = Counter()  # behavior -> count (snippet level)
        self.package_behavior_counts = Counter()  # behavior -> count (package level)
        self.cooccurrence_matrix = None

        # Top N statistics (for visualization)
        self.top_behavior_counts = Counter()
        self.top_package_behavior_counts = Counter()
        self.top_behaviors = []  # List of top N behavior names

    def collect_data(self) -> int:
        logger.info(f"Collecting data from {self.input_dir}")

        json_files = list(self.input_dir.glob("**/result.json"))
        logger.info(f"Found {len(json_files)} result.json files")

        for json_path in json_files:
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                metadata = data.get('metadata', {})
                package_name = metadata.get('package_name', 'unknown')
                version = metadata.get('version', 'unknown')
                package_key = f"{package_name}@{version}"

                if package_key not in self.packages:
                    self.packages[package_key] = set()

                for snippet in data.get('malicious_snippets', []):
                    behaviors = snippet.get('validate_behavior_formal', [])

                    if behaviors:
                        # Snippet-level counting
                        for behavior in behaviors:
                            self.behavior_counts[behavior] += 1

                        # Package-level: add to package's behavior set
                        self.packages[package_key].update(behaviors)

                        # Store snippet info
                        self.snippets.append({
                            'package': package_name,
                            'version': version,
                            'package_key': package_key,
                            'file': snippet.get('file', ''),
                            'type': snippet.get('type', ''),
                            'behaviors': behaviors,
                            'behavior_summary': snippet.get('behavior_summary', '')
                        })

            except Exception as e:
                logger.error(f"Error processing {json_path}: {e}")

        # Calculate package-level behavior counts
        for package_key, behaviors in self.packages.items():
            for behavior in behaviors:
                self.package_behavior_counts[behavior] += 1

        # Get Top N behaviors (by package count)
        self.top_behaviors = [b for b, _ in self.package_behavior_counts.most_common(self.top_n)]
        self.top_behavior_counts = Counter({
            b: self.behavior_counts[b] for b in self.top_behaviors
        })
        self.top_package_behavior_counts = Counter({
            b: self.package_behavior_counts[b] for b in self.top_behaviors
        })

        logger.info(f"Collected {len(self.snippets)} snippets from {len(self.packages)} packages")
        logger.info(f"Found {len(self.behavior_counts)} unique behavior types")
        logger.info(f"Using Top {self.top_n} behaviors for visualization")

        return len(self.snippets)

    def calculate_cooccurrence(self) -> np.ndarray:
        """Calculate behavior co-occurrence matrix (using filtered behaviors)."""
        behaviors = sorted(self.top_behavior_counts.keys())
        n = len(behaviors)
        behavior_to_idx = {b: i for i, b in enumerate(behaviors)}

        matrix = np.zeros((n, n), dtype=int)

        for snippet in self.snippets:
            # Only consider filtered behaviors
            snippet_behaviors = [b for b in snippet['behaviors'] if b in behavior_to_idx]
            for i, b1 in enumerate(snippet_behaviors):
                for b2 in snippet_behaviors[i:]:
                    idx1, idx2 = behavior_to_idx[b1], behavior_to_idx[b2]
                    matrix[idx1, idx2] += 1
                    if idx1 != idx2:
                        matrix[idx2, idx1] += 1

        self.cooccurrence_matrix = matrix
        self.behavior_labels = behaviors
        return matrix

    # =========================================================================
    # Visualization
    # =========================================================================

    def plot_behavior_distribution(self) -> None:
        """Create publication-quality bar chart of behavior distribution."""
        # Sort by count (use filtered data)
        sorted_behaviors = self.top_package_behavior_counts.most_common()
        behaviors = [b for b, _ in sorted_behaviors]
        counts = [c for _, c in sorted_behaviors]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Create horizontal bar chart
        y_pos = np.arange(len(behaviors))
        bars = ax.barh(y_pos, counts, color=COLORS['primary'], edgecolor='black', linewidth=0.5)

        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count + max(counts) * 0.01, i, f'{count}',
                    va='center', ha='left', fontsize=9)

        # Formatting
        ax.set_yticks(y_pos)
        ax.set_yticklabels([self._format_behavior_name(b) for b in behaviors], fontsize=10)
        ax.set_xlabel('Number of Packages', fontsize=12, fontweight='medium')
        ax.set_title('Distribution of Malicious Behaviors Across Packages', fontsize=14, fontweight='bold')

        # Set x-axis limit to accommodate labels
        ax.set_xlim(0, max(counts) * 1.15)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add grid
        ax.xaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Save
        output_path = self.output_dir / 'behavior_distribution.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        plt.close()

        logger.info(f"Saved behavior distribution plot to {output_path}")

    def plot_behavior_distribution_vertical(self) -> None:
        """Create vertical bar chart (alternative visualization)."""
        sorted_behaviors = self.top_package_behavior_counts.most_common()
        behaviors = [self._format_behavior_name(b) for b, _ in sorted_behaviors]
        counts = [c for _, c in sorted_behaviors]

        fig, ax = plt.subplots(figsize=(14, 6))

        x_pos = np.arange(len(behaviors))
        bars = ax.bar(x_pos, counts, color=COLORS['primary'], edgecolor='black', linewidth=0.5)

        # Add value labels on top
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.01,
                    f'{count}', ha='center', va='bottom', fontsize=8, rotation=0)

        ax.set_xticks(x_pos)
        ax.set_xticklabels(behaviors, rotation=45, ha='right', fontsize=9)
        ax.set_ylabel('Number of Packages', fontsize=12, fontweight='medium')
        ax.set_title('Distribution of Malicious Behaviors Across Packages', fontsize=14, fontweight='bold')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)

        plt.tight_layout()

        output_path = self.output_dir / 'behavior_distribution_vertical.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        plt.close()

        logger.info(f"Saved vertical bar chart to {output_path}")

    def plot_cooccurrence_heatmap(self) -> None:
        """Create heatmap of behavior co-occurrence."""
        if self.cooccurrence_matrix is None:
            self.calculate_cooccurrence()

        # Format labels
        labels = [self._format_behavior_name(b) for b in self.behavior_labels]

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 10))

        # Create heatmap
        mask = np.triu(np.ones_like(self.cooccurrence_matrix, dtype=bool), k=1)

        sns.heatmap(
            self.cooccurrence_matrix,
            mask=mask,
            annot=True,
            fmt='d',
            cmap='YlOrRd',
            xticklabels=labels,
            yticklabels=labels,
            square=True,
            linewidths=0.5,
            cbar_kws={'label': 'Co-occurrence Count', 'shrink': 0.8},
            ax=ax
        )

        ax.set_title('Behavior Co-occurrence Matrix', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.yticks(rotation=0, fontsize=9)

        plt.tight_layout()

        output_path = self.output_dir / 'behavior_cooccurrence_heatmap.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        plt.close()

        logger.info(f"Saved co-occurrence heatmap to {output_path}")

    def plot_snippet_vs_package_comparison(self) -> None:
        """Compare snippet-level vs package-level behavior counts."""
        behaviors = sorted(self.top_behavior_counts.keys())
        snippet_counts = [self.top_behavior_counts[b] for b in behaviors]
        package_counts = [self.top_package_behavior_counts[b] for b in behaviors]
        labels = [self._format_behavior_name(b) for b in behaviors]

        # Sort by package count
        sorted_indices = np.argsort(package_counts)[::-1]
        labels = [labels[i] for i in sorted_indices]
        snippet_counts = [snippet_counts[i] for i in sorted_indices]
        package_counts = [package_counts[i] for i in sorted_indices]

        fig, ax = plt.subplots(figsize=(14, 7))

        x = np.arange(len(labels))
        width = 0.35

        bars1 = ax.bar(x - width/2, snippet_counts, width, label='Snippet Level',
                       color=COLORS['primary'], edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width/2, package_counts, width, label='Package Level',
                       color=COLORS['secondary'], edgecolor='black', linewidth=0.5)

        ax.set_ylabel('Count', fontsize=12, fontweight='medium')
        ax.set_title('Behavior Distribution: Snippet Level vs Package Level', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=10)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)

        plt.tight_layout()

        output_path = self.output_dir / 'snippet_vs_package_comparison.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        plt.close()

        logger.info(f"Saved comparison chart to {output_path}")

    def plot_behavior_pie_chart(self) -> None:
        """Create pie chart for top behaviors."""
        sorted_behaviors = self.top_package_behavior_counts.most_common(10)
        labels = [self._format_behavior_name(b) for b, _ in sorted_behaviors]
        sizes = [c for _, c in sorted_behaviors]

        # Add "Others" category
        other_count = sum(c for _, c in self.top_package_behavior_counts.most_common()[10:])
        if other_count > 0:
            labels.append('Others')
            sizes.append(other_count)

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,
            autopct='%1.1f%%',
            colors=colors,
            pctdistance=0.75,
            wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2)
        )

        # Add legend
        ax.legend(wedges, labels, title="Behaviors", loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)

        ax.set_title('Top 10 Malicious Behavior Types', fontsize=14, fontweight='bold')

        plt.tight_layout()

        output_path = self.output_dir / 'behavior_pie_chart.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        
        plt.close()

        logger.info(f"Saved pie chart to {output_path}")

    # =========================================================================
    # Helpers
    # =========================================================================

    @staticmethod
    def _format_behavior_name(name: str) -> str:
        """Format behavior name for display."""
        return name.replace('_', ' ').title()

    def print_summary(self) -> None:
        """Print summary to console."""
        print("\n" + "=" * 60)
        print("BEHAVIOR FORMAL ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"\nTotal snippets analyzed: {len(self.snippets)}")
        print(f"Total packages: {len(self.packages)}")
        print(f"Unique behavior types (total): {len(self.behavior_counts)}")
        print(f"\nTop {self.top_n} behaviors (by package count):")
        print("-" * 50)
        for behavior, count in self.top_package_behavior_counts.most_common():
            pct = count / len(self.packages) * 100
            print(f"  {self._format_behavior_name(behavior):40s} {count:5d} ({pct:5.1f}%)")
        print(f"\nResults saved to: {self.output_dir}")

    # =========================================================================
    # Main Entry
    # =========================================================================

    def run(self) -> None:
        """Run the complete analysis pipeline."""
        # Collect data
        if self.collect_data() == 0:
            logger.error("No data collected. Exiting.")
            return

        # Calculate co-occurrence
        self.calculate_cooccurrence()

        # Generate visualizations
        logger.info("Generating visualizations...")
        self.plot_behavior_distribution()
        self.plot_behavior_distribution_vertical()
        self.plot_cooccurrence_heatmap()
        self.plot_snippet_vs_package_comparison()
        self.plot_behavior_pie_chart()

        # Print summary
        self.print_summary()


# =============================================================================
# Entry Point
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze validate_behavior_formal distribution from malware snippets"
    )
    parser.add_argument(
        "--input", "-i",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Input directory containing malware snippets"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for results"
    )
    parser.add_argument(
        "--top-n", "-n",
        type=int,
        default=15,
        help="Number of top behaviors to show (default: 15)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    analyzer = BehaviorFormalAnalyzer(args.input, args.output, top_n=args.top_n)
    analyzer.run()


if __name__ == "__main__":
    main()
