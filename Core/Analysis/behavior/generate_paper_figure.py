#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate separate figures for paper.

Generates 4 individual figures:
1. Clustering visualization
2. Package complexity (donut chart)
3. Co-occurrence heatmap
4. Behavior distribution (bar chart)
"""

import json
import logging
from pathlib import Path
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from tqdm import tqdm

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parents[2]

INPUT_DIR = PROJECT_ROOT / "Core" / "Analysis" / "code_snipptes" / "malware_snippets"
OUTPUT_DIR = SCRIPT_DIR / "results" / "paper_figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Matplotlib configuration
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.linewidth'] = 1.0
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['figure.dpi'] = 300

# Colors
BAR_COLOR = '#1A5276'
DONUT_COLORS = ['#1A5276', '#2874A6', '#3498DB', '#5DADE2', '#85C1E9', '#AED6F1']
CLUSTER_COLORS = plt.cm.tab20(np.linspace(0, 1, 20))

# Figure size
FIG_SIZE = (8, 6)

# Unified font size - large for paper readability
FONT_SIZE = 18


def collect_behavior_data(input_dir: Path, top_n: int = 15):
    """Collect behavior data from malware snippets."""
    logger.info("Collecting behavior data...")

    json_files = list(input_dir.glob("**/result.json"))

    packages = {}  # package_key -> set of behaviors
    snippets = []  # all snippets

    for json_path in tqdm(json_files, desc="Collecting"):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            metadata = data.get('metadata', {})
            package_name = metadata.get('package_name', 'unknown')
            version = metadata.get('version', 'unknown')
            package_key = f"{package_name}@{version}"

            if package_key not in packages:
                packages[package_key] = set()

            for snippet in data.get('malicious_snippets', []):
                behaviors = snippet.get('validate_behavior_formal', [])
                if behaviors:
                    packages[package_key].update(behaviors)
                    snippets.append({'behaviors': behaviors})
        except:
            pass

    # Calculate statistics
    package_behavior_counts = Counter()
    for behaviors in packages.values():
        for b in behaviors:
            package_behavior_counts[b] += 1

    # Top N behaviors
    top_behaviors = [b for b, _ in package_behavior_counts.most_common(top_n)]
    top_counts = {b: package_behavior_counts[b] for b in top_behaviors}

    # Package complexity
    complexity = [len(b) for b in packages.values()]

    # Co-occurrence matrix
    behavior_to_idx = {b: i for i, b in enumerate(top_behaviors)}
    n = len(top_behaviors)
    cooccurrence = np.zeros((n, n), dtype=int)

    for snippet in snippets:
        snippet_behaviors = [b for b in snippet['behaviors'] if b in behavior_to_idx]
        for i, b1 in enumerate(snippet_behaviors):
            for b2 in snippet_behaviors[i:]:
                idx1, idx2 = behavior_to_idx[b1], behavior_to_idx[b2]
                cooccurrence[idx1, idx2] += 1
                if idx1 != idx2:
                    cooccurrence[idx2, idx1] += 1

    return {
        'top_behaviors': top_behaviors,
        'top_counts': top_counts,
        'total_packages': len(packages),
        'complexity': complexity,
        'cooccurrence': cooccurrence
    }


def collect_clustering_data(input_dir: Path):
    """Collect clustering data (single behavior summaries)."""
    logger.info("Collecting clustering data...")

    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        from sklearn.manifold import TSNE
        from sklearn.preprocessing import normalize
    except ImportError:
        logger.error("Required packages not installed")
        return None

    json_files = list(input_dir.glob("**/result.json"))

    summaries = []
    for json_path in tqdm(json_files, desc="Collecting summaries"):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for snippet in data.get('malicious_snippets', []):
                summary = snippet.get('behavior_summary', '')
                behaviors = snippet.get('validate_behavior_formal', [])

                if summary and len(summary.strip()) > 10 and len(behaviors) == 1:
                    summaries.append(summary.strip())
        except:
            pass

    logger.info(f"Found {len(summaries)} single-behavior summaries")

    # Compute embeddings
    logger.info("Computing embeddings...")
    model = SentenceTransformer('all-mpnet-base-v2')
    embeddings = model.encode(summaries, show_progress_bar=True, batch_size=64)

    # Normalize for cosine similarity
    embeddings_norm = normalize(embeddings, norm='l2')

    # Cluster
    logger.info("Clustering...")
    kmeans = KMeans(n_clusters=15, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings_norm)

    # Reduce dimensions
    logger.info("Reducing dimensions...")
    pca = PCA(n_components=50, random_state=42)
    embeddings_pca = pca.fit_transform(embeddings)

    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings_pca)

    return {
        'embeddings_2d': embeddings_2d,
        'labels': labels,
        'n_samples': len(summaries)
    }


def format_behavior_name(name: str) -> str:
    """Format behavior name for display."""
    return name.replace('_', ' ').title()


def generate_clustering_figure(cluster_data):
    """Generate clustering visualization figure."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    embeddings_2d = cluster_data['embeddings_2d']
    labels_cluster = cluster_data['labels']

    unique_labels = sorted(set(labels_cluster))
    for label in unique_labels:
        mask_c = labels_cluster == label
        color = CLUSTER_COLORS[label % 20]
        ax.scatter(
            embeddings_2d[mask_c, 0], embeddings_2d[mask_c, 1],
            c=[color], s=40, alpha=0.7, edgecolors='white', linewidth=0.3,
            label=f'Cluster {label}'
        )

    ax.set_xlabel('Dimension 1', fontsize=FONT_SIZE, fontweight='bold')
    ax.set_ylabel('Dimension 2', fontsize=FONT_SIZE, fontweight='bold')
    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=FONT_SIZE, ncol=1)

    plt.tight_layout()
    output_path = OUTPUT_DIR / 'fig_clustering.pdf'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"Saved: {output_path}")


def generate_complexity_figure(behavior_data):
    """Generate package complexity donut chart."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    complexity = behavior_data['complexity']
    complexity_counter = Counter(complexity)
    max_c = max(complexity_counter.keys())

    bin_labels = ['1 behavior', '2 behaviors', '3 behaviors', '4 behaviors', '5 behaviors', '6+ behaviors']
    bin_counts = [complexity_counter.get(i, 0) for i in range(1, 6)]
    bin_counts.append(sum(complexity_counter.get(i, 0) for i in range(6, max_c + 1)))

    non_zero = [(l, c, color) for l, c, color in zip(bin_labels, bin_counts, DONUT_COLORS) if c > 0]
    labels_f = [x[0] for x in non_zero]
    counts_f = [x[1] for x in non_zero]
    colors_f = [x[2] for x in non_zero]

    wedges, texts, autotexts = ax.pie(
        counts_f, labels=None,
        autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
        colors=colors_f, pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5),
        startangle=90
    )

    for autotext in autotexts:
        autotext.set_fontsize(FONT_SIZE)
        autotext.set_fontweight('bold')
        autotext.set_color('white')

    legend = ax.legend(wedges, labels_f, title="Behaviors/Package",
                       loc="center left", bbox_to_anchor=(0.9, 0.5), fontsize=FONT_SIZE,
                       title_fontsize=FONT_SIZE, frameon=True)
    legend.get_frame().set_edgecolor('#CCCCCC')

    avg_c = np.mean(complexity)
    median_c = np.median(complexity)
    ax.text(0, 0, f'Mean: {avg_c:.1f}\nMedian: {median_c:.0f}',
            ha='center', va='center', fontsize=FONT_SIZE, fontweight='bold', color=BAR_COLOR)

    plt.tight_layout()
    output_path = OUTPUT_DIR / 'fig_complexity.pdf'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"Saved: {output_path}")


def generate_heatmap_figure(behavior_data):
    """Generate co-occurrence heatmap figure."""
    # Heatmap needs more space for 15x15 grid
    fig, ax = plt.subplots(figsize=(10, 8))

    labels_heat = [format_behavior_name(b) for b in behavior_data['top_behaviors']]
    mask = np.triu(np.ones_like(behavior_data['cooccurrence'], dtype=bool), k=1)

    sns.heatmap(
        behavior_data['cooccurrence'],
        mask=mask,
        annot=True,  # Show numbers inside cells
        fmt='d',
        cmap='YlOrRd',
        xticklabels=labels_heat,
        yticklabels=labels_heat,
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Co-occurrence Count', 'shrink': 0.8},
        ax=ax,
        annot_kws={'size': 8}  # Smaller font for cell numbers
    )

    # Fix label alignment - rotate and align properly, fontsize 14
    ax.set_xticklabels(ax.get_xticklabels(), rotation=55, ha='right', fontsize=FONT_SIZE)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, ha='right', fontsize=FONT_SIZE)

    plt.tight_layout()
    output_path = OUTPUT_DIR / 'fig_heatmap.pdf'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"Saved: {output_path}")


def generate_distribution_figure(behavior_data):
    """Generate behavior distribution bar chart."""
    # Bar chart with 15 behaviors
    fig, ax = plt.subplots(figsize=(10, 6))

    behaviors = [format_behavior_name(b) for b in behavior_data['top_behaviors']]
    counts = [behavior_data['top_counts'][b] for b in behavior_data['top_behaviors']]

    x_pos = np.arange(len(behaviors))
    bars = ax.bar(x_pos, counts, color=BAR_COLOR, edgecolor='white', linewidth=0.8, width=0.7)

    # Add value labels on top of bars with enough spacing
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.02,
                f'{count}', ha='center', va='bottom', fontsize=FONT_SIZE, fontweight='medium')

    ax.set_xticks(x_pos)
    ax.set_xticklabels(behaviors, rotation=55, ha='right', fontsize=FONT_SIZE)
    ax.set_ylabel('Number of Packages', fontsize=FONT_SIZE, fontweight='bold')
    ax.tick_params(axis='y', labelsize=FONT_SIZE)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)

    # Add some padding at the top for labels
    ax.set_ylim(0, max(counts) * 1.15)

    plt.tight_layout()
    output_path = OUTPUT_DIR / 'fig_distribution.pdf'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"Saved: {output_path}")


def generate_combined_figure(behavior_data, cluster_data):
    """Generate combined figure with all 4 subplots."""
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(20, 18))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1], width_ratios=[1, 1],
                  hspace=0.4, wspace=0.35)

    # ==========================================================================
    # (a) Top-left: Clustering Visualization
    # ==========================================================================
    ax1 = fig.add_subplot(gs[0, 0])

    embeddings_2d = cluster_data['embeddings_2d']
    labels_cluster = cluster_data['labels']

    unique_labels = sorted(set(labels_cluster))
    for label in unique_labels:
        mask_c = labels_cluster == label
        color = CLUSTER_COLORS[label % 20]
        ax1.scatter(
            embeddings_2d[mask_c, 0], embeddings_2d[mask_c, 1],
            c=[color], s=50, alpha=0.7, edgecolors='white', linewidth=0.3,
            label=f'Cluster {label}'
        )

    ax1.set_xlabel('Dimension 1', fontsize=FONT_SIZE, fontweight='bold')
    ax1.set_ylabel('Dimension 2', fontsize=FONT_SIZE, fontweight='bold')
    ax1.tick_params(axis='both', labelsize=16)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.legend(loc='upper right', fontsize=14, ncol=2)
    ax1.set_title('(a)', fontsize=FONT_SIZE, fontweight='bold', loc='left')

    # ==========================================================================
    # (b) Top-right: Package Complexity (Donut Chart)
    # ==========================================================================
    ax2 = fig.add_subplot(gs[0, 1])

    complexity = behavior_data['complexity']
    complexity_counter = Counter(complexity)
    max_c = max(complexity_counter.keys())

    bin_labels = ['1 behavior', '2 behaviors', '3 behaviors', '4 behaviors', '5 behaviors', '6+ behaviors']
    bin_counts = [complexity_counter.get(i, 0) for i in range(1, 6)]
    bin_counts.append(sum(complexity_counter.get(i, 0) for i in range(6, max_c + 1)))

    non_zero = [(l, c, color) for l, c, color in zip(bin_labels, bin_counts, DONUT_COLORS) if c > 0]
    labels_f = [x[0] for x in non_zero]
    counts_f = [x[1] for x in non_zero]
    colors_f = [x[2] for x in non_zero]

    wedges, texts, autotexts = ax2.pie(
        counts_f, labels=None,
        autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',
        colors=colors_f, pctdistance=0.78,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2.5),
        startangle=90
    )

    for autotext in autotexts:
        autotext.set_fontsize(16)
        autotext.set_fontweight('bold')
        autotext.set_color('white')

    legend = ax2.legend(wedges, labels_f, title="Behaviors/Package",
                        loc="center left", bbox_to_anchor=(0.85, 0.5), fontsize=16,
                        title_fontsize=16, frameon=True)
    legend.get_frame().set_edgecolor('#CCCCCC')

    avg_c = np.mean(complexity)
    median_c = np.median(complexity)
    ax2.text(0, 0, f'Mean: {avg_c:.1f}\nMedian: {median_c:.0f}',
             ha='center', va='center', fontsize=FONT_SIZE, fontweight='bold', color=BAR_COLOR)
    ax2.set_title('(b)', fontsize=FONT_SIZE, fontweight='bold', loc='left')

    # ==========================================================================
    # (c) Bottom-left: Co-occurrence Heatmap
    # ==========================================================================
    ax3 = fig.add_subplot(gs[1, 0])

    labels_heat = [format_behavior_name(b) for b in behavior_data['top_behaviors']]
    mask = np.triu(np.ones_like(behavior_data['cooccurrence'], dtype=bool), k=1)

    sns.heatmap(
        behavior_data['cooccurrence'],
        mask=mask,
        annot=True,
        fmt='d',
        cmap='YlOrRd',
        xticklabels=labels_heat,
        yticklabels=labels_heat,
        square=True,
        linewidths=0.5,
        cbar_kws={'label': 'Co-occurrence Count', 'shrink': 0.8},
        ax=ax3,
        annot_kws={'size': 10}
    )

    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=55, ha='right', fontsize=14)
    ax3.set_yticklabels(ax3.get_yticklabels(), rotation=0, ha='right', fontsize=14)
    ax3.set_title('(c)', fontsize=FONT_SIZE, fontweight='bold', loc='left')

    # ==========================================================================
    # (d) Bottom-right: Behavior Distribution (Bar Chart)
    # ==========================================================================
    ax4 = fig.add_subplot(gs[1, 1])

    behaviors = [format_behavior_name(b) for b in behavior_data['top_behaviors']]
    counts = [behavior_data['top_counts'][b] for b in behavior_data['top_behaviors']]

    x_pos = np.arange(len(behaviors))
    bars = ax4.bar(x_pos, counts, color=BAR_COLOR, edgecolor='white', linewidth=0.8, width=0.7)

    for bar, count in zip(bars, counts):
        ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.02,
                 f'{count}', ha='center', va='bottom', fontsize=14, fontweight='medium')

    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(behaviors, rotation=55, ha='right', fontsize=14)
    ax4.set_ylabel('Number of Packages', fontsize=FONT_SIZE, fontweight='bold')
    ax4.tick_params(axis='y', labelsize=16)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax4.set_axisbelow(True)
    ax4.set_ylim(0, max(counts) * 1.15)
    ax4.set_title('(d)', fontsize=FONT_SIZE, fontweight='bold', loc='left')

    # Save
    plt.tight_layout()
    output_path = OUTPUT_DIR / 'behavior_analysis_combined.pdf'
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    logger.info(f"Saved combined figure to {output_path}")
    print(f"\nCombined figure saved to: {output_path}")


def generate_all_figures():
    """Generate all figures."""

    # Collect data
    behavior_data = collect_behavior_data(INPUT_DIR)
    cluster_data = collect_clustering_data(INPUT_DIR)

    if cluster_data is None:
        logger.error("Failed to collect clustering data")
        return

    # Generate individual figures
    generate_clustering_figure(cluster_data)
    generate_complexity_figure(behavior_data)
    generate_heatmap_figure(behavior_data)
    generate_distribution_figure(behavior_data)

    # Generate combined figure
    generate_combined_figure(behavior_data, cluster_data)

    print(f"\nAll figures saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all_figures()
