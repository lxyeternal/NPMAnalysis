#!/usr/bin/env python3
"""
RQ4: Tool Combination Heatmap Visualization (1x4 Layout)
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'serif']
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['axes.unicode_minus'] = False
sns.set_style("white")

RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"
BENIGN_SKIP_LIST_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/selected_benign_packages.txt"
SCRIPT_DIR = Path(__file__).parent.resolve()
STATISTIC_DIR = SCRIPT_DIR.parent / "statistic"

TOOL_LABELS = [
    'OSSGadget', 'GuardDog', 'GENIE', 'Packj-S', 'Packj-T',
    'SAP-DT', 'SAP-RF', 'SAP-XGB', 'Cerebro',
    'MalPac-MLP', 'MalPac-NB', 'MalPac-SVM', 'Socket.AI'
]

TOOL_KEYS = [
    'ossgadget', 'guarddog', 'genie', 'packj_static', 'packj_trace',
    'sap_DT', 'sap_RF', 'sap_XGB', 'cerebro',
    'malpacdetector_mlp', 'malpacdetector_nb', 'malpacdetector_svm', 'socketai'
]


def analyze_guarddog(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return "benign" if "Found 0 potentially malicious indicators" in f.read() else "malware"
    except:
        return None


def analyze_ossgadget(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return "benign" if "0 matches found." in f.read() else "malware"
    except:
        return None


def analyze_packj(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return "benign" if not content.strip() or "No risks found!" in content else "malware"
    except:
        return None


def analyze_genie(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return "benign" if not f.read().strip() else "malware"
    except:
        return None


def analyze_sap(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return "benign" if f.read().strip() == "0" else "malware"
    except:
        return None


def analyze_socketai(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return "malware" if json.load(f).get("is_malicious", False) else "benign"
    except:
        return None


TOOLS_CONFIG = {
    "guarddog": {"path": os.path.join(RESULTS_DIR, "guarddog"), "func": analyze_guarddog},
    "ossgadget": {"path": os.path.join(RESULTS_DIR, "ossgadget"), "func": analyze_ossgadget},
    "genie": {"path": os.path.join(RESULTS_DIR, "genie"), "func": analyze_genie},
    "socketai": {"path": os.path.join(RESULTS_DIR, "socketai"), "func": analyze_socketai},
    "packj_static": {"path": os.path.join(RESULTS_DIR, "packj", "result_static"), "func": analyze_packj},
    "packj_trace": {"path": os.path.join(RESULTS_DIR, "packj", "result_trace"), "func": analyze_packj},
    "sap_DT": {"path": os.path.join(RESULTS_DIR, "sap", "DT"), "func": analyze_sap},
    "sap_RF": {"path": os.path.join(RESULTS_DIR, "sap", "RF"), "func": analyze_sap},
    "sap_XGB": {"path": os.path.join(RESULTS_DIR, "sap", "XGB"), "func": analyze_sap},
}


def load_skip_list(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return {line.strip() for line in f if line.strip()}


def find_package_files(base_path, package_type):
    result = []
    package_path = os.path.join(base_path, package_type)
    if not os.path.exists(package_path):
        return result

    for package_name in os.listdir(package_path):
        package_dir = os.path.join(package_path, package_name)
        if not os.path.isdir(package_dir):
            continue
        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            if not os.path.isdir(version_dir):
                continue
            files = [f for f in os.listdir(version_dir) if os.path.isfile(os.path.join(version_dir, f))]
            if files:
                result.append((os.path.join(version_dir, files[0]),
                              f"{package_name.replace('##', '/')}/{version}"))
    return result


def calculate_single_tool_metrics(tool_config, benign_skip_list):
    base_path, analyze_func = tool_config["path"], tool_config["func"]
    tp = tn = fp = fn = 0

    for file_path, package_key in find_package_files(base_path, "benign"):
        if package_key in benign_skip_list:
            continue
        prediction = analyze_func(file_path)
        if prediction == "benign":
            tn += 1
        elif prediction == "malware":
            fp += 1

    for file_path, package_key in find_package_files(base_path, "malware"):
        prediction = analyze_func(file_path)
        if prediction == "malware":
            tp += 1
        elif prediction == "benign":
            fn += 1

    return {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn}


def load_cerebro_metrics(benign_skip_list):
    csv_path = os.path.join(RESULTS_DIR, "cerebro", "evaluation_npm_with_label.csv")
    if not os.path.exists(csv_path):
        return {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

    df = pd.read_csv(csv_path)
    tp = tn = fp = fn = 0

    for _, row in df.iterrows():
        pkg_name = row['package_name']
        parts = pkg_name.rsplit('-', 1)
        if len(parts) == 2:
            package_key = f"{parts[0].replace('##', '/')}/{parts[1]}"
        else:
            package_key = pkg_name.replace('##', '/')

        actual = 'malware' if row['ground_truth'] == 1 else 'benign'
        if actual == 'benign' and package_key in benign_skip_list:
            continue

        prediction = 'malware' if row['prediction'] == 1 else 'benign'
        if prediction == 'malware' and actual == 'malware':
            tp += 1
        elif prediction == 'benign' and actual == 'benign':
            tn += 1
        elif prediction == 'malware' and actual == 'benign':
            fp += 1
        else:
            fn += 1

    return {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn}


def load_malpacdetector_metrics(algo, benign_skip_list):
    csv_path = os.path.join(RESULTS_DIR, "MalPacDetector", "summary_detection_results.csv")
    if not os.path.exists(csv_path):
        return {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

    df = pd.read_csv(csv_path)
    tp = tn = fp = fn = 0

    for _, row in df.iterrows():
        package_key = f"{row['package_name'].replace('##', '/')}/{row['version']}"
        actual = 'malware' if row['actual_label'] == 'malware' else 'benign'
        if actual == 'benign' and package_key in benign_skip_list:
            continue

        prediction = 'malware' if row[algo] == 'malicious' else 'benign'
        if prediction == 'malware' and actual == 'malware':
            tp += 1
        elif prediction == 'benign' and actual == 'benign':
            tn += 1
        elif prediction == 'malware' and actual == 'benign':
            fp += 1
        else:
            fn += 1

    return {'TP': tp, 'TN': tn, 'FP': fp, 'FN': fn}


class HeatmapVisualizer:
    def __init__(self, combination_csv, benign_skip_list):
        self.benign_skip_list = benign_skip_list
        self.combination_df = pd.read_csv(combination_csv) if os.path.exists(combination_csv) else pd.DataFrame()

        self.single_tool_metrics = {}
        for tool_name, tool_config in TOOLS_CONFIG.items():
            if os.path.exists(tool_config["path"]):
                self.single_tool_metrics[tool_name] = calculate_single_tool_metrics(tool_config, benign_skip_list)

        self.single_tool_metrics['cerebro'] = load_cerebro_metrics(benign_skip_list)
        for algo in ['MLP', 'NB', 'SVM']:
            self.single_tool_metrics[f'malpacdetector_{algo.lower()}'] = load_malpacdetector_metrics(algo, benign_skip_list)

    def get_combination_values(self, tool1, tool2, strategy):
        if self.combination_df.empty:
            return {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

        mask1 = (self.combination_df['tool1'] == tool1) & \
                (self.combination_df['tool2'] == tool2) & \
                (self.combination_df['strategy'] == strategy)
        mask2 = (self.combination_df['tool1'] == tool2) & \
                (self.combination_df['tool2'] == tool1) & \
                (self.combination_df['strategy'] == strategy)

        row = self.combination_df[mask1 | mask2]
        if len(row) == 0:
            return {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

        row = row.iloc[0]
        return {'TP': int(row['tp']), 'TN': int(row['tn']), 'FP': int(row['fp']), 'FN': int(row['fn'])}

    def create_matrix(self, metric, strategy):
        n_tools = len(TOOL_KEYS)
        matrix = np.zeros((n_tools, n_tools))

        for i, tool1 in enumerate(TOOL_KEYS):
            for j, tool2 in enumerate(TOOL_KEYS):
                if i == j:
                    values = self.single_tool_metrics.get(tool1, {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0})
                else:
                    values = self.get_combination_values(tool1, tool2, strategy)
                matrix[i, j] = values[metric]

        return matrix

    def find_key_cells(self, tp_matrix, tn_matrix):
        n = len(TOOL_KEYS)
        combined = tp_matrix + tn_matrix

        tp_max, tp_min = -1, float('inf')
        tn_max, tn_min = -1, float('inf')
        combined_max, combined_min = -1, float('inf')
        tp_max_pos = tn_max_pos = combined_max_pos = None
        tp_min_pos = tn_min_pos = combined_min_pos = None

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue

                if tp_matrix[i, j] > tp_max:
                    tp_max = tp_matrix[i, j]
                    tp_max_pos = (i, j)
                if tp_matrix[i, j] < tp_min:
                    tp_min = tp_matrix[i, j]
                    tp_min_pos = (i, j)

                if tn_matrix[i, j] > tn_max:
                    tn_max = tn_matrix[i, j]
                    tn_max_pos = (i, j)
                if tn_matrix[i, j] < tn_min:
                    tn_min = tn_matrix[i, j]
                    tn_min_pos = (i, j)

                if combined[i, j] > combined_max:
                    combined_max = combined[i, j]
                    combined_max_pos = (i, j)
                if combined[i, j] < combined_min:
                    combined_min = combined[i, j]
                    combined_min_pos = (i, j)

        key_cells = set()
        for i in range(n):
            key_cells.add((i, i))

        for pos in [tp_max_pos, tp_min_pos, tn_max_pos, tn_min_pos, combined_max_pos, combined_min_pos]:
            if pos:
                i, j = pos
                if abs(i - j) != 1:
                    key_cells.add(pos)

        return key_cells

    def plot_heatmap(self):
        fig, axes = plt.subplots(1, 4, figsize=(24, 7), dpi=300)

        union_tp = self.create_matrix('TP', 'union')
        union_tn = self.create_matrix('TN', 'union')
        inter_tp = self.create_matrix('TP', 'intersection')
        inter_tn = self.create_matrix('TN', 'intersection')

        union_keys = self.find_key_cells(union_tp, union_tn)
        inter_keys = self.find_key_cells(inter_tp, inter_tn)

        configs = [
            (union_tp, '(a) Union: TP', 'Greens', union_keys),
            (union_tn, '(b) Union: TN', 'Blues', union_keys),
            (inter_tp, '(c) Intersection: TP', 'Oranges', inter_keys),
            (inter_tn, '(d) Intersection: TN', 'Purples', inter_keys),
        ]

        n = len(TOOL_KEYS)

        for idx, (matrix, title, cmap, key_cells) in enumerate(configs):
            ax = axes[idx]

            annot_matrix = np.empty((n, n), dtype=object)
            for i in range(n):
                for j in range(n):
                    if (i, j) in key_cells:
                        annot_matrix[i, j] = f'{int(matrix[i, j])}'
                    else:
                        annot_matrix[i, j] = ''

            sns.heatmap(matrix, ax=ax, cmap=cmap,
                       annot=annot_matrix, fmt='',
                       annot_kws={'size': 12, 'weight': 'bold', 'family': 'serif'},
                       xticklabels=TOOL_LABELS, yticklabels=TOOL_LABELS,
                       cbar_kws={'shrink': 0.8, 'aspect': 20},
                       linewidths=0.5, linecolor='white')

            ax.set_title(title, fontsize=18, fontweight='bold', pad=12, family='serif')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=13, family='serif')
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=13, family='serif')
            ax.set_aspect('equal')

            for i in range(n):
                ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False, edgecolor='#333333', linewidth=1.5))

        plt.tight_layout(pad=1.0)

        STATISTIC_DIR.mkdir(parents=True, exist_ok=True)
        for fmt in ['png', 'pdf']:
            output_file = STATISTIC_DIR / f'fig_heatmap_1x4.{fmt}'
            plt.savefig(output_file, dpi=300 if fmt == 'png' else None,
                       bbox_inches='tight', facecolor='white', edgecolor='none')
            print(f"Saved: {output_file}")

        plt.close()


def main():
    print("RQ4: Heatmap Visualization (1x4 Layout)")
    print("=" * 60)

    benign_skip_list = load_skip_list(BENIGN_SKIP_LIST_PATH)
    print(f"Skip list: {len(benign_skip_list)} packages")

    stats_file = STATISTIC_DIR / 'combination_statistics.csv'
    if not stats_file.exists():
        print(f"Error: {stats_file} not found. Run tool_complement_analysis.py first.")
        return

    print("Generating heatmap...")
    visualizer = HeatmapVisualizer(stats_file, benign_skip_list)
    visualizer.plot_heatmap()
    print("Done!")


if __name__ == "__main__":
    main()
