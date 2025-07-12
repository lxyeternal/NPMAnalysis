#!/usr/bin/env python3
"""
Evasion Technique Detection Analysis Script

This script analyzes different security tools' capabilities to detect evasion techniques
in malicious NPM packages.

Usage:
    python evasion_detection_analysis.py
"""

import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import glob
from pathlib import Path

# Set up plotting style
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    try:
        plt.style.use('seaborn')
    except OSError:
        plt.style.use('default')
sns.set_palette("husl")

class EvasionDetectionAnalyzer:
    def __init__(self, malware_snippets_dir, stats_output_dir):
        """
        Initialize the analyzer with paths to malware snippets and tool statistics.
        
        Args:
            malware_snippets_dir (str): Path to malware snippets directory
            stats_output_dir (str): Path to tool statistics output directory
        """
        self.malware_snippets_dir = Path(malware_snippets_dir)
        self.stats_output_dir = Path(stats_output_dir)
        
        # Data containers
        self.malware_data = {}
        self.tool_stats = {}
        self.evasion_techniques = set()
        self.package_evasion_map = {}
        
        # Results
        self.analysis_results = {}
        
    def load_malware_data(self):
        """Load all malware package data and extract evasion techniques."""
        print("Loading malware package data...")
        
        # Find all result.json files
        json_files = list(self.malware_snippets_dir.glob("*/*/result.json"))
        
        total_files = len(json_files)
        print(f"Found {total_files} malware packages to analyze")
        
        for i, json_file in enumerate(json_files):
            if i % 100 == 0:
                print(f"Processing {i}/{total_files} files...")
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract package name and version from path
                parts = json_file.parts
                package_name = parts[-3]
                version = parts[-2]
                package_id = f"{package_name}/{version}"
                
                # Store malware data
                self.malware_data[package_id] = data
                
                # Extract evasion techniques
                package_evasions = set()
                
                if 'malicious_snippets' in data:
                    for snippet in data['malicious_snippets']:
                        # Get formal evasion techniques
                        if 'evasion_formal' in snippet:
                            for technique in snippet['evasion_formal']:
                                if technique:  # Skip empty strings
                                    self.evasion_techniques.add(technique)
                                    package_evasions.add(technique)
                
                self.package_evasion_map[package_id] = package_evasions
                
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
                continue
        
        print(f"Loaded {len(self.malware_data)} malware packages")
        print(f"Found {len(self.evasion_techniques)} unique evasion techniques")
        
    def load_tool_stats(self):
        """Load tool detection statistics."""
        print("Loading tool detection statistics...")
        
        tool_dirs = [d for d in self.stats_output_dir.iterdir() if d.is_dir()]
        
        for tool_dir in tool_dirs:
            tool_name = tool_dir.name
            print(f"Loading stats for {tool_name}...")
            
            # Load false negatives (packages that tool failed to detect)
            fn_file = tool_dir / "false_negatives.json"
            fp_file = tool_dir / "false_positives.json"
            
            tool_data = {
                'false_negatives': set(),
                'false_positives': set(),
                'true_positives': set(),
                'true_negatives': set()
            }
            
            if fn_file.exists():
                with open(fn_file, 'r', encoding='utf-8') as f:
                    fn_data = json.load(f)
                    tool_data['false_negatives'] = set(fn_data.keys())
            
            if fp_file.exists():
                with open(fp_file, 'r', encoding='utf-8') as f:
                    fp_data = json.load(f)
                    tool_data['false_positives'] = set(fp_data.keys())
            
            # Calculate true positives (malware packages not in false negatives)
            all_malware_packages = set(self.malware_data.keys())
            tool_data['true_positives'] = all_malware_packages - tool_data['false_negatives']
            
            self.tool_stats[tool_name] = tool_data
            
            print(f"  - False Negatives: {len(tool_data['false_negatives'])}")
            print(f"  - False Positives: {len(tool_data['false_positives'])}")
            print(f"  - True Positives: {len(tool_data['true_positives'])}")
    
    def analyze_evasion_distribution(self):
        """Analyze the distribution of evasion techniques across packages."""
        print("Analyzing evasion technique distribution...")
        
        # Count evasion techniques
        evasion_counts = Counter()
        
        for package_id, evasions in self.package_evasion_map.items():
            for evasion in evasions:
                evasion_counts[evasion] += 1
        
        # Create DataFrame
        if evasion_counts:
            evasion_df = pd.DataFrame([
                {'technique': technique, 'count': count, 'percentage': count / len(self.malware_data) * 100}
                for technique, count in evasion_counts.items()
            ]).sort_values('count', ascending=False)
        else:
            evasion_df = pd.DataFrame(columns=['technique', 'count', 'percentage'])
        
        self.analysis_results['evasion_distribution'] = evasion_df
        
        # Plot distribution if we have data
        if len(evasion_df) > 0:
            plt.figure(figsize=(15, 8))
            top_20 = evasion_df.head(20)
            
            bars = plt.bar(range(len(top_20)), top_20['count'])
            plt.xticks(range(len(top_20)), top_20['technique'], rotation=45, ha='right')
            plt.ylabel('Number of Packages')
            plt.title('Top 20 Most Common Evasion Techniques')
            plt.tight_layout()
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')
            
            plt.savefig('evasion_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Generated evasion distribution plot")
        else:
            print("No evasion techniques found to plot")
        
    def analyze_tool_detection_capabilities(self):
        """Analyze each tool's capability to detect different evasion techniques."""
        print("Analyzing tool detection capabilities...")
        
        # For each tool, calculate detection rates for each evasion technique
        tool_detection_results = {}
        
        for tool_name, tool_data in self.tool_stats.items():
            print(f"Analyzing {tool_name}...")
            
            technique_stats = {}
            
            for technique in self.evasion_techniques:
                # Find packages with this technique
                packages_with_technique = set()
                for package_id, evasions in self.package_evasion_map.items():
                    if technique in evasions:
                        packages_with_technique.add(package_id)
                
                if not packages_with_technique:
                    continue
                
                # Calculate detection statistics
                detected = len(packages_with_technique - tool_data['false_negatives'])
                missed = len(packages_with_technique & tool_data['false_negatives'])
                total = len(packages_with_technique)
                
                detection_rate = detected / total if total > 0 else 0
                
                technique_stats[technique] = {
                    'total_packages': total,
                    'detected': detected,
                    'missed': missed,
                    'detection_rate': detection_rate
                }
            
            tool_detection_results[tool_name] = technique_stats
        
        self.analysis_results['tool_detection'] = tool_detection_results
        
        # Create detection rate comparison
        self._create_detection_rate_heatmap()
        
    def _create_detection_rate_heatmap(self):
        """Create a heatmap showing detection rates for each tool and evasion technique."""
        
        # Prepare data for heatmap
        tools = list(self.tool_stats.keys())
        
        # Get techniques with at least 5 packages
        significant_techniques = []
        for technique in self.evasion_techniques:
            technique_count = sum(1 for evasions in self.package_evasion_map.values() 
                                if technique in evasions)
            if technique_count >= 5:
                significant_techniques.append(technique)
        
        if not significant_techniques:
            print("No techniques found with sufficient packages for heatmap")
            return
        
        # Create detection rate matrix
        detection_matrix = np.zeros((len(tools), len(significant_techniques)))
        
        for i, tool in enumerate(tools):
            for j, technique in enumerate(significant_techniques):
                if technique in self.analysis_results['tool_detection'][tool]:
                    detection_matrix[i, j] = self.analysis_results['tool_detection'][tool][technique]['detection_rate']
        
        # Create heatmap
        plt.figure(figsize=(20, 10))
        sns.heatmap(detection_matrix, 
                   xticklabels=significant_techniques,
                   yticklabels=tools,
                   annot=True, 
                   fmt='.2f',
                   cmap='RdYlGn',
                   vmin=0, 
                   vmax=1)
        
        plt.title('Tool Detection Rates by Evasion Technique')
        plt.xlabel('Evasion Techniques')
        plt.ylabel('Security Tools')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('detection_rate_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Generated detection rate heatmap")
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report."""
        print("Generating summary report...")
        
        report = []
        report.append("# Evasion Technique Detection Analysis Report")
        report.append("=" * 50)
        report.append("")
        
        # Overall statistics
        report.append("## Overall Statistics")
        report.append(f"- Total malware packages analyzed: {len(self.malware_data)}")
        report.append(f"- Total unique evasion techniques: {len(self.evasion_techniques)}")
        report.append(f"- Security tools analyzed: {len(self.tool_stats)}")
        report.append("")
        
        # Top evasion techniques
        report.append("## Top 10 Most Common Evasion Techniques")
        if 'evasion_distribution' in self.analysis_results:
            top_10 = self.analysis_results['evasion_distribution'].head(10)
            for _, row in top_10.iterrows():
                report.append(f"- {row['technique']}: {row['count']} packages ({row['percentage']:.1f}%)")
        report.append("")
        
        # Tool performance summary
        report.append("## Tool Performance Summary")
        for tool_name, tool_data in self.tool_stats.items():
            total_malware = len(self.malware_data)
            tp = len(tool_data['true_positives'])
            fn = len(tool_data['false_negatives'])
            fp = len(tool_data['false_positives'])
            
            detection_rate = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            report.append(f"### {tool_name}")
            report.append(f"- Detection Rate: {detection_rate:.3f} ({tp}/{tp + fn})")
            report.append(f"- False Negatives: {fn}")
            report.append(f"- False Positives: {fp}")
            report.append("")
        
        # Hardest to detect techniques
        report.append("## Hardest to Detect Evasion Techniques")
        if 'tool_detection' in self.analysis_results:
            # Calculate average detection rate for each technique
            technique_avg_detection = {}
            for technique in self.evasion_techniques:
                detection_rates = []
                for tool_name in self.tool_stats:
                    if technique in self.analysis_results['tool_detection'][tool_name]:
                        detection_rates.append(
                            self.analysis_results['tool_detection'][tool_name][technique]['detection_rate']
                        )
                
                if detection_rates:
                    technique_avg_detection[technique] = np.mean(detection_rates)
            
            # Sort by detection rate (ascending)
            sorted_techniques = sorted(technique_avg_detection.items(), key=lambda x: x[1])
            
            report.append("Top 10 techniques with lowest average detection rates:")
            for technique, avg_rate in sorted_techniques[:10]:
                report.append(f"- {technique}: {avg_rate:.3f} average detection rate")
        
        report.append("")
        
        # Best detected techniques
        report.append("## Best Detected Evasion Techniques")
        if 'tool_detection' in self.analysis_results:
            report.append("Top 10 techniques with highest average detection rates:")
            for technique, avg_rate in sorted_techniques[-10:]:
                report.append(f"- {technique}: {avg_rate:.3f} average detection rate")
        
        # Save report
        with open('evasion_detection_report.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print("Summary report generated: evasion_detection_report.txt")
        
    def save_detailed_results(self):
        """Save detailed results to JSON and CSV files."""
        print("Saving detailed results...")
        
        # Save evasion distribution
        if 'evasion_distribution' in self.analysis_results:
            self.analysis_results['evasion_distribution'].to_csv('evasion_distribution.csv', index=False)
        
        # Save tool detection results
        if 'tool_detection' in self.analysis_results:
            # Convert to DataFrame for easier analysis
            detailed_results = []
            for tool_name, tool_data in self.analysis_results['tool_detection'].items():
                for technique, stats in tool_data.items():
                    detailed_results.append({
                        'tool': tool_name,
                        'technique': technique,
                        'total_packages': stats['total_packages'],
                        'detected': stats['detected'],
                        'missed': stats['missed'],
                        'detection_rate': stats['detection_rate']
                    })
            
            results_df = pd.DataFrame(detailed_results)
            results_df.to_csv('tool_detection_detailed.csv', index=False)
        
        # Save package-technique mapping
        package_technique_data = []
        for package_id, techniques in self.package_evasion_map.items():
            for technique in techniques:
                package_technique_data.append({
                    'package_id': package_id,
                    'technique': technique
                })
        
        pd.DataFrame(package_technique_data).to_csv('package_technique_mapping.csv', index=False)
        
        print("Detailed results saved to CSV files")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        print("Starting complete evasion detection analysis...")
        
        # Load data
        self.load_malware_data()
        self.load_tool_stats()
        
        # Perform analysis
        self.analyze_evasion_distribution()
        self.analyze_tool_detection_capabilities()
        
        # Generate outputs
        self.generate_summary_report()
        self.save_detailed_results()
        
        print("Analysis complete! Check the generated files:")
        print("- evasion_distribution.png: Distribution of evasion techniques")
        print("- detection_rate_heatmap.png: Tool detection rates heatmap")
        print("- evasion_detection_report.txt: Summary report")
        print("- *.csv files: Detailed data for further analysis")

def main():
    """Main function to run the analysis."""
    
    # Define paths
    malware_snippets_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/code_snipptes/malware_snippets"
    stats_output_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    
    # Create analyzer and run analysis
    analyzer = EvasionDetectionAnalyzer(malware_snippets_dir, stats_output_dir)
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main() 