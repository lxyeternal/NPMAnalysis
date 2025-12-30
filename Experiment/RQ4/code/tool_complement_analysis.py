#!/usr/bin/env python3
"""
RQ4: Tool Complement Analysis - Union/Intersection strategies
"""

import os
import json
import pandas as pd
from pathlib import Path
from itertools import combinations

RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"
BENIGN_SKIP_LIST_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/selected_benign_packages.txt"
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = SCRIPT_DIR.parent / "statistic"


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


def load_tool_predictions(tool_config, benign_skip_list):
    results = {}
    base_path, analyze_func = tool_config["path"], tool_config["func"]

    for file_path, package_key in find_package_files(base_path, "benign"):
        if package_key in benign_skip_list:
            continue
        prediction = analyze_func(file_path)
        if prediction:
            results[package_key] = {'prediction': prediction, 'actual': 'benign'}

    for file_path, package_key in find_package_files(base_path, "malware"):
        prediction = analyze_func(file_path)
        if prediction:
            results[package_key] = {'prediction': prediction, 'actual': 'malware'}

    return results


def load_cerebro_predictions(benign_skip_list):
    csv_path = os.path.join(RESULTS_DIR, "cerebro", "evaluation_npm_with_label.csv")
    if not os.path.exists(csv_path):
        return {}

    df = pd.read_csv(csv_path)
    results = {}

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
        results[package_key] = {'prediction': prediction, 'actual': actual}

    return results


def load_malpacdetector_predictions(algo, benign_skip_list):
    csv_path = os.path.join(RESULTS_DIR, "MalPacDetector", "summary_detection_results.csv")
    if not os.path.exists(csv_path):
        return {}

    df = pd.read_csv(csv_path)
    results = {}

    for _, row in df.iterrows():
        package_key = f"{row['package_name'].replace('##', '/')}/{row['version']}"
        actual = 'malware' if row['actual_label'] == 'malware' else 'benign'
        if actual == 'benign' and package_key in benign_skip_list:
            continue
        prediction = 'malware' if row[algo] == 'malicious' else 'benign'
        results[package_key] = {'prediction': prediction, 'actual': actual}

    return results


def combine_predictions(pred1, pred2, strategy):
    if strategy == 'union':
        return 'malware' if pred1 == 'malware' or pred2 == 'malware' else 'benign'
    return 'malware' if pred1 == 'malware' and pred2 == 'malware' else 'benign'


def calculate_metrics(tp, tn, fp, fn):
    total = tp + tn + fp + fn
    if total == 0:
        return {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1': 0,
                'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn, 'total': total}

    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1,
            'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn, 'total': total}


def analyze_combination(tool1_name, tool2_name, tool1_data, tool2_data, strategy):
    common_packages = set(tool1_data.keys()) & set(tool2_data.keys())
    tp = tn = fp = fn = 0

    for pkg in common_packages:
        combined = combine_predictions(tool1_data[pkg]['prediction'],
                                       tool2_data[pkg]['prediction'], strategy)
        actual = tool1_data[pkg]['actual']

        if combined == 'malware' and actual == 'malware':
            tp += 1
        elif combined == 'benign' and actual == 'benign':
            tn += 1
        elif combined == 'malware' and actual == 'benign':
            fp += 1
        else:
            fn += 1

    metrics = calculate_metrics(tp, tn, fp, fn)
    metrics.update({'tool1': tool1_name, 'tool2': tool2_name,
                   'strategy': strategy, 'common_samples': len(common_packages)})
    return metrics


def main():
    print("RQ4: Tool Complement Analysis")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    benign_skip_list = load_skip_list(BENIGN_SKIP_LIST_PATH)
    print(f"Skip list: {len(benign_skip_list)} packages")

    print("\nLoading tool predictions...")
    all_tool_data = {}

    for tool_name, tool_config in TOOLS_CONFIG.items():
        if os.path.exists(tool_config["path"]):
            all_tool_data[tool_name] = load_tool_predictions(tool_config, benign_skip_list)
            print(f"  {tool_name}: {len(all_tool_data[tool_name])} samples")

    cerebro_data = load_cerebro_predictions(benign_skip_list)
    if cerebro_data:
        all_tool_data['cerebro'] = cerebro_data
        print(f"  cerebro: {len(cerebro_data)} samples")

    for algo in ['MLP', 'NB', 'SVM']:
        mal_data = load_malpacdetector_predictions(algo, benign_skip_list)
        if mal_data:
            all_tool_data[f'malpacdetector_{algo.lower()}'] = mal_data
            print(f"  malpacdetector_{algo.lower()}: {len(mal_data)} samples")

    print("\nAnalyzing combinations...")
    results = []
    tool_names = list(all_tool_data.keys())

    for tool1, tool2 in combinations(tool_names, 2):
        for strategy in ['union', 'intersection']:
            metrics = analyze_combination(tool1, tool2, all_tool_data[tool1],
                                         all_tool_data[tool2], strategy)
            results.append(metrics)

    df = pd.DataFrame(results)
    csv_path = OUTPUT_DIR / "combination_statistics.csv"
    df.to_csv(csv_path, index=False)
    print(f"\nSaved: {csv_path}")

    print("\nTop 10 combinations (by F1):")
    for i, row in df.sort_values('f1', ascending=False).head(10).iterrows():
        print(f"  {row['tool1']} + {row['tool2']} ({row['strategy']}): F1={row['f1']:.4f}")


if __name__ == "__main__":
    main()
