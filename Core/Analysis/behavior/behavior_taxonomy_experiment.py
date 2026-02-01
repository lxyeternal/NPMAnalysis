#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Behavior Taxonomy Experiment

Systematically test clustering algorithms with k=3..10 on behavior_summary data.
- Algorithms: KMeans, KMeans-Cosine, Spectral, Agglomerative, GMM
- Metrics: Silhouette, Calinski-Harabasz, Davies-Bouldin
- Output: metrics table + top keywords per cluster for best configs
"""

import json
import warnings
import logging
from pathlib import Path
from collections import Counter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from tqdm import tqdm

from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import TfidfVectorizer

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parents[2]
INPUT_DIR = PROJECT_ROOT / "Core" / "Analysis" / "code_snipptes" / "malware_snippets"
OUTPUT_DIR = SCRIPT_DIR / "results" / "taxonomy_experiment"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['font.size'] = 12
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['figure.dpi'] = 300


def collect_data(input_dir, single_behavior_only=True):
    """Collect behavior_summary texts."""
    json_files = list(input_dir.glob("**/result.json"))
    logger.info(f"Found {len(json_files)} result.json files")

    summaries = []
    behavior_labels = []

    for json_path in tqdm(json_files, desc="Collecting"):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for snippet in data.get('malicious_snippets', []):
                summary = snippet.get('behavior_summary', '')
                behaviors = snippet.get('validate_behavior_formal', [])
                if not summary or len(summary.strip()) < 10:
                    continue
                if single_behavior_only and len(behaviors) != 1:
                    continue
                summaries.append(summary.strip())
                behavior_labels.append(behaviors[0] if behaviors else 'unknown')
        except:
            pass

    logger.info(f"Collected {len(summaries)} summaries")
    return summaries, behavior_labels


def compute_embeddings(summaries):
    """Compute SBERT embeddings."""
    try:
        from sentence_transformers import SentenceTransformer
        logger.info("Computing SBERT embeddings...")
        model = SentenceTransformer('all-mpnet-base-v2')
        embeddings = model.encode(summaries, show_progress_bar=True, batch_size=64)
        return embeddings, 'SBERT'
    except ImportError:
        logger.warning("SBERT not available, using TF-IDF")
        vectorizer = TfidfVectorizer(max_features=1000, min_df=2, max_df=0.95,
                                      ngram_range=(1, 2), stop_words='english')
        embeddings = vectorizer.fit_transform(summaries).toarray()
        return embeddings, 'TF-IDF'


def run_clustering(embeddings, algorithm, k):
    """Run a single clustering algorithm with given k."""
    embeddings_norm = normalize(embeddings, norm='l2')

    if algorithm == 'kmeans':
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(embeddings)
    elif algorithm == 'kmeans_cosine':
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(embeddings_norm)
    elif algorithm == 'spectral':
        model = SpectralClustering(n_clusters=k, affinity='nearest_neighbors',
                                    n_neighbors=10, random_state=42, n_jobs=-1)
        labels = model.fit_predict(embeddings)
    elif algorithm == 'agglomerative':
        model = AgglomerativeClustering(n_clusters=k, linkage='ward')
        labels = model.fit_predict(embeddings)
    elif algorithm == 'gmm':
        model = GaussianMixture(n_components=k, random_state=42, covariance_type='full')
        labels = model.fit_predict(embeddings)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    # Use normalized embeddings for cosine variant metrics
    emb_for_metrics = embeddings_norm if algorithm == 'kmeans_cosine' else embeddings

    sil = silhouette_score(emb_for_metrics, labels)
    ch = calinski_harabasz_score(emb_for_metrics, labels)
    db = davies_bouldin_score(emb_for_metrics, labels)

    return labels, sil, ch, db


def get_cluster_keywords(summaries, labels, k, top_n=8):
    """Extract top TF-IDF keywords per cluster."""
    cluster_docs = {}
    for i in range(k):
        mask = labels == i
        cluster_docs[i] = ' '.join([summaries[j] for j in range(len(summaries)) if mask[j]])

    vectorizer = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([cluster_docs[i] for i in range(k)])
    feature_names = vectorizer.get_feature_names_out()

    keywords = {}
    for i in range(k):
        scores = tfidf_matrix[i].toarray().flatten()
        top_indices = scores.argsort()[-top_n:][::-1]
        keywords[i] = [(feature_names[idx], scores[idx]) for idx in top_indices]

    return keywords


def plot_metrics(all_results, output_dir):
    """Plot metrics comparison across algorithms and k values."""
    algorithms = ['kmeans', 'kmeans_cosine', 'spectral', 'agglomerative', 'gmm']
    algo_labels = ['KMeans', 'KMeans\n(Cosine)', 'Spectral', 'Agglom.', 'GMM']
    k_values = sorted(set(r['k'] for r in all_results))

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    metrics = [('silhouette', 'Silhouette Score (higher=better)'),
               ('calinski_harabasz', 'Calinski-Harabasz (higher=better)'),
               ('davies_bouldin', 'Davies-Bouldin (lower=better)')]

    colors = plt.cm.tab10(np.linspace(0, 1, len(algorithms)))

    for ax, (metric, title) in zip(axes, metrics):
        for algo_idx, algo in enumerate(algorithms):
            algo_data = [r for r in all_results if r['algorithm'] == algo]
            ks = [r['k'] for r in algo_data]
            vals = [r[metric] for r in algo_data]
            ax.plot(ks, vals, 'o-', color=colors[algo_idx], label=algo_labels[algo_idx],
                    linewidth=2, markersize=6)

        ax.set_xlabel('Number of Clusters (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel(title, fontsize=11, fontweight='bold')
        ax.set_xticks(k_values)
        ax.legend(fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
    fig.savefig(output_dir / 'metrics_comparison.pdf', dpi=300, bbox_inches='tight')
    plt.close()
    logger.info("Saved metrics_comparison.pdf")


def plot_best_clusters(embeddings, summaries, best_result, output_dir):
    """Visualize the best clustering result."""
    logger.info("Reducing dimensions for visualization...")
    pca = PCA(n_components=50, random_state=42)
    emb_pca = pca.fit_transform(embeddings)
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    emb_2d = tsne.fit_transform(emb_pca)

    labels = best_result['labels']
    k = best_result['k']
    algo = best_result['algorithm']

    fig, ax = plt.subplots(figsize=(10, 8))
    cluster_colors = plt.cm.tab20(np.linspace(0, 1, 20))

    for label in sorted(set(labels)):
        mask = labels == label
        color = cluster_colors[label % 20]
        ax.scatter(emb_2d[mask, 0], emb_2d[mask, 1],
                   c=[color], s=40, alpha=0.7, edgecolors='white', linewidth=0.3,
                   label=f'Cluster {label} (n={mask.sum()})')

    ax.set_xlabel('Dimension 1', fontsize=14, fontweight='bold')
    ax.set_ylabel('Dimension 2', fontsize=14, fontweight='bold')
    ax.set_title(f'Best: {algo.upper()} k={k} (Silhouette={best_result["silhouette"]:.4f})',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    fig.savefig(output_dir / f'best_clustering_{algo}_k{k}.pdf', dpi=300, bbox_inches='tight')
    plt.close()

    return emb_2d


def main():
    # 1. Collect data
    summaries, behavior_labels = collect_data(INPUT_DIR, single_behavior_only=True)
    if not summaries:
        logger.error("No data collected")
        return

    # 2. Compute embeddings
    embeddings, emb_method = compute_embeddings(summaries)
    logger.info(f"Embeddings: {embeddings.shape}, method: {emb_method}")

    # 3. Run all algorithms × k values
    algorithms = ['kmeans', 'kmeans_cosine', 'spectral', 'agglomerative', 'gmm']
    k_values = list(range(3, 11))  # 3, 4, 5, 6, 7, 8, 9, 10

    all_results = []

    for algo in algorithms:
        for k in k_values:
            logger.info(f"Running {algo} k={k}...")
            try:
                labels, sil, ch, db = run_clustering(embeddings, algo, k)
                result = {
                    'algorithm': algo,
                    'k': k,
                    'silhouette': sil,
                    'calinski_harabasz': ch,
                    'davies_bouldin': db,
                    'labels': labels,
                }
                all_results.append(result)
                logger.info(f"  {algo} k={k}: Sil={sil:.4f}, CH={ch:.1f}, DB={db:.4f}")
            except Exception as e:
                logger.error(f"  {algo} k={k} FAILED: {e}")

    # 4. Print results table
    print("\n" + "=" * 90)
    print(f"{'Algorithm':<20} {'k':>3} {'Silhouette':>12} {'Calinski-H':>12} {'Davies-B':>12}")
    print("=" * 90)

    for r in sorted(all_results, key=lambda x: (x['algorithm'], x['k'])):
        print(f"{r['algorithm']:<20} {r['k']:>3} {r['silhouette']:>12.4f} "
              f"{r['calinski_harabasz']:>12.1f} {r['davies_bouldin']:>12.4f}")

    # 5. Find best by silhouette
    best = max(all_results, key=lambda x: x['silhouette'])
    print(f"\n*** Best by Silhouette: {best['algorithm']} k={best['k']} "
          f"(Sil={best['silhouette']:.4f}) ***")

    # 6. Plot metrics
    plot_metrics(all_results, OUTPUT_DIR)

    # 7. Visualize best result
    emb_2d = plot_best_clusters(embeddings, summaries, best, OUTPUT_DIR)

    # 8. Show cluster keywords for best result
    keywords = get_cluster_keywords(summaries, best['labels'], best['k'], top_n=10)

    print(f"\n{'=' * 90}")
    print(f"Cluster Keywords ({best['algorithm']} k={best['k']})")
    print(f"{'=' * 90}")

    for cluster_id in range(best['k']):
        mask = best['labels'] == cluster_id
        n = mask.sum()
        kw = keywords[cluster_id]
        kw_str = ', '.join([w for w, _ in kw])
        print(f"\nCluster {cluster_id} (n={n}):")
        print(f"  Keywords: {kw_str}")
        # Show 3 sample summaries
        indices = np.where(mask)[0][:3]
        for idx in indices:
            print(f"  Sample: {summaries[idx][:100]}...")

    # 9. Also show k=6 and k=7 results (close to our manual taxonomy)
    for target_k in [6, 7]:
        print(f"\n{'=' * 90}")
        print(f"Results for k={target_k} (matching our manual taxonomy)")
        print(f"{'=' * 90}")

        k_results = [r for r in all_results if r['k'] == target_k]
        k_results.sort(key=lambda x: x['silhouette'], reverse=True)

        for r in k_results:
            print(f"  {r['algorithm']:<20} Sil={r['silhouette']:.4f}, "
                  f"CH={r['calinski_harabasz']:.1f}, DB={r['davies_bouldin']:.4f}")

        # Show keywords for best k=target_k
        best_k = k_results[0]
        keywords_k = get_cluster_keywords(summaries, best_k['labels'], target_k, top_n=10)

        for cluster_id in range(target_k):
            mask = best_k['labels'] == cluster_id
            n = mask.sum()
            kw = keywords_k[cluster_id]
            kw_str = ', '.join([w for w, _ in kw])

            # Show the original behavior labels in this cluster
            cluster_behavior_labels = [behavior_labels[j] for j in range(len(behavior_labels)) if mask[j]]
            label_counts = Counter(cluster_behavior_labels).most_common(5)
            label_str = ', '.join([f"{l}({c})" for l, c in label_counts])

            print(f"\n  Cluster {cluster_id} (n={n}):")
            print(f"    Keywords: {kw_str}")
            print(f"    Top behaviors: {label_str}")

    # Save full results
    results_file = OUTPUT_DIR / 'experiment_results.txt'
    with open(results_file, 'w') as f:
        f.write(f"{'Algorithm':<20} {'k':>3} {'Silhouette':>12} {'Calinski-H':>12} {'Davies-B':>12}\n")
        f.write("=" * 65 + "\n")
        for r in sorted(all_results, key=lambda x: (x['algorithm'], x['k'])):
            f.write(f"{r['algorithm']:<20} {r['k']:>3} {r['silhouette']:>12.4f} "
                    f"{r['calinski_harabasz']:>12.1f} {r['davies_bouldin']:>12.4f}\n")

    logger.info(f"Results saved to {OUTPUT_DIR}")
    print(f"\nAll results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
