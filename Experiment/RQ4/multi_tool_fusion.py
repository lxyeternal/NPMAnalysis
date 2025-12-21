#!/usr/bin/env python3
"""
RQ4: Multi-Tool Fusion Strategy Evaluation

Evaluates different fusion strategies for combining multiple NPM malware detection tools:
- Majority Voting (various thresholds)
- Weighted Voting (F1-based weights)
- Conservative-Aggressive Fusion
- Unanimous Voting
"""

import os
import glob
from collections import Counter


RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"
BENIGN_SKIP_LIST_PATH = "/home2/wenbo/Documents/NPMAnalysis/Core/Data/cleaning/selected_benign_packages.txt"


def load_skip_list(file_path):
    """Load list of packages to skip."""
    skip_list = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():
                    skip_list.add(line.strip())
    return skip_list


def analyze_guarddog(file_path):
    """Analyze guarddog result. Returns 'benign' if no malicious indicators found."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "Found 0 potentially malicious indicators" in content:
                return "benign"
            return "malware"
    except:
        return None


def analyze_ossgadget(file_path):
    """Analyze ossgadget result. Returns 'benign' if 0 matches found."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "0 matches found." in content:
                return "benign"
            return "malware"
    except:
        return None


def analyze_packj(file_path):
    """Analyze packj result. Returns 'benign' if empty or no risks found."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if not content.strip() or "No risks found!" in content:
                return "benign"
            return "malware"
    except:
        return None


def analyze_genie(file_path):
    """Analyze genie result. Returns 'benign' if csv file is empty."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if not content.strip():
                return "benign"
            return "malware"
    except:
        return None


def convert_package_name(dir_name):
    """Convert directory package name format to standard format."""
    return dir_name.replace('##', '/')


def find_package_files(base_path, package_type):
    """Find all result files in a directory."""
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
                result_file = os.path.join(version_dir, files[0])
                standard_name = convert_package_name(package_name)
                package_key = f"{standard_name}/{version}"
                result.append((result_file, package_key))

    return result


class MultiToolFusion:
    def __init__(self, benign_skip_list=None):
        self.tool_results = {}  # {sample_id: {tool_name: prediction}}
        self.ground_truth = {}  # {sample_id: true_label}
        self.tool_names = ['ossgadget', 'guarddog', 'genie', 'packj_static', 'packj_trace']
        self.benign_skip_list = benign_skip_list or set()
        self.skipped_samples = {'malware': 0, 'benign': 0}

    def should_skip_sample(self, package_key, true_label):
        """Check if sample should be skipped."""
        if true_label == 'benign' and package_key in self.benign_skip_list:
            return True
        return False

    def collect_tool_results(self, sample_id, package_key, tool_predictions, true_label):
        """Collect detection results for a single sample."""
        if self.should_skip_sample(package_key, true_label):
            self.skipped_samples[true_label] += 1
            return False

        self.tool_results[sample_id] = tool_predictions
        self.ground_truth[sample_id] = true_label
        return True

    def calculate_single_tool_performance(self):
        """Calculate performance for each individual tool."""
        performance = {}

        for tool in self.tool_names:
            tp = tn = fp = fn = 0

            for sample_id in self.tool_results:
                if tool not in self.tool_results[sample_id]:
                    continue

                pred = self.tool_results[sample_id][tool]
                true = self.ground_truth[sample_id]

                if pred == 'malware' and true == 'malware':
                    tp += 1
                elif pred == 'benign' and true == 'benign':
                    tn += 1
                elif pred == 'malware' and true == 'benign':
                    fp += 1
                elif pred == 'benign' and true == 'malware':
                    fn += 1

            total = tp + tn + fp + fn
            if total > 0:
                accuracy = (tp + tn) / total
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
                fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

                performance[tool] = {
                    'accuracy': accuracy, 'precision': precision, 'recall': recall,
                    'f1': f1, 'fpr': fpr, 'fnr': fnr,
                    'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn
                }

        return performance

    def majority_voting(self, threshold_ratio=0.5):
        """Majority voting fusion strategy."""
        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
        threshold = max(1, int(len(self.tool_names) * threshold_ratio))

        for sample_id in self.tool_results:
            malware_votes = 0
            total_votes = 0

            for tool in self.tool_names:
                if tool in self.tool_results[sample_id] and self.tool_results[sample_id][tool] is not None:
                    total_votes += 1
                    if self.tool_results[sample_id][tool] == 'malware':
                        malware_votes += 1

            if total_votes == 0:
                continue

            fusion_pred = 'malware' if malware_votes >= threshold else 'benign'
            true_label = self.ground_truth[sample_id]

            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1

        return self._calculate_metrics(results)

    def weighted_voting(self, weights=None):
        """Weighted voting fusion strategy."""
        if weights is None:
            performance = self.calculate_single_tool_performance()
            weights = {}
            total_f1 = sum(performance[tool]['f1'] for tool in performance if performance[tool]['f1'] > 0)
            for tool in self.tool_names:
                if tool in performance and total_f1 > 0:
                    weights[tool] = performance[tool]['f1'] / total_f1
                else:
                    weights[tool] = 1 / len(self.tool_names)

        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}

        for sample_id in self.tool_results:
            weighted_score = 0
            total_weight = 0

            for tool in self.tool_names:
                if tool in self.tool_results[sample_id] and self.tool_results[sample_id][tool] is not None and tool in weights:
                    if self.tool_results[sample_id][tool] == 'malware':
                        weighted_score += weights[tool]
                    total_weight += weights[tool]

            if total_weight == 0:
                continue

            fusion_pred = 'malware' if weighted_score > total_weight * 0.5 else 'benign'
            true_label = self.ground_truth[sample_id]

            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1

        return self._calculate_metrics(results), weights

    def conservative_aggressive_fusion(self):
        """Conservative-Aggressive fusion strategy."""
        performance = self.calculate_single_tool_performance()

        if not performance:
            return self._calculate_metrics({'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}), None, None

        # Conservative tool: lowest FPR; Aggressive tool: highest recall
        conservative_tool = min(performance.keys(), key=lambda x: performance[x]['fpr'])
        aggressive_tool = max(performance.keys(), key=lambda x: performance[x]['recall'])

        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}

        for sample_id in self.tool_results:
            conservative_pred = self.tool_results[sample_id].get(conservative_tool)
            aggressive_pred = self.tool_results[sample_id].get(aggressive_tool)

            if conservative_pred == 'malware':
                fusion_pred = 'malware'
            elif aggressive_pred is not None:
                fusion_pred = aggressive_pred
            else:
                fusion_pred = 'benign'

            true_label = self.ground_truth[sample_id]

            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1

        return self._calculate_metrics(results), conservative_tool, aggressive_tool

    def unanimous_voting(self):
        """Unanimous voting: all tools must agree."""
        results = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0, 'uncertain': 0}

        for sample_id in self.tool_results:
            predictions = []
            for tool in self.tool_names:
                if tool in self.tool_results[sample_id] and self.tool_results[sample_id][tool] is not None:
                    predictions.append(self.tool_results[sample_id][tool])

            if len(predictions) == 0:
                continue

            if len(set(predictions)) == 1:
                fusion_pred = predictions[0]
            else:
                results['uncertain'] += 1
                continue

            true_label = self.ground_truth[sample_id]

            if fusion_pred == 'malware' and true_label == 'malware':
                results['tp'] += 1
            elif fusion_pred == 'benign' and true_label == 'benign':
                results['tn'] += 1
            elif fusion_pred == 'malware' and true_label == 'benign':
                results['fp'] += 1
            elif fusion_pred == 'benign' and true_label == 'malware':
                results['fn'] += 1

        return self._calculate_metrics(results), results['uncertain']

    def _calculate_metrics(self, results):
        """Calculate performance metrics."""
        tp, tn, fp, fn = results['tp'], results['tn'], results['fp'], results['fn']
        total = tp + tn + fp + fn

        if total == 0:
            return {'accuracy': 0, 'precision': 0, 'recall': 0, 'f1': 0, 'fpr': 0, 'fnr': 0,
                    'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}

        accuracy = (tp + tn) / total
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0

        return {'accuracy': accuracy, 'precision': precision, 'recall': recall, 'f1': f1,
                'fpr': fpr, 'fnr': fnr, 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}

    def comprehensive_evaluation(self):
        """Comprehensive evaluation of all fusion strategies."""
        print("=" * 80)
        print("RQ4: Multi-Tool Fusion Strategy Evaluation")
        print("=" * 80)

        # Dataset statistics
        total_samples = len(self.tool_results)
        malware_samples = sum(1 for label in self.ground_truth.values() if label == 'malware')
        benign_samples = sum(1 for label in self.ground_truth.values() if label == 'benign')

        print(f"\nDataset Statistics:")
        print(f"Total valid samples: {total_samples}")
        print(f"  - Malware samples: {malware_samples}")
        print(f"  - Benign samples: {benign_samples}")
        print(f"Skipped samples: {sum(self.skipped_samples.values())}")
        print(f"  - Skipped malware: {self.skipped_samples['malware']}")
        print(f"  - Skipped benign: {self.skipped_samples['benign']}")

        if total_samples == 0:
            print("Error: No valid samples for analysis!")
            return

        # 1. Single tool performance
        print("\n1. Single Tool Performance:")
        print("-" * 50)
        single_performance = self.calculate_single_tool_performance()

        if not single_performance:
            print("Error: No tool performance data!")
            return

        print("| Tool | Accuracy | Precision | Recall | F1 | FPR | FNR |")
        print("| ---- | -------- | --------- | ------ | -- | --- | --- |")
        for tool, metrics in single_performance.items():
            print(f"| {tool:12} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
                  f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['fpr']:.4f} | {metrics['fnr']:.4f} |")

        # 2. Majority voting
        print("\n2. Majority Voting Strategy:")
        print("-" * 50)
        voting_results = {}
        thresholds = [0.2, 0.4, 0.5, 0.6, 0.8]

        print("| Threshold | Accuracy | Precision | Recall | F1 | FPR | FNR |")
        print("| --------- | -------- | --------- | ------ | -- | --- | --- |")
        for threshold in thresholds:
            metrics = self.majority_voting(threshold)
            voting_results[threshold] = metrics
            print(f"| {threshold:9.1f} | {metrics['accuracy']:.4f} | {metrics['precision']:.4f} | "
                  f"{metrics['recall']:.4f} | {metrics['f1']:.4f} | {metrics['fpr']:.4f} | {metrics['fnr']:.4f} |")

        # 3. Weighted voting
        print("\n3. Weighted Voting Strategy:")
        print("-" * 50)
        weighted_metrics, weights = self.weighted_voting()
        print("Tool weights:")
        for tool, weight in weights.items():
            print(f"  {tool}: {weight:.4f}")

        print(f"\nWeighted Voting Results:")
        print(f"Accuracy: {weighted_metrics['accuracy']:.4f}, Precision: {weighted_metrics['precision']:.4f}")
        print(f"Recall: {weighted_metrics['recall']:.4f}, F1: {weighted_metrics['f1']:.4f}")
        print(f"FPR: {weighted_metrics['fpr']:.4f}, FNR: {weighted_metrics['fnr']:.4f}")

        # 4. Conservative-Aggressive fusion
        print("\n4. Conservative-Aggressive Fusion:")
        print("-" * 50)
        ca_metrics, conservative_tool, aggressive_tool = self.conservative_aggressive_fusion()
        if conservative_tool and aggressive_tool:
            print(f"Conservative tool (lowest FPR): {conservative_tool}")
            print(f"Aggressive tool (highest recall): {aggressive_tool}")
            print(f"Accuracy: {ca_metrics['accuracy']:.4f}, Precision: {ca_metrics['precision']:.4f}")
            print(f"Recall: {ca_metrics['recall']:.4f}, F1: {ca_metrics['f1']:.4f}")
            print(f"FPR: {ca_metrics['fpr']:.4f}, FNR: {ca_metrics['fnr']:.4f}")

        # 5. Unanimous voting
        print("\n5. Unanimous Voting Strategy:")
        print("-" * 50)
        unanimous_metrics, uncertain_count = self.unanimous_voting()
        print(f"Uncertain samples: {uncertain_count}")
        print(f"Accuracy: {unanimous_metrics['accuracy']:.4f}, Precision: {unanimous_metrics['precision']:.4f}")
        print(f"Recall: {unanimous_metrics['recall']:.4f}, F1: {unanimous_metrics['f1']:.4f}")
        print(f"FPR: {unanimous_metrics['fpr']:.4f}, FNR: {unanimous_metrics['fnr']:.4f}")

        # 6. Comparison summary
        print("\n6. Strategy Comparison Summary:")
        print("-" * 50)

        best_single_tool = max(single_performance.keys(), key=lambda x: single_performance[x]['f1'])
        best_single_f1 = single_performance[best_single_tool]['f1']

        best_voting_threshold = max(voting_results.keys(), key=lambda x: voting_results[x]['f1'])
        best_voting_f1 = voting_results[best_voting_threshold]['f1']

        comparison_data = [
            ("Best Single Tool", best_single_f1, single_performance[best_single_tool]),
            (f"Majority Vote ({best_voting_threshold})", best_voting_f1, voting_results[best_voting_threshold]),
            ("Weighted Voting", weighted_metrics['f1'], weighted_metrics),
            ("Unanimous Voting", unanimous_metrics['f1'], unanimous_metrics)
        ]

        if conservative_tool and aggressive_tool:
            comparison_data.append(("Conservative-Aggressive", ca_metrics['f1'], ca_metrics))

        comparison_data.sort(key=lambda x: x[1], reverse=True)

        print("| Strategy | F1 | Accuracy | Precision | Recall | FPR | FNR |")
        print("| -------- | -- | -------- | --------- | ------ | --- | --- |")
        for strategy, f1, metrics in comparison_data:
            print(f"| {strategy:20} | {f1:.4f} | {metrics['accuracy']:.4f} | "
                  f"{metrics['precision']:.4f} | {metrics['recall']:.4f} | "
                  f"{metrics['fpr']:.4f} | {metrics['fnr']:.4f} |")

        # 7. Conclusions
        print("\n7. RQ4 Summary:")
        print("-" * 50)
        best_strategy = comparison_data[0]
        improvement = (best_strategy[1] - best_single_f1) / best_single_f1 * 100 if best_single_f1 > 0 else 0

        print(f"Best fusion strategy: {best_strategy[0]}")
        print(f"Improvement over best single tool: {improvement:.2f}%")
        print(f"Tool complementarity: {'Effective' if improvement > 5 else 'Limited'}")

        if improvement > 5:
            print(f"Recommendation: Use {best_strategy[0]} for multi-tool fusion detection")
        else:
            print(f"Recommendation: Limited fusion benefit, prioritize single tool optimization")

        return comparison_data


def collect_all_tool_results(benign_skip_list):
    """Collect detection results from all tools for all samples."""
    fusion_evaluator = MultiToolFusion(benign_skip_list)

    tools_config = {
        "ossgadget": (os.path.join(RESULTS_DIR, "ossgadget"), analyze_ossgadget),
        "guarddog": (os.path.join(RESULTS_DIR, "guarddog"), analyze_guarddog),
        "genie": (os.path.join(RESULTS_DIR, "genie"), analyze_genie),
        "packj_static": (os.path.join(RESULTS_DIR, "packj", "result_static"), analyze_packj),
        "packj_trace": (os.path.join(RESULTS_DIR, "packj", "result_trace"), analyze_packj),
    }

    print("Collecting tool detection results...")

    # Use ossgadget as base to enumerate samples
    base_tool = "ossgadget"
    base_path = tools_config[base_tool][0]

    sample_count = 0

    # Process benign and malware samples
    for label in ["benign", "malware"]:
        base_files = find_package_files(base_path, label)

        for file_path, package_key in base_files:
            sample_id = f"{label}_{package_key}"
            tool_predictions = {}

            # Collect results from all tools
            for tool_name, (tool_path, analyze_func) in tools_config.items():
                try:
                    tool_file_path = file_path.replace(base_path, tool_path)
                    if os.path.exists(tool_file_path):
                        result = analyze_func(tool_file_path)
                        if result is not None:
                            tool_predictions[tool_name] = result
                except Exception:
                    continue

            # Only collect if at least 2 tools have results
            if len(tool_predictions) >= 2:
                if fusion_evaluator.collect_tool_results(sample_id, package_key, tool_predictions, label):
                    sample_count += 1

    print(f"Collected {sample_count} samples with multi-tool results")
    return fusion_evaluator


def main():
    """Main function."""
    benign_skip_list = load_skip_list(BENIGN_SKIP_LIST_PATH)
    print(f"Loaded {len(benign_skip_list)} benign packages to skip")
    print("-" * 50)

    fusion_evaluator = collect_all_tool_results(benign_skip_list)

    if len(fusion_evaluator.tool_results) > 0:
        fusion_evaluator.comprehensive_evaluation()
    else:
        print("Error: No valid tool detection results collected!")
        print("Please check:")
        print(f"1. Results directory: {RESULTS_DIR}")
        print("2. Tool output files exist")
        print("3. File formats are correct")


if __name__ == "__main__":
    main()
