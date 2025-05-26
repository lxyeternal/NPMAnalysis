#!/usr/bin/env python3
"""
Malware Detection Rate Analysis Over Time
This script analyzes how detection rates have changed over time for different malware detection tools.
"""

import pandas as pd
import json
import os
import glob
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

class MalwareDetectionAnalyzer:
    def __init__(self, csv_path, stats_output_dir):
        """
        Initialize the analyzer with paths to data files
        
        Args:
            csv_path: Path to the CSV file containing package timestamps
            stats_output_dir: Path to the directory containing tool detection results
        """
        self.csv_path = csv_path
        self.stats_output_dir = stats_output_dir
        self.time_data = None
        self.detection_data = {}
        self.combined_data = {}
        
    def load_time_data(self):
        """Load and process the timestamp data from CSV"""
        print("Loading timestamp data...")
        self.time_data = pd.read_csv(self.csv_path)
        
        # Create package identifier
        self.time_data['package_id'] = self.time_data['package_name'] + '/' + self.time_data['version']
        
        # Parse timestamps and extract year
        self.time_data['timestamp'] = pd.to_datetime(self.time_data['timestamp'], errors='coerce')
        self.time_data['year'] = self.time_data['timestamp'].dt.year
        
        # Group years according to requirements
        def group_years(year):
            if pd.isna(year):
                return 'Unknown'
            elif year <= 2020:
                return '2011-2020'
            elif year == 2021:
                return '2021'
            elif year == 2022:
                return '2022'
            elif year == 2023:
                return '2023'
            elif year >= 2024:
                return '2024-2025'
            else:
                return 'Unknown'
        
        self.time_data['year_group'] = self.time_data['year'].apply(group_years)
        
        print(f"Loaded {len(self.time_data)} timestamp records")
        print(f"Year distribution:")
        print(self.time_data['year_group'].value_counts().sort_index())
        
    def load_detection_data(self):
        """Load detection results from all tools"""
        print("\nLoading detection data...")
        
        # Find all tool directories
        tool_dirs = [d for d in os.listdir(self.stats_output_dir) 
                    if os.path.isdir(os.path.join(self.stats_output_dir, d))]
        
        for tool in tool_dirs:
            tool_path = os.path.join(self.stats_output_dir, tool)
            
            # Load false negatives (malware predicted as benign)
            fn_path = os.path.join(tool_path, 'false_negatives.json')
            malicious_path = os.path.join(tool_path, 'malicious_reports.json')
            
            tool_data = {
                'false_negatives': {},
                'true_positives': {}
            }
            
            # Load false negatives
            if os.path.exists(fn_path):
                with open(fn_path, 'r') as f:
                    tool_data['false_negatives'] = json.load(f)
            
            # Load malicious reports (should contain true positives)
            if os.path.exists(malicious_path):
                with open(malicious_path, 'r') as f:
                    malicious_data = json.load(f)
                    # Filter for actual malware that was correctly detected
                    for pkg_id, info in malicious_data.items():
                        if isinstance(info, dict) and info.get('actual') == 'malware' and info.get('prediction') == 'malware':
                            tool_data['true_positives'][pkg_id] = info
            
            self.detection_data[tool] = tool_data
            
            print(f"Tool {tool}: {len(tool_data['false_negatives'])} false negatives, "
                  f"{len(tool_data['true_positives'])} true positives")
    
    def combine_data(self):
        """Combine detection data with timestamp data"""
        print("\nCombining detection and timestamp data...")
        
        for tool, tool_data in self.detection_data.items():
            combined_tool_data = defaultdict(lambda: defaultdict(lambda: {'detected': 0, 'missed': 0, 'total': 0}))
            
            # Process false negatives (missed detections)
            for pkg_id in tool_data['false_negatives']:
                # Clean package ID format (remove ## and other special chars)
                clean_pkg_id = pkg_id.replace('##', '/')
                
                # Find matching timestamp
                time_match = self.time_data[self.time_data['package_id'] == clean_pkg_id]
                if not time_match.empty:
                    year_group = time_match.iloc[0]['year_group']
                    combined_tool_data[year_group]['malware']['missed'] += 1
                    combined_tool_data[year_group]['malware']['total'] += 1
                else:
                    # If no timestamp found, categorize as unknown
                    combined_tool_data['Unknown']['malware']['missed'] += 1
                    combined_tool_data['Unknown']['malware']['total'] += 1
            
            # Process true positives (correct detections)
            for pkg_id in tool_data['true_positives']:
                clean_pkg_id = pkg_id.replace('##', '/')
                
                time_match = self.time_data[self.time_data['package_id'] == clean_pkg_id]
                if not time_match.empty:
                    year_group = time_match.iloc[0]['year_group']
                    combined_tool_data[year_group]['malware']['detected'] += 1
                    combined_tool_data[year_group]['malware']['total'] += 1
                else:
                    combined_tool_data['Unknown']['malware']['detected'] += 1
                    combined_tool_data['Unknown']['malware']['total'] += 1
            
            self.combined_data[tool] = dict(combined_tool_data)
            
        print("Data combination completed")
    
    def calculate_detection_rates(self):
        """Calculate detection rates for each tool and year group"""
        detection_rates = {}
        
        for tool, tool_data in self.combined_data.items():
            detection_rates[tool] = {}
            
            for year_group, categories in tool_data.items():
                if 'malware' in categories:
                    stats = categories['malware']
                    total = stats['total']
                    detected = stats['detected']
                    
                    if total > 0:
                        detection_rate = (detected / total) * 100
                        detection_rates[tool][year_group] = {
                            'detection_rate': detection_rate,
                            'detected': detected,
                            'missed': stats['missed'],
                            'total': total
                        }
        
        return detection_rates
    
    def create_visualizations(self, detection_rates):
        """Create comprehensive visualizations"""
        print("\nCreating visualizations...")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Prepare data for plotting
        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025', 'Unknown']
        tools = list(detection_rates.keys())
        
        # Create detection rate matrix
        rate_matrix = []
        tools_with_data = []
        
        for tool in tools:
            tool_rates = []
            has_data = False
            for year_group in year_groups:
                if year_group in detection_rates[tool]:
                    tool_rates.append(detection_rates[tool][year_group]['detection_rate'])
                    has_data = True
                else:
                    tool_rates.append(0)
            
            if has_data:  # Only include tools with some data
                rate_matrix.append(tool_rates)
                tools_with_data.append(tool)
        
        if not rate_matrix:
            print("No data available for visualization")
            return
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Heatmap of detection rates
        plt.subplot(2, 3, 1)
        if rate_matrix:
            sns.heatmap(rate_matrix, 
                       xticklabels=year_groups, 
                       yticklabels=tools_with_data,
                       annot=True, 
                       fmt='.1f', 
                       cmap='RdYlGn',
                       cbar_kws={'label': 'Detection Rate (%)'})
        plt.title('Detection Rates Heatmap by Tool and Year', fontsize=14, fontweight='bold')
        plt.xlabel('Year Group')
        plt.ylabel('Detection Tool')
        
        # # 2. Line plot of detection rates over time
        # plt.subplot(2, 3, 2)
        # for i, tool in enumerate(tools_with_data):
        #     rates = [detection_rates[tool].get(yg, {'detection_rate': 0})['detection_rate'] 
        #             for yg in year_groups[:-1]]  # Exclude 'Unknown'
        #     plt.plot(year_groups[:-1], rates, marker='o', linewidth=2, label=tool)
        
        # plt.title('Detection Rate Trends Over Time', fontsize=14, fontweight='bold')
        # plt.xlabel('Year Group')
        # plt.ylabel('Detection Rate (%)')
        # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        # plt.xticks(rotation=45)
        # plt.grid(True, alpha=0.3)
        

        # ...existing code...
        # 2. Line plot of detection rates over time
        plt.subplot(2, 3, 2)
        
        # Define distinct colors and line styles for better differentiation
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                 '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5']
        
        line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--']
        markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
        
        for i, tool in enumerate(tools_with_data):
            rates = [detection_rates[tool].get(yg, {'detection_rate': 0})['detection_rate'] 
                    for yg in year_groups[:-1]]  # Exclude 'Unknown'
            
            # Use different color, line style, and marker for each tool
            color = colors[i % len(colors)]
            line_style = line_styles[i % len(line_styles)]
            marker = markers[i % len(markers)]
            
            plt.plot(year_groups[:-1], rates, 
                    marker=marker, 
                    linewidth=2.5, 
                    linestyle=line_style,
                    color=color,
                    markersize=8,
                    markeredgewidth=1,
                    markeredgecolor='white',
                    label=tool)
        
        plt.title('Detection Rate Trends Over Time', fontsize=14, fontweight='bold')
        plt.xlabel('Year Group')
        plt.ylabel('Detection Rate (%)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True, 
                  fancybox=True, shadow=True)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, 100)  # Set y-axis limits for better visualization
# ...existing code...

        # 3. Bar plot of total detections by year
        plt.subplot(2, 3, 3)
        year_totals = defaultdict(int)
        for tool in tools_with_data:
            for year_group in year_groups:
                if year_group in detection_rates[tool]:
                    year_totals[year_group] += detection_rates[tool][year_group]['total']
        
        years = list(year_totals.keys())
        totals = list(year_totals.values())
        plt.bar(years, totals, color='skyblue', alpha=0.7)
        plt.title('Total Malware Samples by Year', fontsize=14, fontweight='bold')
        plt.xlabel('Year Group')
        plt.ylabel('Number of Samples')
        plt.xticks(rotation=45)
        
        # 4. Box plot of detection rates by tool
        plt.subplot(2, 3, 4)
        tool_rates_list = []
        tool_names_list = []
        
        for tool in tools_with_data:
            rates = [detection_rates[tool][yg]['detection_rate'] 
                    for yg in detection_rates[tool] if yg != 'Unknown']
            if rates:  # Only include if there are rates
                tool_rates_list.extend(rates)
                tool_names_list.extend([tool] * len(rates))
        
        if tool_rates_list:
            df_box = pd.DataFrame({'Tool': tool_names_list, 'Detection_Rate': tool_rates_list})
            sns.boxplot(data=df_box, x='Tool', y='Detection_Rate')
            plt.title('Detection Rate Distribution by Tool', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.ylabel('Detection Rate (%)')
        
        # 5. Stacked bar chart of detected vs missed
        plt.subplot(2, 3, 5)
        bottom_detected = np.zeros(len(year_groups))
        bottom_missed = np.zeros(len(year_groups))
        
        colors_detected = plt.cm.Set3(np.linspace(0, 1, len(tools_with_data)))
        colors_missed = plt.cm.Set1(np.linspace(0, 1, len(tools_with_data)))
        
        for i, tool in enumerate(tools_with_data):
            detected_counts = [detection_rates[tool].get(yg, {'detected': 0})['detected'] 
                             for yg in year_groups]
            missed_counts = [detection_rates[tool].get(yg, {'missed': 0})['missed'] 
                           for yg in year_groups]
            
            plt.bar(year_groups, detected_counts, bottom=bottom_detected, 
                   label=f'{tool} (Detected)', color=colors_detected[i], alpha=0.8)
            plt.bar(year_groups, missed_counts, bottom=bottom_missed + detected_counts, 
                   label=f'{tool} (Missed)', color=colors_missed[i], alpha=0.5, hatch='//')
            
            bottom_detected += detected_counts
            bottom_missed += missed_counts
        
        plt.title('Detected vs Missed Malware by Year', fontsize=14, fontweight='bold')
        plt.xlabel('Year Group')
        plt.ylabel('Number of Samples')
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 6. Average detection rate by year
        plt.subplot(2, 3, 6)
        avg_rates_by_year = {}
        for year_group in year_groups:
            rates = []
            for tool in tools_with_data:
                if year_group in detection_rates[tool]:
                    rates.append(detection_rates[tool][year_group]['detection_rate'])
            if rates:
                avg_rates_by_year[year_group] = np.mean(rates)
        
        years = list(avg_rates_by_year.keys())
        avg_rates = list(avg_rates_by_year.values())
        plt.bar(years, avg_rates, color='lightcoral', alpha=0.7)
        plt.title('Average Detection Rate Across All Tools', fontsize=14, fontweight='bold')
        plt.xlabel('Year Group')
        plt.ylabel('Average Detection Rate (%)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('malware_detection_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def generate_summary_report(self, detection_rates):
        """Generate a comprehensive summary report"""
        print("\nGenerating summary report...")
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("MALWARE DETECTION RATE ANALYSIS REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overall statistics
        report_lines.append("OVERALL STATISTICS")
        report_lines.append("-" * 40)
        
        total_tools = len(detection_rates)
        total_samples = 0
        total_detected = 0
        
        for tool, tool_data in detection_rates.items():
            for year_group, stats in tool_data.items():
                total_samples += stats['total']
                total_detected += stats['detected']
        
        overall_rate = (total_detected / total_samples * 100) if total_samples > 0 else 0
        
        report_lines.append(f"Total tools analyzed: {total_tools}")
        report_lines.append(f"Total malware samples: {total_samples}")
        report_lines.append(f"Total detected: {total_detected}")
        report_lines.append(f"Overall detection rate: {overall_rate:.2f}%")
        report_lines.append("")
        
        # Year-wise analysis
        report_lines.append("YEAR-WISE ANALYSIS")
        report_lines.append("-" * 40)
        
        year_groups = ['2011-2020', '2021', '2022', '2023', '2024-2025', 'Unknown']
        
        for year_group in year_groups:
            year_total = 0
            year_detected = 0
            tools_with_data = 0
            
            for tool, tool_data in detection_rates.items():
                if year_group in tool_data:
                    year_total += tool_data[year_group]['total']
                    year_detected += tool_data[year_group]['detected']
                    tools_with_data += 1
            
            if year_total > 0:
                year_rate = (year_detected / year_total) * 100
                report_lines.append(f"{year_group}:")
                report_lines.append(f"  Samples: {year_total}")
                report_lines.append(f"  Detected: {year_detected}")
                report_lines.append(f"  Detection Rate: {year_rate:.2f}%")
                report_lines.append(f"  Tools with data: {tools_with_data}")
                report_lines.append("")
        
        # Tool-wise analysis
        report_lines.append("TOOL-WISE ANALYSIS")
        report_lines.append("-" * 40)
        
        for tool, tool_data in detection_rates.items():
            tool_total = sum(stats['total'] for stats in tool_data.values())
            tool_detected = sum(stats['detected'] for stats in tool_data.values())
            tool_rate = (tool_detected / tool_total * 100) if tool_total > 0 else 0
            
            report_lines.append(f"{tool}:")
            report_lines.append(f"  Total samples: {tool_total}")
            report_lines.append(f"  Total detected: {tool_detected}")
            report_lines.append(f"  Overall detection rate: {tool_rate:.2f}%")
            
            # Year breakdown for this tool
            for year_group in year_groups:
                if year_group in tool_data:
                    stats = tool_data[year_group]
                    report_lines.append(f"    {year_group}: {stats['detection_rate']:.2f}% "
                                      f"({stats['detected']}/{stats['total']})")
            report_lines.append("")
        
        # Trends and insights
        report_lines.append("TRENDS AND INSIGHTS")
        report_lines.append("-" * 40)
        
        # Calculate average detection rates by year
        year_avg_rates = {}
        for year_group in year_groups:
            rates = []
            for tool, tool_data in detection_rates.items():
                if year_group in tool_data:
                    rates.append(tool_data[year_group]['detection_rate'])
            if rates:
                year_avg_rates[year_group] = np.mean(rates)
        
        if len(year_avg_rates) > 1:
            years_sorted = sorted([y for y in year_avg_rates.keys() if y != 'Unknown'])
            if len(years_sorted) > 1:
                trend = "improving" if year_avg_rates[years_sorted[-1]] > year_avg_rates[years_sorted[0]] else "declining"
                report_lines.append(f"Overall trend: Detection rates are {trend} over time")
        
        # Best and worst performing tools
        tool_overall_rates = {}
        for tool, tool_data in detection_rates.items():
            total = sum(stats['total'] for stats in tool_data.values())
            detected = sum(stats['detected'] for stats in tool_data.values())
            if total > 0:
                tool_overall_rates[tool] = (detected / total) * 100
        
        if tool_overall_rates:
            best_tool = max(tool_overall_rates, key=tool_overall_rates.get)
            worst_tool = min(tool_overall_rates, key=tool_overall_rates.get)
            
            report_lines.append(f"Best performing tool: {best_tool} ({tool_overall_rates[best_tool]:.2f}%)")
            report_lines.append(f"Worst performing tool: {worst_tool} ({tool_overall_rates[worst_tool]:.2f}%)")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        
        # Save report to file
        with open('malware_detection_summary_report.txt', 'w') as f:
            f.write('\n'.join(report_lines))
        
        # Print summary to console
        print('\n'.join(report_lines))
        
        return report_lines
    
    def run_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting malware detection rate analysis...")
        
        # Load data
        self.load_time_data()
        self.load_detection_data()
        self.combine_data()
        
        # Calculate detection rates
        detection_rates = self.calculate_detection_rates()
        
        # Create visualizations
        self.create_visualizations(detection_rates)
        
        # Generate summary report
        self.generate_summary_report(detection_rates)
        
        print("\nAnalysis completed!")
        print("Files generated:")
        print("- malware_detection_analysis.png (visualization)")
        print("- malware_detection_summary_report.txt (summary report)")
        
        return detection_rates

def main():
    """Main function to run the analysis"""
    # Configuration
    CSV_PATH = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/timecollect/time/filtered_malware_time.csv"
    STATS_OUTPUT_DIR = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    
    # Verify paths exist
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return
    
    if not os.path.exists(STATS_OUTPUT_DIR):
        print(f"Error: Stats output directory not found at {STATS_OUTPUT_DIR}")
        return
    
    # Create analyzer and run analysis
    analyzer = MalwareDetectionAnalyzer(CSV_PATH, STATS_OUTPUT_DIR)
    detection_rates = analyzer.run_analysis()
    
    return detection_rates

if __name__ == "__main__":
    detection_rates = main()