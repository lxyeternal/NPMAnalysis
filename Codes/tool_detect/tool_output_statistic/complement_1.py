import json
import os
from pathlib import Path
from itertools import combinations
import pandas as pd

class ToolComplementAnalyzer:
    def __init__(self, base_dir, output_dir):
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # JSON file types
        self.file_types = [
            'benign_reports.json',
            'false_negatives.json', 
            'false_positives.json',
            'malicious_reports.json'
        ]
        
    def load_tool_data(self, tool_name):
        """Load all JSON files for a specific tool"""
        tool_path = self.base_dir / tool_name
        tool_data = {}
        
        for file_type in self.file_types:
            file_path = tool_path / file_type
            if file_path.exists():
                with open(file_path, 'r') as f:
                    tool_data[file_type] = json.load(f)
            else:
                tool_data[file_type] = {}
                
        return tool_data
    
    def get_all_packages(self, tool1_data, tool2_data):
        """Get all unique packages from both tools"""
        all_packages = set()
        
        for tool_data in [tool1_data, tool2_data]:
            for file_type in self.file_types:
                all_packages.update(tool_data[file_type].keys())
                
        return all_packages
    
    def get_package_info(self, package, tool_data):
        """Get package information from tool data"""
        for file_type in self.file_types:
            if package in tool_data[file_type]:
                return tool_data[file_type][package]
        return None
    
    def combine_predictions(self, pred1, pred2, strategy='union'):
        """
        Combine predictions from two tools
        strategy: 'union' (either tool detects malware) or 'intersection' (both tools detect malware)
        """
        if strategy == 'union':
            # If either tool predicts malware, combined prediction is malware
            return 'malware' if pred1 == 'malware' or pred2 == 'malware' else 'benign'
        elif strategy == 'intersection':
            # Both tools must predict malware for combined prediction to be malware
            return 'malware' if pred1 == 'malware' and pred2 == 'malware' else 'benign'
        
    def merge_tools(self, tool1_name, tool2_name, strategy='union'):
        """Merge results from two tools"""
        tool1_data = self.load_tool_data(tool1_name)
        tool2_data = self.load_tool_data(tool2_name)
        
        all_packages = self.get_all_packages(tool1_data, tool2_data)
        
        # Initialize combined results
        combined_results = {
            'benign_reports.json': {},
            'false_negatives.json': {},
            'false_positives.json': {},
            'malicious_reports.json': {}
        }
        
        for package in all_packages:
            info1 = self.get_package_info(package, tool1_data)
            info2 = self.get_package_info(package, tool2_data)
            
            # Default values if package not found in a tool
            pred1 = info1['prediction'] if info1 else 'benign'
            pred2 = info2['prediction'] if info2 else 'benign'
            actual = info1['actual'] if info1 else (info2['actual'] if info2 else 'unknown')
            
            # Skip if actual label is unknown
            if actual == 'unknown':
                continue
                
            # Combine predictions
            combined_pred = self.combine_predictions(pred1, pred2, strategy)
            
            # Create package entry
            package_entry = {
                'prediction': combined_pred,
                'actual': actual,
                'tool1_prediction': pred1,
                'tool2_prediction': pred2
            }
            
            # Categorize the result
            if combined_pred == 'benign' and actual == 'benign':
                combined_results['benign_reports.json'][package] = package_entry
            elif combined_pred == 'malware' and actual == 'malware':
                combined_results['malicious_reports.json'][package] = package_entry
            elif combined_pred == 'benign' and actual == 'malware':
                combined_results['false_negatives.json'][package] = package_entry
            elif combined_pred == 'malware' and actual == 'benign':
                combined_results['false_positives.json'][package] = package_entry
                
        return combined_results
    
    def save_combined_results(self, combined_results, tool1_name, tool2_name, strategy):
        """Save combined results to files"""
        combo_name = f"{tool1_name}_{tool2_name}_{strategy}"
        combo_dir = self.output_dir / combo_name
        combo_dir.mkdir(parents=True, exist_ok=True)
        
        for file_type, data in combined_results.items():
            output_file = combo_dir / file_type
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        return combo_name, combo_dir
    
    def calculate_metrics(self, combined_results):
        """Calculate performance metrics"""
        tp = len(combined_results['malicious_reports.json'])  # True Positives
        tn = len(combined_results['benign_reports.json'])     # True Negatives
        fp = len(combined_results['false_positives.json'])    # False Positives
        fn = len(combined_results['false_negatives.json'])    # False Negatives
        
        total = tp + tn + fp + fn
        
        if total == 0:
            return {
                'precision': 0, 'recall': 0, 'f1_score': 0,
                'accuracy': 0, 'specificity': 0,
                'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn, 'total': total
            }
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / total
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'accuracy': accuracy,
            'specificity': specificity,
            'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn,
            'total': total
        }
    
    def analyze_all_combinations(self, strategies=['union', 'intersection']):
        """Analyze all tool combinations"""
        # Get all tool directories
        tool_dirs = [d for d in self.base_dir.iterdir() if d.is_dir()]
        tool_names = [d.name for d in tool_dirs]
        
        print(f"Found tools: {tool_names}")
        
        statistics = []
        
        # Generate all combinations of tools
        for tool1, tool2 in combinations(tool_names, 2):
            for strategy in strategies:
                print(f"Processing combination: {tool1} + {tool2} ({strategy})")
                
                try:
                    # Merge tools
                    combined_results = self.merge_tools(tool1, tool2, strategy)
                    
                    # Save results
                    combo_name, combo_dir = self.save_combined_results(
                        combined_results, tool1, tool2, strategy
                    )
                    
                    # Calculate metrics
                    metrics = self.calculate_metrics(combined_results)
                    
                    # Add to statistics
                    stat_entry = {
                        'tool1': tool1,
                        'tool2': tool2,
                        'strategy': strategy,
                        'combination_name': combo_name,
                        **metrics
                    }
                    statistics.append(stat_entry)
                    
                    print(f"  Completed: {combo_name}")
                    print(f"  Accuracy: {metrics['accuracy']:.3f}, F1: {metrics['f1_score']:.3f}")
                    
                except Exception as e:
                    print(f"Error processing {tool1} + {tool2} ({strategy}): {e}")
        
        return statistics
    
    def save_statistics(self, statistics):
        """Save statistics to CSV and JSON files"""
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(statistics)
        
        # Save as CSV
        csv_file = self.output_dir / 'combination_statistics.csv'
        df.to_csv(csv_file, index=False)
        
        # Save as JSON
        json_file = self.output_dir / 'combination_statistics.json'
        with open(json_file, 'w') as f:
            json.dump(statistics, f, indent=2)
        
        # Create summary statistics
        summary_stats = {
            'total_combinations': len(statistics),
            'best_accuracy': df['accuracy'].max() if not df.empty else 0,
            'best_f1_score': df['f1_score'].max() if not df.empty else 0,
            'average_accuracy': df['accuracy'].mean() if not df.empty else 0,
            'average_f1_score': df['f1_score'].mean() if not df.empty else 0
        }
        
        if not df.empty:
            best_accuracy_combo = df.loc[df['accuracy'].idxmax()]
            best_f1_combo = df.loc[df['f1_score'].idxmax()]
            
            summary_stats['best_accuracy_combination'] = {
                'tools': f"{best_accuracy_combo['tool1']} + {best_accuracy_combo['tool2']}",
                'strategy': best_accuracy_combo['strategy'],
                'accuracy': best_accuracy_combo['accuracy']
            }
            
            summary_stats['best_f1_combination'] = {
                'tools': f"{best_f1_combo['tool1']} + {best_f1_combo['tool2']}",
                'strategy': best_f1_combo['strategy'],
                'f1_score': best_f1_combo['f1_score']
            }
        
        # Save summary
        summary_file = self.output_dir / 'summary_statistics.json'
        with open(summary_file, 'w') as f:
            json.dump(summary_stats, f, indent=2)
        
        print(f"\nStatistics saved to:")
        print(f"  CSV: {csv_file}")
        print(f"  JSON: {json_file}")
        print(f"  Summary: {summary_file}")
        
        return summary_stats

def main():
    # Configuration
    base_directory = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    output_directory = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/complement"
    
    # Initialize analyzer
    analyzer = ToolComplementAnalyzer(base_directory, output_directory)
    
    # Analyze all combinations
    print("Starting tool combination analysis...")
    statistics = analyzer.analyze_all_combinations(['union', 'intersection'])
    
    # Save statistics
    summary = analyzer.save_statistics(statistics)
    
    # Print summary
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    print(f"Total combinations analyzed: {summary['total_combinations']}")
    print(f"Best accuracy: {summary['best_accuracy']:.3f}")
    print(f"Best F1 score: {summary['best_f1_score']:.3f}")
    print(f"Average accuracy: {summary['average_accuracy']:.3f}")
    print(f"Average F1 score: {summary['average_f1_score']:.3f}")
    
    if 'best_accuracy_combination' in summary:
        print(f"\nBest accuracy combination:")
        print(f"  Tools: {summary['best_accuracy_combination']['tools']}")
        print(f"  Strategy: {summary['best_accuracy_combination']['strategy']}")
        print(f"  Accuracy: {summary['best_accuracy_combination']['accuracy']:.3f}")
    
    if 'best_f1_combination' in summary:
        print(f"\nBest F1 score combination:")
        print(f"  Tools: {summary['best_f1_combination']['tools']}")
        print(f"  Strategy: {summary['best_f1_combination']['strategy']}")
        print(f"  F1 Score: {summary['best_f1_combination']['f1_score']:.3f}")
    
    print(f"\nAll results saved to: {output_directory}")

if __name__ == "__main__":
    main()