#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Behavior Summary Clustering V2

Improved clustering of behavior_summary texts:
1. Filter snippets with single behavior (cleaner data)
2. Use Sentence-BERT for semantic embeddings
3. Try multiple clustering algorithms including Spectral Clustering
4. Better evaluation metrics

Output:
    - results/behavior_summary_clustering_v2/
        - clustering results and visualizations (PDF only)
"""

import json
import warnings
import logging
from pathlib import Path
from collections import Counter
from typing import List, Dict, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm

# Scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import normalize

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parents[2]

DEFAULT_INPUT_DIR = PROJECT_ROOT / "Core" / "Analysis" / "code_snipptes" / "malware_snippets"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "results" / "behavior_summary_clustering"

# Matplotlib configuration for publication quality
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 12
mpl.rcParams['axes.linewidth'] = 1.0
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['figure.dpi'] = 300

# Color palette (blue gradient)
CLUSTER_COLORS = plt.cm.tab20(np.linspace(0, 1, 20))

# =============================================================================
# Optional imports
# =============================================================================

try:
    from sentence_transformers import SentenceTransformer
    HAS_SBERT = True
except ImportError:
    HAS_SBERT = False
    logger.warning("sentence-transformers not installed. Install with: pip install sentence-transformers")

try:
    import umap
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False


# =============================================================================
# Main Class
# =============================================================================

class BehaviorSummaryClustererV2:
    """Improved clustering of behavior summaries."""

    def __init__(self, input_dir: Path = None, output_dir: Path = None, n_clusters: int = 15):
        self.input_dir = Path(input_dir or DEFAULT_INPUT_DIR)
        self.output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.n_clusters = n_clusters

        # Data storage
        self.summaries = []          # behavior_summary texts
        self.metadata = []           # corresponding metadata
        self.single_behavior_type = []  # the single behavior type for each snippet

        # All data (before filtering)
        self.all_summaries_count = 0
        self.filtered_summaries_count = 0

        # Embeddings
        self.embeddings = None
        self.embeddings_2d = None
        self.embedding_method = None

        # Clustering results
        self.cluster_results = {}

    def collect_data(self, single_behavior_only: bool = True) -> int:
        """Collect behavior_summary texts, optionally filtering for single-behavior snippets."""
        logger.info(f"Collecting data from {self.input_dir}")
        logger.info(f"Filter mode: {'Single behavior only' if single_behavior_only else 'All snippets'}")

        json_files = list(self.input_dir.glob("**/result.json"))
        logger.info(f"Found {len(json_files)} result.json files")

        all_count = 0
        single_count = 0

        for json_path in tqdm(json_files, desc="Collecting summaries"):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                metadata = data.get('metadata', {})
                package_name = metadata.get('package_name', 'unknown')
                version = metadata.get('version', 'unknown')

                for snippet in data.get('malicious_snippets', []):
                    summary = snippet.get('behavior_summary', '')
                    behaviors = snippet.get('validate_behavior_formal', [])

                    if not summary or len(summary.strip()) < 10:
                        continue

                    all_count += 1

                    # Filter: only single behavior snippets
                    if single_behavior_only and len(behaviors) != 1:
                        continue

                    single_count += 1
                    self.summaries.append(summary.strip())
                    self.metadata.append({
                        'package': package_name,
                        'version': version,
                        'file': snippet.get('file', ''),
                        'type': snippet.get('type', ''),
                        'behaviors': behaviors
                    })
                    if behaviors:
                        self.single_behavior_type.append(behaviors[0])
                    else:
                        self.single_behavior_type.append('unknown')

            except Exception as e:
                logger.error(f"Error processing {json_path}: {e}")

        self.all_summaries_count = all_count
        self.filtered_summaries_count = single_count

        logger.info(f"Total summaries: {all_count}")
        logger.info(f"Single-behavior summaries: {single_count} ({single_count/all_count*100:.1f}%)")

        return len(self.summaries)

    # =========================================================================
    # Embedding Methods
    # =========================================================================

    def compute_tfidf_embeddings(self) -> np.ndarray:
        """Compute TF-IDF embeddings."""
        logger.info("Computing TF-IDF embeddings...")

        vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.95,
            ngram_range=(1, 2),
            stop_words='english'
        )

        self.embeddings = vectorizer.fit_transform(self.summaries).toarray()
        self.embedding_method = 'TF-IDF'

        logger.info(f"TF-IDF embeddings shape: {self.embeddings.shape}")
        return self.embeddings

    def compute_sbert_embeddings(self, model_name: str = 'all-mpnet-base-v2') -> np.ndarray:
        """Compute Sentence-BERT embeddings using a powerful model."""
        if not HAS_SBERT:
            logger.warning("sentence-transformers not available. Using TF-IDF.")
            return self.compute_tfidf_embeddings()

        logger.info(f"Computing Sentence-BERT embeddings using {model_name}...")
        logger.info("This may take a few minutes...")

        model = SentenceTransformer(model_name)
        self.embeddings = model.encode(
            self.summaries,
            show_progress_bar=True,
            convert_to_numpy=True,
            batch_size=64
        )
        self.embedding_method = f'SBERT ({model_name})'

        logger.info(f"SBERT embeddings shape: {self.embeddings.shape}")
        return self.embeddings

    def reduce_dimensions(self, method: str = 'umap', n_components: int = 2) -> np.ndarray:
        """Reduce embedding dimensions for visualization."""
        logger.info(f"Reducing dimensions using {method.upper()}...")

        # First reduce to 50 dimensions with PCA if needed
        if self.embeddings.shape[1] > 50:
            pca = PCA(n_components=50, random_state=42)
            embeddings_reduced = pca.fit_transform(self.embeddings)
        else:
            embeddings_reduced = self.embeddings

        if method == 'umap' and HAS_UMAP:
            reducer = umap.UMAP(
                n_components=n_components,
                n_neighbors=15,
                min_dist=0.1,
                metric='cosine',
                random_state=42
            )
            self.embeddings_2d = reducer.fit_transform(embeddings_reduced)
        else:
            tsne = TSNE(
                n_components=n_components,
                perplexity=min(30, len(self.summaries) - 1),
                random_state=42,
                n_iter=1000
            )
            self.embeddings_2d = tsne.fit_transform(embeddings_reduced)

        logger.info(f"Reduced dimensions: {self.embeddings_2d.shape}")
        return self.embeddings_2d

    # =========================================================================
    # Clustering Algorithms
    # =========================================================================

    def cluster_kmeans(self, n_clusters: int = None) -> np.ndarray:
        """K-Means clustering."""
        n_clusters = n_clusters or self.n_clusters
        logger.info(f"Running K-Means with K={n_clusters}...")

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(self.embeddings)

        self.cluster_results['kmeans'] = {
            'labels': labels,
            'n_clusters': n_clusters,
            'silhouette': silhouette_score(self.embeddings, labels),
            'calinski_harabasz': calinski_harabasz_score(self.embeddings, labels),
            'davies_bouldin': davies_bouldin_score(self.embeddings, labels)
        }
        return labels

    def cluster_kmeans_cosine(self, n_clusters: int = None) -> np.ndarray:
        """Spherical K-Means (K-Means with cosine distance via normalization)."""
        n_clusters = n_clusters or self.n_clusters
        logger.info(f"Running Spherical K-Means (cosine) with K={n_clusters}...")

        # Normalize embeddings for cosine similarity
        embeddings_normalized = normalize(self.embeddings, norm='l2')

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings_normalized)

        self.cluster_results['kmeans_cosine'] = {
            'labels': labels,
            'n_clusters': n_clusters,
            'silhouette': silhouette_score(embeddings_normalized, labels),
            'calinski_harabasz': calinski_harabasz_score(embeddings_normalized, labels),
            'davies_bouldin': davies_bouldin_score(embeddings_normalized, labels)
        }
        return labels

    def cluster_spectral(self, n_clusters: int = None) -> np.ndarray:
        """Spectral Clustering."""
        n_clusters = n_clusters or self.n_clusters
        logger.info(f"Running Spectral Clustering with K={n_clusters}...")

        # Use a subset if data is too large (spectral clustering is memory-intensive)
        if len(self.summaries) > 5000:
            logger.warning("Data too large for full spectral clustering, using nearest neighbors affinity")
            spectral = SpectralClustering(
                n_clusters=n_clusters,
                affinity='nearest_neighbors',
                n_neighbors=10,
                random_state=42,
                n_jobs=-1
            )
        else:
            spectral = SpectralClustering(
                n_clusters=n_clusters,
                affinity='rbf',
                random_state=42,
                n_jobs=-1
            )

        labels = spectral.fit_predict(self.embeddings)

        self.cluster_results['spectral'] = {
            'labels': labels,
            'n_clusters': n_clusters,
            'silhouette': silhouette_score(self.embeddings, labels),
            'calinski_harabasz': calinski_harabasz_score(self.embeddings, labels),
            'davies_bouldin': davies_bouldin_score(self.embeddings, labels)
        }
        return labels

    def cluster_agglomerative(self, n_clusters: int = None) -> np.ndarray:
        """Agglomerative (Hierarchical) clustering."""
        n_clusters = n_clusters or self.n_clusters
        logger.info(f"Running Agglomerative Clustering with K={n_clusters}...")

        agg = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        labels = agg.fit_predict(self.embeddings)

        self.cluster_results['agglomerative'] = {
            'labels': labels,
            'n_clusters': n_clusters,
            'silhouette': silhouette_score(self.embeddings, labels),
            'calinski_harabasz': calinski_harabasz_score(self.embeddings, labels),
            'davies_bouldin': davies_bouldin_score(self.embeddings, labels)
        }
        return labels

    def cluster_gmm(self, n_components: int = None) -> np.ndarray:
        """Gaussian Mixture Model clustering."""
        n_components = n_components or self.n_clusters
        logger.info(f"Running GMM with {n_components} components...")

        gmm = GaussianMixture(n_components=n_components, random_state=42, covariance_type='full')
        labels = gmm.fit_predict(self.embeddings)

        self.cluster_results['gmm'] = {
            'labels': labels,
            'n_clusters': n_components,
            'silhouette': silhouette_score(self.embeddings, labels),
            'bic': gmm.bic(self.embeddings),
            'aic': gmm.aic(self.embeddings)
        }
        return labels

    # =========================================================================
    # Visualization
    # =========================================================================

    def plot_clusters(self, labels: np.ndarray, method_name: str) -> None:
        """Create publication-quality cluster visualization."""
        if self.embeddings_2d is None:
            self.reduce_dimensions()

        fig, ax = plt.subplots(figsize=(10, 8))

        unique_labels = sorted(set(labels))
        n_clusters = len(unique_labels)

        for i, label in enumerate(unique_labels):
            mask = labels == label
            color = CLUSTER_COLORS[label % 20]
            ax.scatter(
                self.embeddings_2d[mask, 0],
                self.embeddings_2d[mask, 1],
                c=[color],
                marker='o',
                s=50,
                alpha=0.7,
                edgecolors='white',
                linewidth=0.5,
                label=f'Cluster {label}'
            )

        ax.set_xlabel('Dimension 1', fontsize=14, fontweight='bold')
        ax.set_ylabel('Dimension 2', fontsize=14, fontweight='bold')
        ax.set_title(f'{method_name} Clustering ({n_clusters} clusters)', fontsize=16, fontweight='bold')

        if n_clusters <= 15:
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        output_path = self.output_dir / f'cluster_visualization_{method_name.lower().replace(" ", "_")}.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        logger.info(f"Saved cluster visualization to {output_path}")

    def plot_metrics_comparison(self) -> None:
        """Plot comparison of clustering metrics across methods."""
        methods = []
        silhouettes = []
        n_clusters_list = []

        for method, results in self.cluster_results.items():
            if results.get('silhouette') is not None:
                methods.append(method.upper().replace('_', '\n'))
                silhouettes.append(results['silhouette'])
                n_clusters_list.append(results.get('n_clusters', 0))

        if len(methods) < 2:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Color
        bar_color = '#1A5276'

        # Silhouette scores
        bars1 = ax1.bar(methods, silhouettes, color=bar_color, edgecolor='white', linewidth=0.8)
        ax1.set_ylabel('Silhouette Score', fontsize=14, fontweight='bold')
        ax1.set_title('Clustering Quality Comparison', fontsize=16, fontweight='bold')
        ax1.set_ylim(0, max(silhouettes) * 1.3)

        for bar, val in zip(bars1, silhouettes):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=11, fontweight='medium')

        # Number of clusters
        bars2 = ax2.bar(methods, n_clusters_list, color=bar_color, edgecolor='white', linewidth=0.8)
        ax2.set_ylabel('Number of Clusters', fontsize=14, fontweight='bold')
        ax2.set_title('Number of Clusters by Method', fontsize=16, fontweight='bold')

        for bar, val in zip(bars2, n_clusters_list):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     str(val), ha='center', va='bottom', fontsize=11, fontweight='medium')

        for ax in [ax1, ax2]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.grid(True, linestyle='--', alpha=0.4)
            ax.tick_params(axis='x', labelsize=10)
            ax.tick_params(axis='y', labelsize=11)

        plt.tight_layout()
        fig.savefig(self.output_dir / 'clustering_metrics_comparison.pdf', dpi=300, bbox_inches='tight')
        plt.close()

        logger.info("Saved clustering metrics comparison plot")

    def plot_all_methods_comparison(self) -> None:
        """Create comparison plot of all clustering methods."""
        methods = [m for m in self.cluster_results.keys() if self.cluster_results[m].get('labels') is not None]

        if len(methods) < 2:
            return

        n_methods = len(methods)
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        axes = axes.flatten()

        for idx, method in enumerate(methods):
            if idx >= 6:
                break
            ax = axes[idx]
            labels = self.cluster_results[method]['labels']
            unique_labels = sorted(set(labels))

            for label in unique_labels:
                mask = labels == label
                color = CLUSTER_COLORS[label % 20]
                ax.scatter(
                    self.embeddings_2d[mask, 0],
                    self.embeddings_2d[mask, 1],
                    c=[color], s=20, alpha=0.7
                )

            n_clusters = self.cluster_results[method].get('n_clusters', len(set(labels)))
            silhouette = self.cluster_results[method].get('silhouette')
            sil_str = f"Sil={silhouette:.3f}" if silhouette else ""

            ax.set_title(f'{method.upper()}\n({n_clusters} clusters, {sil_str})', fontsize=12, fontweight='bold')
            ax.set_xlabel('Dim 1', fontsize=10)
            ax.set_ylabel('Dim 2', fontsize=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        # Hide unused subplots
        for idx in range(len(methods), 6):
            axes[idx].set_visible(False)

        plt.tight_layout()
        fig.savefig(self.output_dir / 'clustering_methods_comparison.pdf', dpi=300, bbox_inches='tight')
        plt.close()

        logger.info("Saved clustering methods comparison plot")

    # =========================================================================
    # Main Pipeline
    # =========================================================================

    def run(self, embedding_method: str = 'sbert', single_behavior_only: bool = True) -> None:
        """Run the complete clustering pipeline."""
        # Collect data
        if self.collect_data(single_behavior_only=single_behavior_only) == 0:
            logger.error("No data collected. Exiting.")
            return

        # Compute embeddings
        if embedding_method == 'sbert' and HAS_SBERT:
            self.compute_sbert_embeddings()
        else:
            self.compute_tfidf_embeddings()

        # Reduce dimensions for visualization
        dim_method = 'umap' if HAS_UMAP else 'tsne'
        self.reduce_dimensions(method=dim_method)

        # Run all clustering methods
        logger.info("Running clustering algorithms...")

        # K-Means
        labels_kmeans = self.cluster_kmeans()
        self.plot_clusters(labels_kmeans, 'K-Means')

        # Spherical K-Means (cosine)
        labels_kmeans_cos = self.cluster_kmeans_cosine()
        self.plot_clusters(labels_kmeans_cos, 'K-Means Cosine')

        # Spectral
        labels_spectral = self.cluster_spectral()
        self.plot_clusters(labels_spectral, 'Spectral')

        # Agglomerative
        labels_agg = self.cluster_agglomerative()
        self.plot_clusters(labels_agg, 'Agglomerative')

        # GMM
        labels_gmm = self.cluster_gmm()
        self.plot_clusters(labels_gmm, 'GMM')

        # Comparison plots
        self.plot_all_methods_comparison()
        self.plot_metrics_comparison()

        # Print summary
        self.print_summary()

    def print_summary(self) -> None:
        """Print summary to console."""
        print("\n" + "=" * 70)
        print("BEHAVIOR SUMMARY CLUSTERING V2 - RESULTS")
        print("=" * 70)
        print(f"\nData:")
        print(f"  Total summaries: {self.all_summaries_count}")
        print(f"  Single-behavior summaries: {self.filtered_summaries_count} ({self.filtered_summaries_count/self.all_summaries_count*100:.1f}%)")
        print(f"  Embedding method: {self.embedding_method}")
        print(f"\nClustering Results (K={self.n_clusters}):")
        print("-" * 50)

        # Sort by silhouette score
        sorted_results = sorted(
            self.cluster_results.items(),
            key=lambda x: x[1].get('silhouette', 0),
            reverse=True
        )

        for method, results in sorted_results:
            n_clusters = results.get('n_clusters', 'N/A')
            silhouette = results.get('silhouette')
            sil_str = f"{silhouette:.4f}" if silhouette else "N/A"
            ch = results.get('calinski_harabasz')
            ch_str = f"{ch:.1f}" if ch else "N/A"
            print(f"  {method.upper():20s} | Silhouette: {sil_str} | Calinski-Harabasz: {ch_str}")

        print(f"\nResults saved to: {self.output_dir}")

        # Best method
        if sorted_results:
            best_method = sorted_results[0][0]
            best_score = sorted_results[0][1].get('silhouette', 0)
            print(f"\n*** Best method: {best_method.upper()} (Silhouette: {best_score:.4f}) ***")


# =============================================================================
# Entry Point
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Improved clustering of behavior summaries (V2)"
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
        "--embedding", "-e",
        choices=['tfidf', 'sbert'],
        default='sbert',
        help="Embedding method (default: sbert)"
    )
    parser.add_argument(
        "--clusters", "-k",
        type=int,
        default=15,
        help="Number of clusters (default: 15)"
    )
    parser.add_argument(
        "--all-snippets",
        action="store_true",
        help="Use all snippets instead of single-behavior only"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    clusterer = BehaviorSummaryClustererV2(args.input, args.output, n_clusters=args.clusters)
    clusterer.run(
        embedding_method=args.embedding,
        single_behavior_only=not args.all_snippets
    )


if __name__ == "__main__":
    main()
