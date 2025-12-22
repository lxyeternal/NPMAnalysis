#!/usr/bin/env python3
"""
Category-based Evasion Detection Analysis Script

This script analyzes different security tools' capabilities to detect evasion technique categories
in malicious NPM packages using the new classification system.

Usage:
    python evasion_detection_analysis_classified_v2.py
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
import matplotlib.patches as mpatches

# Set up plotting style
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    try:
        plt.style.use('seaborn')
    except OSError:
        plt.style.use('default')
sns.set_palette("husl")

# 设置全局字体大小
plt.rcParams.update({'font.size': 18})
plt.rcParams.update({'axes.labelsize': 20})
plt.rcParams.update({'axes.titlesize': 24})
plt.rcParams.update({'xtick.labelsize': 18})
plt.rcParams.update({'ytick.labelsize': 18})
plt.rcParams.update({'legend.fontsize': 18})

class CategoryBasedEvasionAnalyzer:
    def __init__(self, malware_snippets_dir, stats_output_dir, classification_file, output_dir):
        """
        Initialize the analyzer with paths and classification system.
        
        Args:
            malware_snippets_dir (str): Path to malware snippets directory
            stats_output_dir (str): Path to tool statistics output directory
            classification_file (str): Path to evasion classification CSV
            output_dir (str): Path for output files
        """
        self.malware_snippets_dir = Path(malware_snippets_dir)
        self.stats_output_dir = Path(stats_output_dir)
        self.classification_file = Path(classification_file)
        self.output_dir = Path(output_dir)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Data containers
        self.malware_data = {}
        self.tool_stats = {}
        self.package_category_map = {}
        self.technique_to_category = {}
        self.categories = {}
        
        # Results
        self.analysis_results = {}
        
    def load_classification_mapping(self):
        """Load the evasion technique classification mapping."""
        print("Loading evasion technique classification...")
        
        df_classification = pd.read_csv(self.classification_file)
        
        # Create mapping from technique to category
        for _, row in df_classification.iterrows():
            category = str(row['category'])
            techniques_str = str(row['techniques'])
            techniques = [t.strip() for t in techniques_str.split(',') if t.strip()]
            
            # Store category info
            self.categories[category] = {
                'techniques': techniques,
                'count': int(row['count']),
                'percentage': float(row['percentage']),
                'description': str(row['description'])
            }
            
            # Create technique to category mapping
            for technique in techniques:
                self.technique_to_category[technique] = category
        
        print(f"Loaded {len(self.categories)} evasion categories")
        print(f"Mapped {len(self.technique_to_category)} techniques to categories")
        
    def load_malware_data(self):
        """Load all malware package data and extract evasion categories."""
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
                
                # Extract evasion categories from techniques (skip unknown techniques)
                package_categories = set()
                
                if 'malicious_snippets' in data:
                    for snippet in data['malicious_snippets']:
                        # Get formal evasion techniques
                        if 'validate_evasion_formal' in snippet:
                            for technique in snippet['validate_evasion_formal']:
                                if technique and technique.strip():
                                    technique = technique.strip()
                                    # Map technique to category (skip unknown techniques)
                                    if technique in self.technique_to_category:
                                        category = self.technique_to_category[technique]
                                        package_categories.add(category)
                                    # Skip unknown techniques completely
                
                # Only include packages with at least one known category
                if len(package_categories) > 0:
                    self.package_category_map[package_id] = package_categories
                
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
                continue
        
        print(f"Loaded {len(self.malware_data)} malware packages")
        print(f"Extracted categories for {len(self.package_category_map)} packages")
        
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
    
    def analyze_category_distribution(self):
        """Analyze the distribution of evasion categories across packages."""
        print("Analyzing evasion category distribution...")
        
        # Count category occurrences
        category_counts = Counter()
        
        for package_id, categories in self.package_category_map.items():
            for category in categories:
                category_counts[category] += 1
        
        # Create DataFrame for category distribution
        if category_counts:
            total_occurrences = sum(category_counts.values())
            category_df = pd.DataFrame([
                {
                    'category': category, 
                    'count': count, 
                    'percentage': count / total_occurrences * 100,
                    'description': self.categories.get(category, {}).get('description', 'Unknown category')
                }
                for category, count in category_counts.items()
            ]).sort_values('count', ascending=False)
        else:
            category_df = pd.DataFrame({
                'category': [],
                'count': [],
                'percentage': [],
                'description': []
            })
        
        self.analysis_results['category_distribution'] = category_df
        
        # Plot category distribution
        if len(category_df) > 0:
            plt.figure(figsize=(18, 13))
            
            # Create vertical bar chart
            x_pos = list(range(len(category_df)))
            counts = category_df['count'].tolist()
            categories = category_df['category'].tolist()
            
            bars = plt.bar(x_pos, counts)
            
            plt.xticks(x_pos, categories, fontsize=26, rotation=30, ha='right')
            plt.yticks(fontsize=26)
            plt.ylabel('Number of Packages', fontsize=32)
            
            # Set white background with grid
            plt.gca().set_facecolor('white')
            plt.gcf().patch.set_facecolor('white')
            plt.grid(True, alpha=0.5, linestyle='-', linewidth=0.5, color='gray')
            
            # Add value labels on bars
            for i, (bar, count) in enumerate(zip(bars, counts)):
                plt.text(bar.get_x() + bar.get_width()/2, 
                        bar.get_height() + max(counts) * 0.01,
                        f'{int(count)}',
                        ha='center', va='bottom', fontsize=28, fontweight='bold')
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'category_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"Generated category distribution plot")
        else:
            print("No categories found to plot")
    
    def analyze_tool_detection_by_category(self):
        """Analyze each tool's capability to detect different evasion categories."""
        print("Analyzing tool detection capabilities by category...")
        
        # For each tool, calculate detection rates for each category
        tool_detection_results = {}
        
        for tool_name, tool_data in self.tool_stats.items():
            print(f"Analyzing {tool_name}...")
            
            category_stats = {}
            
            for category in self.categories.keys():
                # Find packages with this category
                packages_with_category = set()
                
                for package_id, categories in self.package_category_map.items():
                    if category in categories:
                        packages_with_category.add(package_id)
                
                if not packages_with_category:
                    continue
                
                # Calculate detection statistics
                detected = len(packages_with_category - tool_data['false_negatives'])
                missed = len(packages_with_category & tool_data['false_negatives'])
                total = len(packages_with_category)
                
                detection_rate = detected / total if total > 0 else 0
                
                category_stats[category] = {
                    'total_packages': total,
                    'detected': detected,
                    'missed': missed,
                    'detection_rate': detection_rate
                }
            
            tool_detection_results[tool_name] = category_stats
        
        self.analysis_results['tool_detection_by_category'] = tool_detection_results
        
        # Create detection rate heatmap
        self._create_category_detection_heatmap()
        
    def _create_category_detection_heatmap(self):
        """Create a heatmap showing detection rates for each tool and evasion category."""
        
        # Prepare data for heatmap
        tools = list(self.tool_stats.keys())
        categories = list(self.categories.keys())
        
        # Create detection rate matrix
        detection_matrix = np.zeros((len(tools), len(categories)))
        
        for i, tool in enumerate(tools):
            for j, category in enumerate(categories):
                if category in self.analysis_results['tool_detection_by_category'][tool]:
                    detection_matrix[i, j] = self.analysis_results['tool_detection_by_category'][tool][category]['detection_rate']
        
        # Create heatmap
        plt.figure(figsize=(20, 12))
        
        sns.heatmap(detection_matrix, 
                   xticklabels=categories,
                   yticklabels=tools,
                   annot=True, 
                   fmt='.3f',
                   cmap='RdYlGn',
                   vmin=0, 
                   vmax=1,
                   annot_kws={"size": 18, "weight": "bold"})
        
        plt.title('Tool Detection Rates by Evasion Category', fontsize=30, fontweight='bold')
        plt.xlabel('Evasion Categories', fontsize=26)
        plt.ylabel('Security Tools', fontsize=26)
        plt.xticks(rotation=30, ha='right', fontsize=20)
        plt.yticks(fontsize=20)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'category_detection_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Generated category detection rate heatmap")
    
    def analyze_package_complexity(self):
        """Analyze package complexity based on number of categories."""
        print("Analyzing package complexity...")
        
        complexity_data = []
        
        for package_id in self.malware_data.keys():
            categories = self.package_category_map.get(package_id, set())
            
            complexity_data.append({
                'package_id': package_id,
                'category_count': len(categories),
                'categories': ';'.join(sorted(categories))
            })
        
        complexity_df = pd.DataFrame(complexity_data)
        self.analysis_results['package_complexity'] = complexity_df
        
        # Create complexity visualization
        plt.figure(figsize=(16, 10))
        
        # Distribution of category counts
        category_dist = complexity_df['category_count'].value_counts().sort_index()
        
        bars = plt.bar(category_dist.index.tolist(), category_dist.values.tolist())
        plt.xlabel('Number of Evasion Categories', fontsize=20)
        plt.ylabel('Number of Packages', fontsize=20)
        plt.title('Package Complexity Distribution', fontsize=24, fontweight='bold')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=16, fontweight='bold')
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'package_complexity.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Generated package complexity plot")
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive summary report."""
        print("Generating comprehensive report...")
        
        report = []
        report.append("# Category-based Evasion Detection Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        # Overall statistics
        report.append("## Overall Statistics")
        report.append(f"- Total malware packages analyzed: {len(self.malware_data)}")
        report.append(f"- Evasion categories: {len(self.categories)}")
        report.append(f"- Security tools analyzed: {len(self.tool_stats)}")
        report.append("")
        
        # Category statistics
        report.append("## Evasion Category Statistics")
        if 'category_distribution' in self.analysis_results:
            category_df = self.analysis_results['category_distribution']
            report.append("### Top Categories by Occurrence")
            for _, row in category_df.head(10).iterrows():
                report.append(f"- {row['category']}: {row['count']} occurrences ({row['percentage']:.1f}%)")
            report.append("")
        
        # Package complexity analysis
        if 'package_complexity' in self.analysis_results:
            complexity_df = self.analysis_results['package_complexity']
            
            report.append("## Package Complexity Analysis")
            
            # Category count distribution
            category_dist = complexity_df['category_count'].value_counts().sort_index()
            report.append("### Distribution by Number of Categories")
            for count, packages in category_dist.items():
                pct = packages / len(complexity_df) * 100
                report.append(f"- {count} categories: {packages} packages ({pct:.1f}%)")
            report.append("")
            
            # Complexity statistics
            avg_categories = complexity_df['category_count'].mean()
            report.append(f"### Complexity Metrics")
            report.append(f"- Average categories per package: {avg_categories:.2f}")
            report.append("")
        
        # Tool performance by category
        report.append("## Tool Performance by Category")
        if 'tool_detection_by_category' in self.analysis_results:
            for tool_name, tool_results in self.analysis_results['tool_detection_by_category'].items():
                report.append(f"### {tool_name}")
                
                # Sort categories by detection rate
                sorted_categories = sorted(tool_results.items(), 
                                         key=lambda x: x[1]['detection_rate'], reverse=True)
                
                for category, stats in sorted_categories:
                    if stats['total_packages'] > 0:
                        report.append(f"- {category}: {stats['detection_rate']:.3f} "
                                    f"({stats['detected']}/{stats['total_packages']})")
                report.append("")
        
        # Best and worst detected categories
        if 'tool_detection_by_category' in self.analysis_results:
            # Calculate average detection rate per category
            category_avg_detection = {}
            for category in self.categories.keys():
                detection_rates = []
                for tool_results in self.analysis_results['tool_detection_by_category'].values():
                    if category in tool_results:
                        detection_rates.append(tool_results[category]['detection_rate'])
                
                if detection_rates:
                    category_avg_detection[category] = np.mean(detection_rates)
            
            # Sort categories by average detection rate
            sorted_categories = sorted(category_avg_detection.items(), key=lambda x: x[1])
            
            report.append("## Hardest to Detect Categories")
            for category, avg_rate in sorted_categories[:5]:
                report.append(f"- {category}: {avg_rate:.3f} average detection rate")
            report.append("")
            
            report.append("## Best Detected Categories")
            for category, avg_rate in sorted_categories[-5:]:
                report.append(f"- {category}: {avg_rate:.3f} average detection rate")
            report.append("")
        
        # Save report
        report_file = self.output_dir / 'category_based_detection_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"Comprehensive report generated: {report_file}")
        
    def save_detailed_results(self):
        """Save detailed results to CSV files."""
        print("Saving detailed results...")
        
        # Save category distribution
        if 'category_distribution' in self.analysis_results:
            self.analysis_results['category_distribution'].to_csv(
                self.output_dir / 'category_distribution_analysis.csv', index=False)
        
        # Save package complexity data
        if 'package_complexity' in self.analysis_results:
            self.analysis_results['package_complexity'].to_csv(
                self.output_dir / 'package_complexity_analysis.csv', index=False)
        
        # Save tool detection results by category
        if 'tool_detection_by_category' in self.analysis_results:
            detailed_results = []
            for tool_name, tool_data in self.analysis_results['tool_detection_by_category'].items():
                for category, stats in tool_data.items():
                    detailed_results.append({
                        'tool': tool_name,
                        'category': category,
                        'total_packages': stats['total_packages'],
                        'detected': stats['detected'],
                        'missed': stats['missed'],
                        'detection_rate': stats['detection_rate']
                    })
            
            results_df = pd.DataFrame(detailed_results)
            results_df.to_csv(self.output_dir / 'tool_detection_by_category_analysis.csv', index=False)
        
        print("Detailed results saved to CSV files")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        print("Starting category-based evasion detection analysis...")
        
        # Load data
        self.load_classification_mapping()
        self.load_malware_data()
        self.load_tool_stats()
        
        # Perform analysis
        self.analyze_category_distribution()
        self.analyze_tool_detection_by_category()
        self.analyze_package_complexity()
        
        # Generate outputs
        self.generate_comprehensive_report()
        self.save_detailed_results()
        
        print("Analysis complete! Check the generated files in:")
        print(f"  {self.output_dir}")
        print("\nGenerated files:")
        print("- category_distribution.png: Distribution of evasion categories")
        print("- category_detection_heatmap.png: Tool detection rates by category")
        print("- package_complexity.png: Package complexity analysis")
        print("- category_based_detection_report.txt: Comprehensive report")
        print("- *_analysis.csv files: Detailed data for further analysis")

def main():
    """Main function to run the analysis."""

    # Define paths using relative paths from script location
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent.parent  # Experiment/RQ2/code -> NPMAnalysis

    malware_snippets_dir = project_root / "Core" / "Analysis" / "code_snipptes" / "malware_snippets"
    stats_output_dir = project_root / "Core" / "ToolDetection" / "DetectionResults"
    classification_file = script_dir.parent / "statistic" / "input" / "evation_classification.csv"
    output_dir = script_dir.parent / "statistic" / "evasion_analysis"

    # Create analyzer and run analysis
    analyzer = CategoryBasedEvasionAnalyzer(
        malware_snippets_dir,
        stats_output_dir,
        classification_file,
        output_dir
    )
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()

