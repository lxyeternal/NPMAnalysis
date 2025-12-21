#!/usr/bin/env python3
"""
RQ1: NPM Malware Detection Tool Accuracy Evaluation

This script evaluates the detection accuracy of multiple NPM malware detection tools:
- Rule-based: GuardDog, OSSGadget, Genie, Socket.AI
- Hybrid: Packj (static and trace modes)
- ML-based: SAP (DT, RF, XGB), MalPacDetector (MLP, NB, SVM)
"""

import os
import json
import pandas as pd


RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"
BENIGN_SKIP_LIST_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/selected_benign_packages.txt"


def load_skip_list(file_path):
    """Load the list of packages to skip during evaluation."""
    skip_list = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():
                    skip_list.add(line.strip())
    return skip_list


def convert_package_name(dir_name):
    """
    Convert directory package name format to standard format.
    Directory uses '##' for scoped packages, standard format uses '/'.
    """
    return dir_name.replace('##', '/')


def analyze_guarddog(file_path):
    """Returns 'benign' if "Found 0 potentially malicious indicators" is found."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if "Found 0 potentially malicious indicators" in content:
            return "benign"
        return "malware"


def analyze_socketai(file_path):
    """Parses JSON and checks the 'is_malicious' field."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
            if data.get("is_malicious", False):
                return "malware"
            return "benign"
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        return "benign"


def analyze_ossgadget(file_path):
    """Returns 'benign' if "0 matches found." is found."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if "0 matches found." in content:
            return "benign"
        return "malware"


def analyze_packj(file_path):
    """Returns 'benign' if file is empty or contains "No risks found!"."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if not content.strip() or "No risks found!" in content:
            return "benign"
        return "malware"


def analyze_genie(file_path):
    """Returns 'benign' if file is empty, 'malware' otherwise."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if not content.strip():
            return "benign"
        return "malware"


def analyze_sap(file_path):
    """result.txt contains '0' for benign, '1' for malware."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().strip()
        if content == "0":
            return "benign"
        return "malware"


def calculate_metrics(tp, tn, fp, fn):
    """Calculate precision, recall, F1 score and accuracy."""
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


def find_package_files(base_path, package_type):
    """
    Find tool output files. Each version directory should have exactly one result file.
    Returns list of (file_path, package_key) tuples.
    """
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

            # Find the first file in the version directory
            files = [f for f in os.listdir(version_dir) if os.path.isfile(os.path.join(version_dir, f))]
            if files:
                result_file = os.path.join(version_dir, files[0])
                standard_name = convert_package_name(package_name)
                package_key = f"{standard_name}/{version}"
                result.append((result_file, package_key))

    return result


def evaluate_tool(tool_name, tool_function, benign_skip_list, sub_tool=None):
    """Evaluate a specific tool's detection performance."""
    if sub_tool:
        base_path = os.path.join(RESULTS_DIR, tool_name, sub_tool)
    else:
        base_path = os.path.join(RESULTS_DIR, tool_name)

    results = {"tp": 0, "tn": 0, "fp": 0, "fn": 0}

    # Process benign samples
    for file_path, package_key in find_package_files(base_path, "benign"):
        if package_key in benign_skip_list:
            continue
        prediction = tool_function(file_path)
        if prediction == "benign":
            results["tn"] += 1
        else:
            results["fp"] += 1

    # Process malware samples
    for file_path, package_key in find_package_files(base_path, "malware"):
        prediction = tool_function(file_path)
        if prediction == "malware":
            results["tp"] += 1
        else:
            results["fn"] += 1

    results.update(calculate_metrics(results["tp"], results["tn"], results["fp"], results["fn"]))
    return results


def evaluate_malpacdetector(benign_skip_list):
    """Evaluate MalPacDetector from summary CSV file."""
    csv_path = os.path.join(RESULTS_DIR, "MalPacDetector", "summary_detection_results.csv")
    if not os.path.exists(csv_path):
        return {}

    df = pd.read_csv(csv_path)
    df['package_key'] = df['package_name'].apply(convert_package_name) + '/' + df['version']
    df = df[~((df['package_type'] == 'benign') & (df['package_key'].isin(benign_skip_list)))]

    results = {}
    for algo in ['MLP', 'NB', 'SVM']:
        df[f'{algo}_binary'] = df[algo].apply(lambda x: 1 if x == 'malicious' else 0)
        df['actual_binary'] = df['actual_label'].apply(lambda x: 1 if x == 'malware' else 0)

        tp = len(df[(df['actual_binary'] == 1) & (df[f'{algo}_binary'] == 1)])
        tn = len(df[(df['actual_binary'] == 0) & (df[f'{algo}_binary'] == 0)])
        fp = len(df[(df['actual_binary'] == 0) & (df[f'{algo}_binary'] == 1)])
        fn = len(df[(df['actual_binary'] == 1) & (df[f'{algo}_binary'] == 0)])

        metrics = calculate_metrics(tp, tn, fp, fn)
        results[f"MalPacDetector_{algo}"] = {"tp": tp, "tn": tn, "fp": fp, "fn": fn, **metrics}

    return results


def main():
    """Main function to evaluate all tools."""
    benign_skip_list = load_skip_list(BENIGN_SKIP_LIST_PATH)

    tools_config = [
        ("GuardDog", "guarddog", analyze_guarddog, None),
        ("OSSGadget", "ossgadget", analyze_ossgadget, None),
        ("Genie", "genie", analyze_genie, None),
        ("Socket.AI", "socketai", analyze_socketai, None),
        ("Packj_static", "packj", analyze_packj, "result_static"),
        ("Packj_trace", "packj", analyze_packj, "result_trace"),
        ("SAP_DT", "sap", analyze_sap, "DT"),
        ("SAP_RF", "sap", analyze_sap, "RF"),
        ("SAP_XGB", "sap", analyze_sap, "XGB"),
    ]

    all_results = {}
    for display_name, tool_name, tool_func, sub_tool in tools_config:
        all_results[display_name] = evaluate_tool(tool_name, tool_func, benign_skip_list, sub_tool)

    all_results.update(evaluate_malpacdetector(benign_skip_list))

    # Print summary table
    print("\n" + "=" * 100)
    print("NPM Malware Detection Tool Accuracy Evaluation")
    print("=" * 100 + "\n")
    print("| Tool | TP | TN | FP | FN | Accuracy | Precision | Recall | F1 |")
    print("| ---- | -- | -- | -- | -- | -------- | --------- | ------ | -- |")

    for tool_name, r in all_results.items():
        print(f"| {tool_name} | {r['tp']} | {r['tn']} | {r['fp']} | {r['fn']} | "
              f"{r['accuracy']:.4f} | {r['precision']:.4f} | {r['recall']:.4f} | {r['f1']:.4f} |")
    print()


if __name__ == "__main__":
    main()
