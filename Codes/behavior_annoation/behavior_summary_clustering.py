#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import glob
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
import matplotlib.cm as cm
import pandas as pd
from tqdm import tqdm
import logging
import nltk
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import re
import seaborn as sns

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
        logger.info("正在收集malware_snippets目录下的behavior summaries...")
        
        result_files = glob.glob(f"{self.malware_snippets_dir}/**/*.json", recursive=True)
        
        for file_path in tqdm(result_files, desc="处理malware_snippets文件"):
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
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
    
    def collect_from_package_label(self):
        """收集package_label目录下的behavior summaries"""
        logger.info("正在收集package_label目录下的behavior summaries...")
        
        analysis_files = glob.glob(f"{self.package_label_dir}/**/*analysis.json", recursive=True)
        
        for file_path in tqdm(analysis_files, desc="处理package_label文件"):
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
                logger.error(f"处理文件 {file_path} 时出错: {str(e)}")
    
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
        logger.info("使用Word2Vec向量化文本...")
        
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
        logger.info(f"Word2Vec向量化完成，向量维度: {self.X.shape}")
        
        # 保存模型
        model_path = os.path.join(self.output_dir, 'word2vec_model.bin')
        model.save(model_path)
        logger.info(f"Word2Vec模型已保存到 {model_path}")
    
    def vectorize_doc2vec(self):
        """使用Doc2Vec向量化文本"""
        logger.info("使用Doc2Vec向量化文本...")
        
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
        logger.info(f"Doc2Vec向量化完成，向量维度: {self.X.shape}")
        
        # 保存模型
        model_path = os.path.join(self.output_dir, 'doc2vec_model.bin')
        model.save(model_path)
        logger.info(f"Doc2Vec模型已保存到 {model_path}")
    
    def reduce_dimensions(self):
        """降维以便可视化，但不影响聚类过程"""
        logger.info("Reducing dimensions for visualization only...")
        
        # PCA降维到50维
        pca = PCA(n_components=min(50, self.X.shape[0], self.X.shape[1]))
        X_pca = pca.fit_transform(self.X)
        logger.info(f"PCA reduced dimensions: {X_pca.shape}")
        
        # t-SNE降维到3维用于可视化
        self.tsne = TSNE(n_components=3, random_state=42)
        self.X_3d = self.tsne.fit_transform(X_pca)
        logger.info(f"t-SNE reduced dimensions: {self.X_3d.shape}")
        
        # 同时保留2D版本用于兼容现有代码
        self.tsne_2d = TSNE(n_components=2, random_state=42)
        self.X_2d = self.tsne_2d.fit_transform(X_pca)
        logger.info(f"t-SNE 2D reduced dimensions: {self.X_2d.shape}")
        
        return self.X_3d
    
    def find_optimal_k(self, max_k=20):
        """寻找最优的K值"""
        logger.info(f"寻找最优K值 (1-{max_k})...")
        
        inertias = []
        silhouette_scores = []
        k_range = range(2, max_k + 1)
        
        for k in tqdm(k_range, desc="Testing different K values"):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.X)
            inertias.append(kmeans.inertia_)
            
            # 计算轮廓系数
            silhouette_avg = silhouette_score(self.X, kmeans.labels_)
            silhouette_scores.append(silhouette_avg)
            logger.info(f"K={k}, Silhouette Score={silhouette_avg:.4f}")
        
        # 保存肘部曲线
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(k_range, inertias, 'bo-')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Inertia')
        plt.title('K-Means Elbow Curve')
        
        plt.subplot(1, 2, 2)
        plt.plot(k_range, silhouette_scores, 'ro-')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score Evaluation')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'optimal_k.png'), dpi=300)
        
        # 返回最优K值 (轮廓系数最高的K值)
        best_k = k_range[np.argmax(silhouette_scores)]
        logger.info(f"Optimal K: {best_k}, Silhouette Score: {max(silhouette_scores):.4f}")
        return best_k
    
    def perform_kmeans_clustering(self, k):
        """执行K-means聚类"""
        logger.info(f"使用K={k}执行K-means聚类...")
        
        self.kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        self.cluster_labels_kmeans = self.kmeans.fit_predict(self.X)
        
        # 将聚类标签添加到元数据
        for i, item in enumerate(self.metadata):
            item["cluster_kmeans"] = int(self.cluster_labels_kmeans[i])
    
    def perform_spectral_clustering(self, k):
        """执行谱聚类(Spectral Clustering)"""
        logger.info(f"Using K={k} for Spectral Clustering...")
        
        try:
            # 直接在原始向量空间进行聚类
            spectral = SpectralClustering(
                n_clusters=k,
                affinity='nearest_neighbors',
                random_state=42
            )
            self.cluster_labels_spectral = spectral.fit_predict(self.X)
            
            # 将谱聚类标签添加到元数据
            for i, item in enumerate(self.metadata):
                item["cluster_spectral"] = int(self.cluster_labels_spectral[i])
                
            # 计算轮廓系数
            silhouette_avg = silhouette_score(self.X, self.cluster_labels_spectral)
            logger.info(f"Spectral Clustering Silhouette Score: {silhouette_avg:.4f}")
            
            return True
        except Exception as e:
            logger.error(f"Spectral Clustering error: {str(e)}")
            return False
    
    def perform_agglomerative_clustering(self, k):
        """执行层次聚类(Agglomerative Clustering)"""
        logger.info(f"使用K={k}执行层次聚类...")
        
        agglomerative = AgglomerativeClustering(n_clusters=k)
        self.cluster_labels_agglomerative = agglomerative.fit_predict(self.X)
        
        # 将层次聚类标签添加到元数据
        for i, item in enumerate(self.metadata):
            item["cluster_agglomerative"] = int(self.cluster_labels_agglomerative[i])
            
        # 计算轮廓系数
        silhouette_avg = silhouette_score(self.X, self.cluster_labels_agglomerative)
        logger.info(f"层次聚类轮廓系数: {silhouette_avg:.4f}")
    
    def perform_dbscan_clustering(self):
        """执行DBSCAN聚类"""
        logger.info("Performing DBSCAN clustering...")
        
        # 直接在原始向量空间尝试不同的参数
        eps_values = [0.5, 1.0, 1.5, 2.0, 2.5]
        min_samples_values = [5, 10, 15]
        
        best_silhouette = -1
        best_params = None
        best_labels = None
        
        for eps in eps_values:
            for min_samples in min_samples_values:
                dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                labels = dbscan.fit_predict(self.X)
                
                # 计算聚类数量（不包括噪声点）
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                
                # 只有当聚类数量大于1时才计算轮廓系数
                if n_clusters > 1:
                    # 排除噪声点进行轮廓系数计算
                    mask = labels != -1
                    if sum(mask) > 1:  # 确保至少有两个非噪声点
                        silhouette_avg = silhouette_score(self.X[mask], labels[mask])
                        logger.info(f"DBSCAN (eps={eps}, min_samples={min_samples}): clusters={n_clusters}, silhouette={silhouette_avg:.4f}")
                        
                        if silhouette_avg > best_silhouette:
                            best_silhouette = silhouette_avg
                            best_params = (eps, min_samples)
                            best_labels = labels
                else:
                    logger.info(f"DBSCAN (eps={eps}, min_samples={min_samples}): Only found {n_clusters} clusters")
        
        if best_params:
            logger.info(f"Best DBSCAN parameters: eps={best_params[0]}, min_samples={best_params[1]}, silhouette={best_silhouette:.4f}")
            self.cluster_labels_dbscan = best_labels
            
            # 将DBSCAN聚类标签添加到元数据
            for i, item in enumerate(self.metadata):
                item["cluster_dbscan"] = int(self.cluster_labels_dbscan[i])
            
            return True
        else:
            logger.warning("Could not find suitable DBSCAN parameters")
            return False
    
    def visualize_clusters(self, method="kmeans"):
        """可视化聚类结果"""
        # 创建2D和3D两个可视化
        self._visualize_clusters_2d(method)
        self._visualize_clusters_3d(method)
        
    def _visualize_clusters_2d(self, method="kmeans"):
        """二维可视化聚类结果"""
        plt.figure(figsize=(14, 10))
        
        if method == "kmeans":
            labels = self.cluster_labels_kmeans
            title = f"K-Means Clustering (K={len(set(labels))}) - 2D"
        elif method == "spectral":
            labels = self.cluster_labels_spectral
            title = f"Spectral Clustering (K={len(set(labels))}) - 2D"
        elif method == "agglomerative":
            labels = self.cluster_labels_agglomerative
            title = f"Hierarchical Clustering (K={len(set(labels))}) - 2D"
        elif method == "dbscan":
            labels = self.cluster_labels_dbscan
            title = "DBSCAN Clustering - 2D"
        else:
            logger.error(f"Unsupported clustering method: {method}")
            return
        
        # 获取唯一的聚类标签
        unique_labels = set(labels)
        n_clusters = len(unique_labels)
        if -1 in unique_labels:  # DBSCAN可能有噪声点
            n_clusters -= 1
        
        # 为每个聚类生成颜色
        colors = cm.rainbow(np.linspace(0, 1, n_clusters + 1))
        
        # 为噪声点指定颜色 (如果有)
        noise_color = 'black'
        
        # 计算每个聚类的中心点
        cluster_centers = []
        for label in unique_labels:
            if label != -1:  # 排除噪声点
                mask = labels == label
                points = self.X_2d[mask]
                center = np.mean(points, axis=0)
                cluster_centers.append((label, center))
        
        # 绘制每个聚类的点和连接到中心点的线
        for i, label in enumerate(unique_labels):
            if label == -1:  # 噪声点
                color = noise_color
                marker = 'x'
                label_name = "Noise"
            else:
                color = colors[i if label == -1 else label]
                marker = 'o'
                label_name = f"Cluster {label}"
            
            mask = labels == label
            plt.scatter(
                self.X_2d[mask, 0],
                self.X_2d[mask, 1],
                s=50, 
                c=[color],
                marker=marker,
                alpha=0.7,
                label=label_name
            )
            
            # 如果不是噪声点，绘制到中心点的线
            if label != -1:
                for center_label, center in cluster_centers:
                    if center_label == label:
                        for point in self.X_2d[mask]:
                            plt.plot([point[0], center[0]], [point[1], center[1]], 
                                     c=color, linewidth=0.5, linestyle='--', alpha=0.3)
        
        # 绘制中心点
        for label, center in cluster_centers:
            plt.scatter(center[0], center[1], s=200, c=[colors[label]], marker='*', 
                        edgecolors='k', linewidths=1)
        
        plt.title(title, fontsize=18)
        plt.xlabel("t-SNE Feature 1", fontsize=14)
        plt.ylabel("t-SNE Feature 2", fontsize=14)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # 保存图像
        file_name = f"{method}_clusters_visualization_2d.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"2D Cluster visualization saved to {file_name}")
    
    def _visualize_clusters_3d(self, method="kmeans"):
        """三维可视化聚类结果"""
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        if method == "kmeans":
            labels = self.cluster_labels_kmeans
            title = f"K-Means Clustering (K={len(set(labels))}) - 3D"
        elif method == "spectral":
            labels = self.cluster_labels_spectral
            title = f"Spectral Clustering (K={len(set(labels))}) - 3D"
        elif method == "agglomerative":
            labels = self.cluster_labels_agglomerative
            title = f"Hierarchical Clustering (K={len(set(labels))}) - 3D"
        elif method == "dbscan":
            labels = self.cluster_labels_dbscan
            title = "DBSCAN Clustering - 3D"
        else:
            logger.error(f"Unsupported clustering method: {method}")
            return
        
        # 获取唯一的聚类标签
        unique_labels = set(labels)
        n_clusters = len(unique_labels)
        if -1 in unique_labels:  # DBSCAN可能有噪声点
            n_clusters -= 1
        
        # 为每个聚类生成颜色
        colors = cm.rainbow(np.linspace(0, 1, n_clusters + 1))
        
        # 为噪声点指定颜色 (如果有)
        noise_color = 'black'
        
        # 计算每个聚类的中心点
        cluster_centers = []
        for label in unique_labels:
            if label != -1:  # 排除噪声点
                mask = labels == label
                points = self.X_3d[mask]
                center = np.mean(points, axis=0)
                cluster_centers.append((label, center))
        
        # 绘制每个聚类的点
        for i, label in enumerate(unique_labels):
            if label == -1:  # 噪声点
                color = noise_color
                marker = 'x'
                label_name = "Noise"
            else:
                color = colors[i if label == -1 else label]
                marker = 'o'
                label_name = f"Cluster {label}"
            
            mask = labels == label
            ax.scatter(
                self.X_3d[mask, 0],
                self.X_3d[mask, 1],
                self.X_3d[mask, 2],
                s=50, 
                c=[color],
                marker=marker,
                alpha=0.7,
                label=label_name
            )
            
            # 如果不是噪声点，绘制到中心点的线（可选，在3D中可能会使图形过于复杂）
            if label != -1 and len(self.X_3d[mask]) < 100:  # 限制线条数量以避免过度绘制
                for center_label, center in cluster_centers:
                    if center_label == label:
                        for point in self.X_3d[mask]:
                            ax.plot([point[0], center[0]], 
                                    [point[1], center[1]], 
                                    [point[2], center[2]],
                                    c=color, linewidth=0.5, linestyle='--', alpha=0.2)
        
        # 绘制中心点
        for label, center in cluster_centers:
            ax.scatter(center[0], center[1], center[2], 
                      s=200, c=[colors[label]], marker='*', 
                      edgecolors='k', linewidths=1)
        
        ax.set_title(title, fontsize=18)
        ax.set_xlabel("t-SNE Feature 1", fontsize=14)
        ax.set_ylabel("t-SNE Feature 2", fontsize=14)
        ax.set_zlabel("t-SNE Feature 3", fontsize=14)
        
        # 添加图例
        ax.legend(fontsize=10)
        
        # 设置视角
        ax.view_init(elev=30, azim=45)
        
        # 保存图像
        file_name = f"{method}_clusters_visualization_3d.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"3D Cluster visualization saved to {file_name}")
        
        # 创建额外的视角
        for angle in [0, 90, 180, 270]:
            ax.view_init(elev=30, azim=angle)
            file_name = f"{method}_clusters_visualization_3d_angle_{angle}.png"
            plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
            logger.info(f"3D Cluster visualization (angle {angle}) saved to {file_name}")
        
    def visualize_heatmap(self, method="kmeans"):
        """使用热图可视化聚类结果"""
        logger.info(f"Creating heatmap visualization for {method} clustering...")
        
        if method == "kmeans":
            labels = self.cluster_labels_kmeans
            title = f"K-Means Clustering Heatmap"
        elif method == "spectral":
            labels = self.cluster_labels_spectral
            title = f"Spectral Clustering Heatmap"
        elif method == "agglomerative":
            labels = self.cluster_labels_agglomerative
            title = f"Hierarchical Clustering Heatmap"
        elif method == "dbscan":
            labels = self.cluster_labels_dbscan
            title = "DBSCAN Clustering Heatmap"
        else:
            logger.error(f"Unsupported clustering method: {method}")
            return
        
        # 获取唯一的聚类标签
        unique_labels = sorted(set(labels))
        if -1 in unique_labels:  # 移除噪声点
            unique_labels.remove(-1)
        
        # 计算每个聚类的中心
        cluster_centers = []
        for label in unique_labels:
            mask = labels == label
            # 直接使用原始向量空间计算中心
            cluster_centers.append(np.mean(self.X[mask], axis=0))
        
        # 计算聚类中心之间的距离矩阵
        n_clusters = len(cluster_centers)
        distance_matrix = np.zeros((n_clusters, n_clusters))
        
        for i in range(n_clusters):
            for j in range(n_clusters):
                distance_matrix[i, j] = np.linalg.norm(cluster_centers[i] - cluster_centers[j])
        
        # 创建热图
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            distance_matrix,
            annot=True,
            fmt=".2f",
            cmap="YlGnBu",
            xticklabels=[f"C{label}" for label in unique_labels],
            yticklabels=[f"C{label}" for label in unique_labels],
            cbar_kws={'label': 'Distance'}
        )
        plt.title(title, fontsize=16)
        plt.tight_layout()
        
        # 保存热图
        file_name = f"{method}_heatmap.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"Heatmap visualization saved to {file_name}")
        
        # 统计每个聚类的大小
        cluster_sizes = {}
        for label in unique_labels:
            cluster_sizes[f"Cluster {label}"] = sum(labels == label)
        
        # 创建条形图显示聚类大小
        plt.figure(figsize=(12, 6))
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
        
        plt.title(f"{method.capitalize()} Clustering - Cluster Sizes", fontsize=16)
        plt.xlabel("Clusters", fontsize=12)
        plt.ylabel("Number of Samples", fontsize=12)
        plt.xticks(range(len(cluster_sizes)), list(cluster_sizes.keys()), rotation=45)
        plt.tight_layout()
        
        # 保存条形图
        file_name = f"{method}_cluster_sizes.png"
        plt.savefig(os.path.join(self.output_dir, file_name), dpi=300, bbox_inches='tight')
        logger.info(f"Cluster sizes visualization saved to {file_name}")
    
    def analyze_clusters(self, method="kmeans"):
        """分析聚类内容，提取每个聚类的特征词和代表性summary"""
        logger.info(f"Analyzing {method} clustering results...")
        
        if method == "kmeans":
            labels = self.cluster_labels_kmeans
            cluster_field = "cluster_kmeans"
        elif method == "spectral":
            labels = self.cluster_labels_spectral
            cluster_field = "cluster_spectral"
        elif method == "agglomerative":
            labels = self.cluster_labels_agglomerative
            cluster_field = "cluster_agglomerative"
        elif method == "dbscan":
            labels = self.cluster_labels_dbscan
            cluster_field = "cluster_dbscan"
        else:
            logger.error(f"Unsupported clustering method: {method}")
            return
        
        # 获取唯一的聚类标签
        unique_labels = sorted(set(labels))
        
        # 将元数据转换为DataFrame
        df = pd.DataFrame(self.metadata)
        
        # 为每个聚类提取特征词和示例
        cluster_analysis = {}
        
        for label in unique_labels:
            cluster_mask = df[cluster_field] == label
            cluster_name = "Noise" if label == -1 else f"Cluster {label}"
            
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
            top_features = [word for word, _ in top_features]
            
            # 获取这个聚类中的示例 (最多5个)
            examples = df[cluster_mask].sample(min(5, len(cluster_summaries)))["summary"].tolist()
            
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
                "examples": examples,
                "source_distribution": source_percentages,
                "type_distribution": type_percentages
            }
        
        # 保存分析结果
        with open(os.path.join(self.output_dir, f"{method}_cluster_analysis.json"), "w", encoding="utf-8") as f:
            json.dump(cluster_analysis, f, ensure_ascii=False, indent=2)
        
        # 打印分析结果
        for cluster_name, analysis in cluster_analysis.items():
            logger.info(f"\n{cluster_name} (Contains {analysis['size']} samples, {analysis['percentage']} of total)")
            logger.info(f"Top features: {', '.join(analysis['top_features'])}")
            logger.info(f"Source distribution: {analysis['source_distribution']}")
            logger.info(f"Type distribution: {analysis['type_distribution']}")
            logger.info("Examples:")
            for i, example in enumerate(analysis['examples'][:3], 1):
                logger.info(f"  {i}. {example}")
            logger.info("-" * 80)
        
        return cluster_analysis
    
    def run_analysis(self, vectorization_method="word2vec", use_original_space=True):
        """运行完整的分析流程
        
        Args:
            vectorization_method: 向量化方法，"word2vec"或"doc2vec"
            use_original_space: 是否在原始向量空间聚类，True表示不降维
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
        
        # 寻找最优K值
        optimal_k = self.find_optimal_k(max_k=20)
        
        # 执行K-means聚类
        self.perform_kmeans_clustering(optimal_k)
        
        # 可视化K-means聚类结果
        self.visualize_clusters(method="kmeans")
        self.visualize_heatmap(method="kmeans")
        
        # 分析K-means聚类内容
        kmeans_analysis = self.analyze_clusters(method="kmeans")
        
        # 执行谱聚类
        if self.perform_spectral_clustering(optimal_k):
            # 可视化谱聚类结果
            self.visualize_clusters(method="spectral")
            self.visualize_heatmap(method="spectral")
            
            # 分析谱聚类内容
            spectral_analysis = self.analyze_clusters(method="spectral")
        
        # 执行层次聚类
        self.perform_agglomerative_clustering(optimal_k)
        
        # 可视化层次聚类结果
        self.visualize_clusters(method="agglomerative")
        self.visualize_heatmap(method="agglomerative")
        
        # 分析层次聚类内容
        agglomerative_analysis = self.analyze_clusters(method="agglomerative")
        
        # 执行DBSCAN聚类
        if self.perform_dbscan_clustering():
            # 可视化DBSCAN聚类结果
            self.visualize_clusters(method="dbscan")
            self.visualize_heatmap(method="dbscan")
            
            # 分析DBSCAN聚类内容
            dbscan_analysis = self.analyze_clusters(method="dbscan")
        
        # 保存完整的元数据
        df = pd.DataFrame(self.metadata)
        df.to_csv(os.path.join(self.output_dir, "behavior_summaries_with_clusters.csv"), index=False)
        
        logger.info("Analysis complete, results saved to the results directory")

if __name__ == "__main__":
    clusterer = BehaviorSummaryClusterer()
    
    # 可以选择使用Word2Vec或Doc2Vec进行向量化
    # 直接在原始向量空间进行聚类，而不是降维后的空间
    clusterer.run_analysis(vectorization_method="doc2vec", use_original_space=True) 