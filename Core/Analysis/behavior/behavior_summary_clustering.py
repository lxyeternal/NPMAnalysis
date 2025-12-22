#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Behavior Summary Clustering

Cluster behavior_summary texts from malware snippets using multiple algorithms.
Generates publication-quality visualizations and cluster analysis.

Embedding Methods:
    - TF-IDF (default, no GPU required)
    - Sentence-BERT (if sentence-transformers installed)
    - Doc2Vec

Clustering Algorithms:
    - K-Means
    - DBSCAN
    - HDBSCAN (if hdbscan installed)
    - Agglomerative Clustering
    - Gaussian Mixture Model (GMM)

Output:
    - results/behavior_summary_clustering/
        - optimal_k_analysis.pdf: Elbow and silhouette analysis
        - cluster_visualization_{method}.pdf: Cluster visualization for each method
        - clustering_methods_comparison.pdf: Side-by-side comparison
        - clustering_metrics_comparison.pdf: Metrics comparison chart
"""

import os
import json
import glob
import re
import warnings
import logging
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from tqdm import tqdm

# Scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler

# Suppress warnings
warnings.filterwarnings('ignore')

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

DEFAULT_INPUT_DIR = PROJECT_ROOT / "Core" / "Analysis" / "code_snipptes" / "malware_snippets"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "results" / "behavior_summary_clustering"

# Matplotlib configuration for publication quality
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 11
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['figure.dpi'] = 300

# Color palettes
CLUSTER_COLORS = plt.cm.tab20(np.linspace(0, 1, 20))


# =============================================================================
# Optional imports
# =============================================================================

# Try to import optional dependencies
try:
    import hdbscan
    HAS_HDBSCAN = True
except ImportError:
    HAS_HDBSCAN = False
    logger.info("HDBSCAN not installed. Skipping HDBSCAN clustering.")

try:
    from sentence_transformers import SentenceTransformer
    HAS_SBERT = True
except ImportError:
    HAS_SBERT = False
    logger.info("sentence-transformers not installed. Using TF-IDF instead.")

try:
    import umap
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False
    logger.info("UMAP not installed. Using t-SNE for visualization.")


# =============================================================================
# Data Collection
# =============================================================================

class BehaviorSummaryClusterer:
    """Cluster behavior summaries using multiple algorithms."""

    def __init__(self, input_dir: Path = None, output_dir: Path = None):
        self.input_dir = Path(input_dir or DEFAULT_INPUT_DIR)
        self.output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Data storage
        self.summaries = []  # List of behavior_summary texts
        self.metadata = []   # Corresponding metadata

        # Embeddings
        self.embeddings = None
        self.embeddings_2d = None
        self.embedding_method = None

        # Clustering results
        self.cluster_results = {}

    def collect_data(self) -> int:
        """Collect behavior_summary texts from result.json files."""
        logger.info(f"Collecting data from {self.input_dir}")

        json_files = list(self.input_dir.glob("**/result.json"))
        logger.info(f"Found {len(json_files)} result.json files")

        for json_path in tqdm(json_files, desc="Collecting summaries"):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                metadata = data.get('metadata', {})
                package_name = metadata.get('package_name', 'unknown')
                version = metadata.get('version', 'unknown')

                for snippet in data.get('malicious_snippets', []):
                    summary = snippet.get('behavior_summary', '')
                    if summary and len(summary.strip()) > 10:  # Filter very short summaries
                        self.summaries.append(summary.strip())
                        self.metadata.append({
                            'package': package_name,
                            'version': version,
                            'file': snippet.get('file', ''),
                            'type': snippet.get('type', ''),
                            'behaviors': snippet.get('validate_behavior_formal', [])
                        })

            except Exception as e:
                logger.error(f"Error processing {json_path}: {e}")

        logger.info(f"Collected {len(self.summaries)} behavior summaries")
        return len(self.summaries)

    # =========================================================================
    # Text Preprocessing
    # =========================================================================

    @staticmethod
    def preprocess_text(text: str) -> str:
        """Clean and preprocess text."""
        # Lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    # =========================================================================
    # Embedding Methods
    # =========================================================================

    def compute_tfidf_embeddings(self) -> np.ndarray:
        """Compute TF-IDF embeddings."""
        logger.info("Computing TF-IDF embeddings...")

        # Preprocess texts
        processed_texts = [self.preprocess_text(s) for s in self.summaries]

        # TF-IDF vectorization
        vectorizer = TfidfVectorizer(
            max_features=1000,
            min_df=2,
            max_df=0.95,
            ngram_range=(1, 2),
            stop_words='english'
        )

        self.embeddings = vectorizer.fit_transform(processed_texts).toarray()
        self.embedding_method = 'TF-IDF'

        logger.info(f"TF-IDF embeddings shape: {self.embeddings.shape}")
        return self.embeddings

    def compute_sbert_embeddings(self, model_name: str = 'all-MiniLM-L6-v2') -> np.ndarray:
        """Compute Sentence-BERT embeddings."""
        if not HAS_SBERT:
            logger.warning("sentence-transformers not available. Using TF-IDF.")
            return self.compute_tfidf_embeddings()

        logger.info(f"Computing Sentence-BERT embeddings using {model_name}...")

        model = SentenceTransformer(model_name)
        self.embeddings = model.encode(
            self.summaries,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        self.embedding_method = 'SBERT'

        logger.info(f"SBERT embeddings shape: {self.embeddings.shape}")
        return self.embeddings

    def reduce_dimensions(self, method: str = 'tsne', n_components: int = 2) -> np.ndarray:
        """Reduce embedding dimensions for visualization."""
        logger.info(f"Reducing dimensions using {method.upper()}...")

        # First reduce to 50 dimensions with PCA if needed
        if self.embeddings.shape[1] > 50:
            pca = PCA(n_components=50, random_state=42)
            embeddings_pca = pca.fit_transform(self.embeddings)
        else:
            embeddings_pca = self.embeddings

        if method == 'umap' and HAS_UMAP:
            reducer = umap.UMAP(
                n_components=n_components,
                n_neighbors=15,
                min_dist=0.1,
                metric='cosine',
                random_state=42
            )
            self.embeddings_2d = reducer.fit_transform(embeddings_pca)
        else:
            tsne = TSNE(
                n_components=n_components,
                perplexity=min(30, len(self.summaries) - 1),
                random_state=42,
                n_iter=1000
            )
            self.embeddings_2d = tsne.fit_transform(embeddings_pca)

        logger.info(f"Reduced dimensions: {self.embeddings_2d.shape}")
        return self.embeddings_2d

    # =========================================================================
    # Clustering Algorithms
    # =========================================================================

    def find_optimal_k(self, max_k: int = 15) -> int:
        """Find optimal number of clusters using elbow method and silhouette score."""
        logger.info(f"Finding optimal K (2-{max_k})...")

        k_range = range(2, min(max_k + 1, len(self.summaries) // 10))
        inertias = []
        silhouette_scores = []

        for k in tqdm(k_range, desc="Testing K values"):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(self.embeddings)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(self.embeddings, labels))

        # Plot elbow curve
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        ax1.plot(list(k_range), inertias, 'bo-', linewidth=2, markersize=6)
        ax1.set_xlabel('Number of Clusters (K)', fontsize=11)
        ax1.set_ylabel('Inertia', fontsize=11)
        ax1.set_title('Elbow Method', fontsize=12, fontweight='bold')
        ax1.grid(True, linestyle='--', alpha=0.3)

        ax2.plot(list(k_range), silhouette_scores, 'ro-', linewidth=2, markersize=6)
        ax2.set_xlabel('Number of Clusters (K)', fontsize=11)
        ax2.set_ylabel('Silhouette Score', fontsize=11)
        ax2.set_title('Silhouette Analysis', fontsize=12, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout()
        fig.savefig(self.output_dir / 'optimal_k_analysis.pdf', dpi=300, bbox_inches='tight')
        plt.close()

        # Find optimal K
        optimal_k = list(k_range)[np.argmax(silhouette_scores)]
        logger.info(f"Optimal K: {optimal_k} (silhouette: {max(silhouette_scores):.4f})")

        return optimal_k

    def cluster_kmeans(self, n_clusters: int) -> np.ndarray:
        """K-Means clustering."""
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

    def cluster_dbscan(self, eps: float = 0.5, min_samples: int = 5) -> np.ndarray:
        """DBSCAN clustering."""
        logger.info(f"Running DBSCAN (eps={eps}, min_samples={min_samples})...")

        # Normalize embeddings for DBSCAN
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(self.embeddings)

        # Try different eps values
        best_labels = None
        best_silhouette = -1
        best_eps = eps

        for test_eps in [0.3, 0.5, 0.7, 1.0, 1.5]:
            dbscan = DBSCAN(eps=test_eps, min_samples=min_samples)
            labels = dbscan.fit_predict(embeddings_scaled)

            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            if n_clusters >= 2:
                # Only calculate silhouette for non-noise points
                mask = labels != -1
                if sum(mask) > n_clusters:
                    score = silhouette_score(embeddings_scaled[mask], labels[mask])
                    if score > best_silhouette:
                        best_silhouette = score
                        best_labels = labels
                        best_eps = test_eps

        if best_labels is None:
            logger.warning("DBSCAN could not find valid clusters. Using default eps.")
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            best_labels = dbscan.fit_predict(embeddings_scaled)

        n_clusters = len(set(best_labels)) - (1 if -1 in best_labels else 0)
        noise_count = sum(best_labels == -1)

        self.cluster_results['dbscan'] = {
            'labels': best_labels,
            'n_clusters': n_clusters,
            'noise_points': noise_count,
            'eps': best_eps,
            'silhouette': best_silhouette if best_silhouette > -1 else None
        }
        logger.info(f"DBSCAN found {n_clusters} clusters, {noise_count} noise points")
        return best_labels

    def cluster_hdbscan(self, min_cluster_size: int = 10) -> Optional[np.ndarray]:
        """HDBSCAN clustering."""
        if not HAS_HDBSCAN:
            logger.warning("HDBSCAN not available. Skipping.")
            return None

        logger.info(f"Running HDBSCAN (min_cluster_size={min_cluster_size})...")

        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            metric='euclidean',
            cluster_selection_method='eom'
        )
        labels = clusterer.fit_predict(self.embeddings)

        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        noise_count = sum(labels == -1)

        silhouette = None
        if n_clusters >= 2:
            mask = labels != -1
            if sum(mask) > n_clusters:
                silhouette = silhouette_score(self.embeddings[mask], labels[mask])

        self.cluster_results['hdbscan'] = {
            'labels': labels,
            'n_clusters': n_clusters,
            'noise_points': noise_count,
            'silhouette': silhouette
        }
        logger.info(f"HDBSCAN found {n_clusters} clusters, {noise_count} noise points")
        return labels

    def cluster_agglomerative(self, n_clusters: int) -> np.ndarray:
        """Agglomerative (Hierarchical) clustering."""
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

    def cluster_gmm(self, n_components: int) -> np.ndarray:
        """Gaussian Mixture Model clustering."""
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
        n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)

        # Plot each cluster
        for i, label in enumerate(unique_labels):
            mask = labels == label
            if label == -1:
                # Noise points
                ax.scatter(
                    self.embeddings_2d[mask, 0],
                    self.embeddings_2d[mask, 1],
                    c='lightgray',
                    marker='x',
                    s=30,
                    alpha=0.5,
                    label='Noise'
                )
            else:
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

        ax.set_xlabel('Dimension 1', fontsize=11)
        ax.set_ylabel('Dimension 2', fontsize=11)
        ax.set_title(f'{method_name} Clustering ({n_clusters} clusters)', fontsize=14, fontweight='bold')

        # Add legend if not too many clusters
        if n_clusters <= 15:
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()

        output_path = self.output_dir / f'cluster_visualization_{method_name.lower().replace(" ", "_")}.pdf'
        fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        logger.info(f"Saved cluster visualization to {output_path}")

    def plot_all_methods_comparison(self) -> None:
        """Create comparison plot of all clustering methods."""
        methods = [m for m in self.cluster_results.keys() if self.cluster_results[m].get('labels') is not None]

        if len(methods) < 2:
            return

        n_methods = len(methods)
        fig, axes = plt.subplots(1, n_methods, figsize=(5 * n_methods, 5))

        if n_methods == 1:
            axes = [axes]

        for ax, method in zip(axes, methods):
            labels = self.cluster_results[method]['labels']
            unique_labels = sorted(set(labels))

            for label in unique_labels:
                mask = labels == label
                if label == -1:
                    ax.scatter(
                        self.embeddings_2d[mask, 0],
                        self.embeddings_2d[mask, 1],
                        c='lightgray', marker='x', s=20, alpha=0.5
                    )
                else:
                    color = CLUSTER_COLORS[label % 20]
                    ax.scatter(
                        self.embeddings_2d[mask, 0],
                        self.embeddings_2d[mask, 1],
                        c=[color], s=30, alpha=0.7
                    )

            n_clusters = self.cluster_results[method].get('n_clusters', len(set(labels)))
            silhouette = self.cluster_results[method].get('silhouette')
            sil_str = f", Sil={silhouette:.3f}" if silhouette else ""

            ax.set_title(f'{method.upper()}\n({n_clusters} clusters{sil_str})', fontsize=11, fontweight='bold')
            ax.set_xlabel('Dim 1', fontsize=9)
            ax.set_ylabel('Dim 2', fontsize=9)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        plt.tight_layout()
        fig.savefig(self.output_dir / 'clustering_methods_comparison.pdf', dpi=300, bbox_inches='tight')
        plt.close()

        logger.info("Saved clustering methods comparison plot")

    def plot_metrics_comparison(self) -> None:
        """Plot comparison of clustering metrics across methods."""
        methods = []
        silhouettes = []
        n_clusters_list = []

        for method, results in self.cluster_results.items():
            if results.get('silhouette') is not None:
                methods.append(method.upper())
                silhouettes.append(results['silhouette'])
                n_clusters_list.append(results.get('n_clusters', 0))

        if len(methods) < 2:
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Silhouette scores
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(methods)))
        bars1 = ax1.bar(methods, silhouettes, color=colors, edgecolor='black', linewidth=0.5)
        ax1.set_ylabel('Silhouette Score', fontsize=11)
        ax1.set_title('Clustering Quality Comparison', fontsize=12, fontweight='bold')
        ax1.set_ylim(0, max(silhouettes) * 1.2)

        for bar, val in zip(bars1, silhouettes):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{val:.3f}', ha='center', va='bottom', fontsize=9)

        # Number of clusters
        bars2 = ax2.bar(methods, n_clusters_list, color=colors, edgecolor='black', linewidth=0.5)
        ax2.set_ylabel('Number of Clusters', fontsize=11)
        ax2.set_title('Number of Clusters by Method', fontsize=12, fontweight='bold')

        for bar, val in zip(bars2, n_clusters_list):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     str(val), ha='center', va='bottom', fontsize=9)

        for ax in [ax1, ax2]:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.yaxis.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout()
        fig.savefig(self.output_dir / 'clustering_metrics_comparison.pdf', dpi=300, bbox_inches='tight')
        plt.close()

        logger.info("Saved clustering metrics comparison plot")

    # =========================================================================
    # Cluster Analysis
    # =========================================================================

    def analyze_clusters(self, labels: np.ndarray, method_name: str) -> dict:
        """Analyze cluster contents and extract key features."""
        analysis = {
            'method': method_name,
            'n_clusters': len(set(labels)) - (1 if -1 in labels else 0),
            'clusters': {}
        }

        unique_labels = sorted(set(labels))

        for label in unique_labels:
            if label == -1:
                continue

            mask = labels == label
            cluster_summaries = [self.summaries[i] for i in range(len(self.summaries)) if mask[i]]
            cluster_metadata = [self.metadata[i] for i in range(len(self.metadata)) if mask[i]]

            # Extract common words
            all_words = []
            for summary in cluster_summaries:
                words = self.preprocess_text(summary).split()
                all_words.extend(words)

            word_freq = Counter(all_words)
            # Filter common stop words
            stop_words = {'the', 'a', 'an', 'to', 'of', 'in', 'for', 'and', 'or', 'is', 'it', 'this', 'that', 'with', 'from', 'as', 'on', 'by', 'at'}
            top_words = [(w, c) for w, c in word_freq.most_common(20) if w not in stop_words][:10]

            # Get behavior types
            behavior_counter = Counter()
            for meta in cluster_metadata:
                for behavior in meta.get('behaviors', []):
                    behavior_counter[behavior] += 1

            analysis['clusters'][int(label)] = {
                'size': int(sum(mask)),
                'percentage': float(sum(mask) / len(labels) * 100),
                'top_words': top_words,
                'top_behaviors': behavior_counter.most_common(5),
                'example_summaries': cluster_summaries[:3]
            }

        return analysis

    def save_results(self) -> None:
        """Print clustering results summary (PDF-only output mode)."""
        logger.info(f"Results saved to {self.output_dir}")

    # =========================================================================
    # Main Pipeline
    # =========================================================================

    def run(self, embedding_method: str = 'tfidf') -> None:
        """Run the complete clustering pipeline."""
        # Collect data
        if self.collect_data() == 0:
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

        # Find optimal K
        optimal_k = self.find_optimal_k()

        # Run all clustering methods
        logger.info("Running clustering algorithms...")

        # K-Means
        labels_kmeans = self.cluster_kmeans(optimal_k)
        self.plot_clusters(labels_kmeans, 'K-Means')

        # DBSCAN
        labels_dbscan = self.cluster_dbscan()
        self.plot_clusters(labels_dbscan, 'DBSCAN')

        # HDBSCAN
        if HAS_HDBSCAN:
            labels_hdbscan = self.cluster_hdbscan()
            if labels_hdbscan is not None:
                self.plot_clusters(labels_hdbscan, 'HDBSCAN')

        # Agglomerative
        labels_agg = self.cluster_agglomerative(optimal_k)
        self.plot_clusters(labels_agg, 'Agglomerative')

        # GMM
        labels_gmm = self.cluster_gmm(optimal_k)
        self.plot_clusters(labels_gmm, 'GMM')

        # Comparison plots
        self.plot_all_methods_comparison()
        self.plot_metrics_comparison()

        # Save results
        self.save_results()

        # Print summary
        self.print_summary()

    def print_summary(self) -> None:
        """Print summary to console."""
        print("\n" + "=" * 60)
        print("BEHAVIOR SUMMARY CLUSTERING COMPLETE")
        print("=" * 60)
        print(f"\nTotal summaries: {len(self.summaries)}")
        print(f"Embedding method: {self.embedding_method}")
        print(f"\nClustering Results:")
        print("-" * 40)

        for method, results in self.cluster_results.items():
            n_clusters = results.get('n_clusters', 'N/A')
            silhouette = results.get('silhouette')
            sil_str = f"{silhouette:.4f}" if silhouette else "N/A"
            noise = results.get('noise_points', 0)
            print(f"  {method.upper():15s} | Clusters: {n_clusters:3} | Silhouette: {sil_str} | Noise: {noise}")

        print(f"\nResults saved to: {self.output_dir}")


# =============================================================================
# Entry Point
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Cluster behavior summaries from malware snippets"
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
        default='tfidf',
        help="Embedding method (default: tfidf)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    clusterer = BehaviorSummaryClusterer(args.input, args.output)
    clusterer.run(embedding_method=args.embedding)


if __name__ == "__main__":
    main()
