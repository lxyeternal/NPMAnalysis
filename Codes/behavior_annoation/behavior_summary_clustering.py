#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import glob
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import SpectralClustering
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.cm as cm
import pandas as pd
from tqdm import tqdm
import logging
import nltk
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import re

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 下载nltk数据
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class BehaviorSummaryClusterer:
    def __init__(self):
        self.base_dir = "/home2/wenbo/Documents/NPMAnalysis"
        self.malware_snippets_dir = os.path.join(self.base_dir, "Codes/code_snipptes/malware_snippets")
        self.package_label_dir = os.path.join(self.base_dir, "Codes/dataclean/package_label")
        self.output_dir = os.path.join(self.base_dir, "Codes/behavior_annoation/results")
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 存储所有收集到的behavior summaries
        self.summaries = []
        # 存储每个summary的元信息
        self.metadata = []
        
    def collect_from_malware_snippets(self):
        """收集malware_snippets目录下的behavior summaries"""
        logger.info("Collecting behavior summaries from malware_snippets directory...")
        
        result_files = glob.glob(f"{self.malware_snippets_dir}/**/*.json", recursive=True)
        
        for file_path in tqdm(result_files, desc="Processing malware_snippets files"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "malicious_snippets" in data:
                    for snippet in data["malicious_snippets"]:
                        if "behavior_summary" in snippet and snippet["behavior_summary"]:
                            self.summaries.append(snippet["behavior_summary"])
                            
                            # 收集元数据
                            package_name = data.get("metadata", {}).get("package_name", "unknown")
                            version = data.get("metadata", {}).get("version", "unknown")
                            file_name = snippet.get("file", "unknown")
                            type_name = snippet.get("type", "unknown")
                            
                            self.metadata.append({
                                "source": "malware_snippets",
                                "package_name": package_name,
                                "version": version,
                                "file": file_name,
                                "type": type_name,
                                "summary": snippet["behavior_summary"]
                            })
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
    
    def collect_from_package_label(self):
        """收集package_label目录下的behavior summaries"""
        logger.info("Collecting behavior summaries from package_label directory...")
        
        analysis_files = glob.glob(f"{self.package_label_dir}/**/*analysis.json", recursive=True)
        
        for file_path in tqdm(analysis_files, desc="Processing package_label files"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "behavior_summaries" in data:
                    for file_path, summary in data["behavior_summaries"].items():
                        if summary:
                            self.summaries.append(summary)
                            
                            # 收集元数据
                            package_name = data.get("package_name", "unknown")
                            version = data.get("version", "unknown")
                            
                            self.metadata.append({
                                "source": "package_label",
                                "package_name": package_name,
                                "version": version,
                                "file": file_path,
                                "type": "unknown",
                                "summary": summary
                            })
            except Exception as e:
                logger.error(f"Error processing file {file_path}: {str(e)}")
    
    def preprocess_text(self, text):
        """预处理文本，去除标点符号、数字等"""
        # 转换为小写
        text = text.lower()
        # 去除标点符号和数字
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        # 分词
        tokens = word_tokenize(text)
        # 去除停用词
        stop_words = {'the', 'a', 'an', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 
                      'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 
                      'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
                      'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 
                      'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
                      'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 
                      'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 
                      'will', 'just', 'don', 'should', 'now'}
        tokens = [token for token in tokens if token not in stop_words and len(token) > 1]
        return tokens
    
    def vectorize_word2vec(self):
        """使用Word2Vec向量化文本"""
        model_path = os.path.join(self.output_dir, 'word2vec_model.bin')
        
        # 检查是否存在已训练的模型
        if os.path.exists(model_path):
            logger.info(f"Loading existing Word2Vec model from {model_path}")
            try:
                model = Word2Vec.load(model_path)
                
                # 预处理文本
                tokenized_texts = [self.preprocess_text(summary) for summary in self.summaries]
                
                # 计算每个summary的向量表示（取词向量的平均值）
                vectors = []
                for tokens in tokenized_texts:
                    if tokens:
                        word_vectors = [model.wv[token] for token in tokens if token in model.wv]
                        if word_vectors:
                            vectors.append(np.mean(word_vectors, axis=0))
                        else:
                            vectors.append(np.zeros(model.vector_size))
                    else:
                        vectors.append(np.zeros(model.vector_size))
                
                self.X = np.array(vectors)
                logger.info(f"Vectors generated from existing Word2Vec model, dimensions: {self.X.shape}")
                return
            except Exception as e:
                logger.warning(f"Failed to load existing Word2Vec model: {str(e)}. Training new model.")
        
        # 如果没有找到模型或加载失败，训练新模型
        logger.info("Vectorizing text using Word2Vec...")
        
        # 预处理文本
        tokenized_texts = [self.preprocess_text(summary) for summary in self.summaries]
        
        # 训练Word2Vec模型
        model = Word2Vec(sentences=tokenized_texts, vector_size=100, window=5, min_count=1, workers=4, epochs=100)
        
        # 计算每个summary的向量表示（取词向量的平均值）
        vectors = []
        for tokens in tokenized_texts:
            if tokens:
                word_vectors = [model.wv[token] for token in tokens if token in model.wv]
                if word_vectors:
                    vectors.append(np.mean(word_vectors, axis=0))
                else:
                    vectors.append(np.zeros(model.vector_size))
            else:
                vectors.append(np.zeros(model.vector_size))
        
        self.X = np.array(vectors)
        logger.info(f"Word2Vec vectorization complete, vector dimensions: {self.X.shape}")
        
        # 保存模型
        model.save(model_path)
        logger.info(f"Word2Vec model saved to {model_path}")
    
    def vectorize_doc2vec(self):
        """使用Doc2Vec向量化文本"""
        model_path = os.path.join(self.output_dir, 'doc2vec_model.bin')
        vectors_path = os.path.join(self.output_dir, 'doc2vec_vectors.npy')
        
        # 检查是否存在已训练的模型和向量
        if os.path.exists(model_path) and os.path.exists(vectors_path):
            logger.info(f"Loading existing Doc2Vec model from {model_path}")
            try:
                model = Doc2Vec.load(model_path)
                vectors = np.load(vectors_path)
                
                # 检查向量数量是否与当前摘要数量匹配
                if len(vectors) == len(self.summaries):
                    self.X = vectors
                    logger.info(f"Loaded vectors from {vectors_path}, dimensions: {self.X.shape}")
                    return
                else:
                    logger.warning(f"Number of loaded vectors ({len(vectors)}) doesn't match current summaries ({len(self.summaries)}). Training new model.")
            except Exception as e:
                logger.warning(f"Failed to load existing Doc2Vec model or vectors: {str(e)}. Training new model.")
        
        # 如果没有找到模型或加载失败，训练新模型
        logger.info("Vectorizing text using Doc2Vec...")
        
        # 预处理文本
        tokenized_texts = [self.preprocess_text(summary) for summary in self.summaries]
        
        # 创建TaggedDocument对象
        tagged_data = [TaggedDocument(words=tokens, tags=[str(i)]) for i, tokens in enumerate(tokenized_texts)]
        
        # 训练Doc2Vec模型
        model = Doc2Vec(vector_size=100, min_count=1, epochs=100, workers=4)
        model.build_vocab(tagged_data)
        model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
        
        # 获取文档向量
        self.X = np.array([model.dv[str(i)] for i in range(len(self.summaries))])
        logger.info(f"Doc2Vec vectorization complete, vector dimensions: {self.X.shape}")
        
        # 保存模型和向量
        model.save(model_path)
        np.save(vectors_path, self.X)
        logger.info(f"Doc2Vec model saved to {model_path}")
        logger.info(f"Doc2Vec vectors saved to {vectors_path}")
    
    def reduce_dimensions(self):
        """降维以便可视化，但不影响聚类过程"""
        logger.info("Reducing dimensions for visualization only...")
        
        # PCA降维到50维
        pca = PCA(n_components=min(50, self.X.shape[0], self.X.shape[1]))
        X_pca = pca.fit_transform(self.X)
        logger.info(f"PCA reduced dimensions: {X_pca.shape}")
        
        # t-SNE降维到2维用于可视化
        self.tsne = TSNE(n_components=2, random_state=42)
        self.X_2d = self.tsne.fit_transform(X_pca)
        logger.info(f"t-SNE reduced dimensions: {self.X_2d.shape}")
        
        return self.X_2d
    
    def perform_spectral_clustering(self, k=30):
        """执行谱聚类(Spectral Clustering)，固定为30个类"""
        logger.info(f"Performing Spectral Clustering with K={k}...")
        
        try:
            # 直接在原始向量空间进行聚类
            spectral = SpectralClustering(
                n_clusters=k,
                affinity='nearest_neighbors',
                random_state=42
            )
            self.cluster_labels = spectral.fit_predict(self.X)
            
            # 将谱聚类标签添加到元数据
            for i, item in enumerate(self.metadata):
                item["cluster"] = int(self.cluster_labels[i])
                
            # 计算轮廓系数
            silhouette_avg = silhouette_score(self.X, self.cluster_labels)
            logger.info(f"Spectral Clustering Silhouette Score: {silhouette_avg:.4f}")
            
            return True
        except Exception as e:
            logger.error(f"Spectral Clustering error: {str(e)}")
            return False
    
    def visualize_clusters(self):
        """可视化聚类结果"""
        logger.info("Visualizing clusters...")
        
        plt.figure(figsize=(14, 10))
        
        # 获取唯一的聚类标签
        unique_labels = sorted(set(self.cluster_labels))
        n_clusters = len(unique_labels)
        
        # 为每个聚类生成颜色
        colors = cm.rainbow(np.linspace(0, 1, n_clusters))
        
        # 计算每个聚类的中心点
        cluster_centers = []
        for label in unique_labels:
            mask = self.cluster_labels == label
            points = self.X_2d[mask]
            center = np.mean(points, axis=0)
            cluster_centers.append((label, center))
        
        # 绘制每个聚类的点和连接到中心点的线
        for i, label in enumerate(unique_labels):
            color = colors[i]
            marker = 'o'
            label_name = f"Cluster {label}"
            
            mask = self.cluster_labels == label
            plt.scatter(
                self.X_2d[mask, 0],
                self.X_2d[mask, 1],
                s=50, 
                c=[color],
                marker=marker,
                alpha=0.7,
                label=label_name if i % 3 == 0 else ""  # 每3个标签显示一个，避免拥挤
            )
            
            # 绘制到中心点的线
            for center_label, center in cluster_centers:
                if center_label == label:
                    for point in self.X_2d[mask]:
                        plt.plot([point[0], center[0]], [point[1], center[1]], 
                                 c=color, linewidth=0.5, linestyle='--', alpha=0.3)
        
        # 绘制中心点
        for label, center in cluster_centers:
            plt.scatter(center[0], center[1], s=200, c=[colors[label]], marker='*', 
                        edgecolors='k', linewidths=1)
        
        plt.title(f"Spectral Clustering (K={n_clusters})", fontsize=18)
        plt.xlabel("t-SNE Feature 1", fontsize=14)
        plt.ylabel("t-SNE Feature 2", fontsize=14)
        plt.legend(fontsize=10, loc='upper right', bbox_to_anchor=(1.15, 1))
        plt.grid(True, alpha=0.3)
        
        # 保存图像
        file_name = "spectral_clusters_visualization.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"Cluster visualization saved to {file_name}")
    
    def visualize_heatmap(self):
        """使用热图可视化聚类结果"""
        logger.info("Creating heatmap visualization...")
        
        # 获取唯一的聚类标签
        unique_labels = sorted(set(self.cluster_labels))
        
        # 计算每个聚类的中心
        cluster_centers = []
        for label in unique_labels:
            mask = self.cluster_labels == label
            # 直接使用原始向量空间计算中心
            cluster_centers.append(np.mean(self.X[mask], axis=0))
        
        # 计算聚类中心之间的距离矩阵
        n_clusters = len(cluster_centers)
        distance_matrix = np.zeros((n_clusters, n_clusters))
        
        for i in range(n_clusters):
            for j in range(n_clusters):
                distance_matrix[i, j] = np.linalg.norm(cluster_centers[i] - cluster_centers[j])
        
        # 创建热图
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            distance_matrix,
            annot=False,  # 30个类太多，不显示数值
            fmt=".2f",
            cmap="YlGnBu",
            xticklabels=[f"C{label}" for label in unique_labels],
            yticklabels=[f"C{label}" for label in unique_labels],
            cbar_kws={'label': 'Distance'}
        )
        plt.title("Spectral Clustering Heatmap", fontsize=16)
        plt.tight_layout()
        
        # 保存热图
        file_name = "spectral_heatmap.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"Heatmap visualization saved to {file_name}")
        
        # 统计每个聚类的大小
        cluster_sizes = {}
        for label in unique_labels:
            cluster_sizes[f"Cluster {label}"] = sum(self.cluster_labels == label)
        
        # 创建条形图显示聚类大小
        plt.figure(figsize=(15, 8))
        bars = plt.bar(
            range(len(cluster_sizes)), 
            list(cluster_sizes.values()), 
            color=sns.color_palette("husl", len(cluster_sizes))
        )
        
        # 在条形上方添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2., 
                height + 0.1,
                f'{int(height)}',
                ha='center', 
                va='bottom',
                fontsize=10
            )
        
        plt.title("Spectral Clustering - Cluster Sizes", fontsize=16)
        plt.xlabel("Clusters", fontsize=12)
        plt.ylabel("Number of Samples", fontsize=12)
        plt.xticks(range(len(cluster_sizes)), list(cluster_sizes.keys()), rotation=90)
        plt.tight_layout()
        
        # 保存条形图
        file_name = "spectral_cluster_sizes.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"Cluster sizes visualization saved to {file_name}")
    
    def analyze_clusters(self):
        """分析聚类内容，提取每个聚类的特征词和代表性summary"""
        logger.info("Analyzing clustering results...")
        
        # 将元数据转换为DataFrame
        df = pd.DataFrame(self.metadata)
        
        # 获取唯一的聚类标签
        unique_labels = sorted(set(self.cluster_labels))
        
        # 为每个聚类提取特征词和示例
        cluster_analysis = {}
        
        for label in unique_labels:
            cluster_mask = df["cluster"] == label
            cluster_name = f"Cluster_{label}"
            
            cluster_summaries = df[cluster_mask]["summary"].tolist()
            
            if not cluster_summaries:
                continue
            
            # 提取这个聚类中的常见词
            all_tokens = []
            for summary in cluster_summaries:
                tokens = self.preprocess_text(summary)
                all_tokens.extend(tokens)
            
            # 统计词频
            word_freq = {}
            for token in all_tokens:
                if token in word_freq:
                    word_freq[token] += 1
                else:
                    word_freq[token] = 1
            
            # 获取前10个高频词
            top_features = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            top_features = [{"word": word, "frequency": freq} for word, freq in top_features]
            
            # 获取这个聚类中的所有样本
            cluster_samples = df[cluster_mask].to_dict('records')
            
            # 统计聚类大小
            cluster_size = sum(cluster_mask)
            
            # 统计每种源在这个聚类中的比例
            source_counts = df[cluster_mask]["source"].value_counts().to_dict()
            source_percentages = {k: f"{v/cluster_size*100:.1f}%" for k, v in source_counts.items()}
            
            # 统计每种类型在这个聚类中的比例
            type_counts = df[cluster_mask]["type"].value_counts().to_dict()
            type_percentages = {k: f"{v/cluster_size*100:.1f}%" for k, v in type_counts.items()}
            
            cluster_analysis[cluster_name] = {
                "size": cluster_size,
                "percentage": f"{cluster_size/len(self.metadata)*100:.1f}%",
                "top_features": top_features,
                "source_distribution": source_percentages,
                "type_distribution": type_percentages,
                "samples": cluster_samples  # 包含所有样本的详细信息
            }
        
        # 保存分析结果
        with open(os.path.join(self.output_dir, "spectral_cluster_analysis.json"), "w", encoding="utf-8") as f:
            json.dump(cluster_analysis, f, ensure_ascii=False, indent=2)
        logger.info("Cluster analysis saved to spectral_cluster_analysis.json")
        
        # 打印分析结果摘要
        for cluster_name, analysis in cluster_analysis.items():
            logger.info(f"\n{cluster_name} (Contains {analysis['size']} samples, {analysis['percentage']} of total)")
            logger.info(f"Top features: {', '.join([item['word'] for item in analysis['top_features']])}")
            logger.info(f"Source distribution: {analysis['source_distribution']}")
            logger.info(f"Type distribution: {analysis['type_distribution']}")
            logger.info("-" * 80)
        
        return cluster_analysis
    
    def find_optimal_k_spectral(self, min_k=2, max_k=40, step=2):
        """寻找谱聚类的最优K值
        
        通过计算不同K值的轮廓系数(Silhouette Score)和Davies-Bouldin指数来评估聚类效果
        
        Args:
            min_k: 最小K值
            max_k: 最大K值
            step: K值递增步长
        
        Returns:
            最优K值
        """
        logger.info(f"Finding optimal K for Spectral Clustering ({min_k}-{max_k}, step={step})...")
        
        k_range = range(min_k, max_k + 1, step)
        silhouette_scores = []
        davies_bouldin_scores = []
        
        # 为了加速计算，可以在降维后的数据上评估
        # 但最终聚类仍在原始空间进行
        X_eval = self.X
        
        for k in tqdm(k_range, desc="Testing different K values"):
            try:
                # 使用nearest_neighbors亲和度，这通常在高维数据上效果更好
                spectral = SpectralClustering(
                    n_clusters=k,
                    affinity='nearest_neighbors',
                    random_state=42
                )
                labels = spectral.fit_predict(X_eval)
                
                # 计算评估指标
                sil_score = silhouette_score(X_eval, labels)
                db_score = davies_bouldin_score(X_eval, labels)
                
                silhouette_scores.append(sil_score)
                davies_bouldin_scores.append(db_score)
                
                logger.info(f"K={k}, Silhouette Score={sil_score:.4f}, Davies-Bouldin Index={db_score:.4f}")
            except Exception as e:
                logger.error(f"Error evaluating K={k}: {str(e)}")
                silhouette_scores.append(-1)
                davies_bouldin_scores.append(float('inf'))
        
        # 绘制评估指标曲线
        plt.figure(figsize=(12, 10))
        
        # 轮廓系数 - 越高越好
        plt.subplot(2, 1, 1)
        plt.plot(list(k_range), silhouette_scores, 'bo-')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score Evaluation (higher is better)')
        plt.grid(True)
        
        # Davies-Bouldin指数 - 越低越好
        plt.subplot(2, 1, 2)
        plt.plot(list(k_range), davies_bouldin_scores, 'ro-')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Davies-Bouldin Index')
        plt.title('Davies-Bouldin Index Evaluation (lower is better)')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'spectral_optimal_k.png'), dpi=300)
        
        # 根据轮廓系数选择最优K值
        valid_scores = [(k, score) for k, score in zip(k_range, silhouette_scores) if score > 0]
        if valid_scores:
            best_k, best_score = max(valid_scores, key=lambda x: x[1])
            logger.info(f"Optimal K for Spectral Clustering: {best_k}, Silhouette Score: {best_score:.4f}")
        else:
            best_k = 30  # 默认值
            logger.warning(f"Could not determine optimal K, using default: {best_k}")
        
        return best_k
    
    def run_analysis(self, vectorization_method="doc2vec", find_optimal_k=True):
        """运行完整的分析流程
        
        Args:
            vectorization_method: 向量化方法，"word2vec"或"doc2vec"
            find_optimal_k: 是否寻找最优K值，False则使用固定值30
        """
        # 收集数据
        self.collect_from_malware_snippets()
        self.collect_from_package_label()
        
        if not self.summaries:
            logger.error("No behavior summaries collected")
            return
        
        logger.info(f"Collected {len(self.summaries)} behavior summaries in total")
        
        # 数据向量化
        if vectorization_method == "word2vec":
            self.vectorize_word2vec()
        else:
            self.vectorize_doc2vec()
        
        # 降维仅用于可视化
        self.reduce_dimensions()
        
        # 确定聚类数量
        if find_optimal_k:
            # 寻找最优K值
            k = self.find_optimal_k_spectral(min_k=2, max_k=40, step=2)
        else:
            # 使用固定的K值
            k = 20
            logger.info(f"Using fixed K={k} for Spectral Clustering")
        
        # 执行谱聚类
        if self.perform_spectral_clustering(k=k):
            # 可视化聚类结果
            self.visualize_clusters()
            self.visualize_heatmap()
            
            # 分析聚类内容
            cluster_analysis = self.analyze_clusters()
            
            # 保存完整的元数据
            df = pd.DataFrame(self.metadata)
            df.to_csv(os.path.join(self.output_dir, "behavior_summaries_with_clusters.csv"), index=False)
            
            logger.info("Analysis complete, results saved to the results directory")
        else:
            logger.error("Spectral clustering failed")

if __name__ == "__main__":
    clusterer = BehaviorSummaryClusterer()
    # 设置find_optimal_k=True来寻找最优K值，False则使用固定值30
    clusterer.run_analysis(vectorization_method="doc2vec", find_optimal_k=False) 