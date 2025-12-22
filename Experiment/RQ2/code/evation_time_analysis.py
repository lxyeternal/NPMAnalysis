#!/usr/bin/env python3
"""
Evasion Technique Time Distribution Analysis v2

This script analyzes the temporal distribution of evasion techniques in malicious NPM packages
using time period classification: early2020, 2021, 2022, 2023, 2024-2025

Usage:
    python evasion_time_analysis_v2.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import re
from collections import defaultdict, Counter
import os
from pathlib import Path

# Set up plotting style
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    try:
        plt.style.use('seaborn')
    except OSError:
        plt.style.use('default')

# Global font settings
plt.rcParams.update({'font.size': 20})
plt.rcParams.update({'axes.labelsize': 24})
plt.rcParams.update({'axes.titlesize': 28})
plt.rcParams.update({'xtick.labelsize': 20})
plt.rcParams.update({'ytick.labelsize': 20})
plt.rcParams.update({'legend.fontsize': 20})

class EvasionTimeAnalyzerV2:
    def __init__(self, package_category_file, malware_time_file, output_dir):
        """
        Initialize the analyzer with data file paths.
        
        Args:
            package_category_file (str): Path to package category summary CSV
            malware_time_file (str): Path to malware time CSV
            output_dir (str): Path for output files
        """
        self.package_category_file = Path(package_category_file)
        self.malware_time_file = Path(malware_time_file)
        self.output_dir = Path(output_dir)
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define time periods in order
        self.time_periods = ["early_2020", "2021", "2022", "2023", "2024-2025"]
        
        # Data containers
        self.package_categories = {}
        self.package_time_data = {}
        self.category_time_data = defaultdict(list)
        self.period_category_counts = defaultdict(lambda: defaultdict(int))
        
        # Analysis results
        self.analysis_results = {}
        
    def year_to_period(self, year):
        """Convert year to time period classification"""
        if year <= 2020:
            return "early2020"
        elif year == 2021:
            return "2021"
        elif year == 2022:
            return "2022"
        elif year == 2023:
            return "2023"
        elif year >= 2024:
            return "2024-2025"
        else:
            return None
    
    def extract_time_period_from_timestamp(self, timestamp):
        """Extract time period from various timestamp formats"""
        if pd.isna(timestamp) or timestamp == '' or timestamp is None:
            return None
        
        try:
            timestamp_str = str(timestamp).strip()
            
            # Match ISO format: 2023-09-18T18:09:31.126Z
            match = re.search(r'(\d{4})-\d{2}-\d{2}', timestamp_str)
            if match:
                year = int(match.group(1))
                return self.year_to_period(year)
            
            # Match MM/DD/YYYY format
            match = re.search(r'\d{1,2}/\d{1,2}/(\d{4})', timestamp_str)
            if match:
                year = int(match.group(1))
                return self.year_to_period(year)
            
            # Handle Unix timestamp
            if timestamp_str.isdigit() and len(timestamp_str) >= 10:
                timestamp_int = int(timestamp_str[:10])
                try:
                    year = datetime.fromtimestamp(timestamp_int).year
                    return self.year_to_period(year)
                except:
                    pass
            
            return None
        except:
            return None
    
    def load_package_categories(self):
        """Load package category mappings"""
        print("Loading package category data...")
        
        df_categories = pd.read_csv(self.package_category_file)
        
        for _, row in df_categories.iterrows():
            package_id = row['package_id']
            categories_value = row['categories']
            
            if str(categories_value) not in ['nan', 'None', ''] and categories_value is not None:
                categories_str = str(categories_value)
                categories = categories_str.split(';') if categories_str else []
            else:
                categories = []
            
            self.package_categories[package_id] = categories
        
        print(f"Loaded {len(self.package_categories)} packages with category data")
    
    def load_time_data(self):
        """Load malware time data"""
        print("Loading time data...")
        
        df_time = pd.read_csv(self.malware_time_file)
        
        for _, row in df_time.iterrows():
            package_name = str(row['package_name']).strip()
            version = str(row['version']).strip()
            timestamp = row['timestamp']
            
            package_id = f"{package_name}/{version}"
            period = self.extract_time_period_from_timestamp(timestamp)
            
            if period is not None:
                self.package_time_data[package_id] = {
                    'period': period,
                    'timestamp': timestamp
                }
        
        print(f"Loaded time data for {len(self.package_time_data)} packages")
    
    def analyze_category_time_distribution(self):
        """Analyze time distribution for each evasion category"""
        print("Analyzing category time distribution...")
        
        # Combine package categories with time data
        for package_id, categories in self.package_categories.items():
            if package_id in self.package_time_data:
                period = self.package_time_data[package_id]['period']
                
                for category in categories:
                    self.category_time_data[category].append(period)
                    self.period_category_counts[period][category] += 1
        
        # Calculate statistics for each category
        category_stats = {}
        
        for category, periods in self.category_time_data.items():
            if len(periods) > 0:
                period_counts = Counter(periods)
                total_packages = len(periods)
                
                category_stats[category] = {
                    'total_packages': total_packages,
                    'periods': sorted(period_counts.keys(), key=lambda x: self.time_periods.index(x) if x in self.time_periods else 999),
                    'period_counts': period_counts,
                    'earliest_period': min(periods, key=lambda x: self.time_periods.index(x) if x in self.time_periods else 999),
                    'latest_period': max(periods, key=lambda x: self.time_periods.index(x) if x in self.time_periods else 999),
                    'peak_period': period_counts.most_common(1)[0][0],
                    'peak_count': period_counts.most_common(1)[0][1]
                }
        
        self.analysis_results['category_stats'] = category_stats
        
        print(f"Analyzed time distribution for {len(category_stats)} categories")
    
    def create_time_trend_visualization(self):
        """Create time trend visualization for evasion categories"""
        print("Creating time trend visualization...")
        
        if not self.analysis_results.get('category_stats'):
            print("No category statistics available for visualization")
            return
        
        # Prepare data for plotting
        category_stats = self.analysis_results['category_stats']
        
        # Get all categories (removed minimum package filter)
        all_categories = list(category_stats.keys())
        
        if len(all_categories) == 0:
            print("No categories available for visualization")
            return
        
        # Sort categories by total package count (descending)
        all_categories.sort(key=lambda x: category_stats[x]['total_packages'], reverse=True)
        
        # Show all categories (changed from top 8 to all)
        top_categories = all_categories
        
        # Create the plot with larger size for more categories
        plt.figure(figsize=(16, 12))
        
        # Define more colors and styles for all categories
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                 '#ff1744', '#00e676', '#ff9800', '#9c27b0']
        line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', 
                      '-', '--', '-.', ':', '-', '--']
        markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 
                  'P', 'X', '+', 'x', '8', '4']
        
        max_count = 0
        
        for i, category in enumerate(top_categories):
            stats = category_stats[category]
            period_counts = stats['period_counts']
            
            # Create data points for all time periods
            counts = []
            for period in self.time_periods:
                count = period_counts.get(period, 0)
                counts.append(count)
                max_count = max(max_count, count)
            
            # Plot the line
            color = colors[i % len(colors)]
            line_style = line_styles[i % len(line_styles)]
            marker = markers[i % len(markers)]
            
            plt.plot(self.time_periods, counts,
                    marker=marker,
                    linewidth=2.5,
                    linestyle=line_style,
                    color=color,
                    markersize=8,
                    markeredgewidth=1,
                    markeredgecolor='white',
                    label=category)
        
        # Customize the plot
        plt.ylabel('Number of Packages', fontsize=24)
        
        # Set background and grid
        plt.gca().set_facecolor('none')
        plt.gcf().patch.set_facecolor('white')
        plt.grid(True, alpha=0.5, linestyle='-', linewidth=0.5, color='gray')
        
        # Configure legend with single column
        legend = plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
                           frameon=False,
                           handlelength=2, handletextpad=0.5,
                           fontsize=16, ncol=1)
        
        # Set axis limits and ticks
        plt.xticks(rotation=45, fontsize=20)
        plt.yticks(fontsize=20)
        plt.ylim(0, max_count * 1.1)
        
        plt.tight_layout()
        
        # Save the plot
        output_file = self.output_dir / 'evasion_time_trends.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Time trend visualization saved to: {output_file}")
    
    def create_category_distribution_by_period(self):
        """Create visualization showing category distribution by time period"""
        print("Creating category distribution by time period...")
        
        if not self.period_category_counts:
            print("No period-category data available")
            return
        
        # Prepare data for stacked bar chart
        category_stats = self.analysis_results.get('category_stats', {})
        
        # Get all categories (changed from top 10 to all)
        top_categories = sorted(category_stats.keys(), 
                               key=lambda x: category_stats[x]['total_packages'], 
                               reverse=True)
        
        # Create data matrix
        data_matrix = []
        for category in top_categories:
            category_data = []
            for period in self.time_periods:
                count = self.period_category_counts[period].get(category, 0)
                category_data.append(count)
            data_matrix.append(category_data)
        
        # Create stacked bar chart with larger size for all categories
        plt.figure(figsize=(16, 12))
        
        # Define colors
        import matplotlib.cm as cm
        colors = cm.get_cmap('Set3')(np.linspace(0, 1, len(top_categories)))
        
        bottom = np.zeros(len(self.time_periods))
        
        for i, (category, data) in enumerate(zip(top_categories, data_matrix)):
            plt.bar(self.time_periods, data, bottom=bottom, label=category, 
                    color=colors[i], alpha=0.8, edgecolor='white', linewidth=0.5)
            bottom += np.array(data)
        
        # plt.xlabel('Time Period', fontsize=26)  # 去掉横轴标题
        plt.ylabel('Number of Packages', fontsize=26)
        # plt.title('Evasion Technique Categories Distribution by Time Period (All Categories)', fontsize=30, fontweight='bold')  # 去掉标题
        
        # Set background and grid - 白色底的线条网格
        plt.gca().set_facecolor('white')
        plt.gcf().patch.set_facecolor('white')
        plt.grid(True, alpha=0.5, linestyle='-', linewidth=0.5, color='gray')
        
        # Configure legend with smaller font for all categories - 改为一列
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False, fontsize=16, ncol=1)
        
        plt.xticks(rotation=45, fontsize=22)
        plt.yticks(fontsize=22)
        
        plt.tight_layout()
        
        # Save the plot
        output_file = self.output_dir / 'evasion_categories_by_period.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Category distribution by period saved to: {output_file}")
    
    def generate_time_analysis_report(self):
        """Generate comprehensive time analysis report"""
        print("Generating time analysis report...")
        
        category_stats = self.analysis_results.get('category_stats', {})
        
        report_lines = []
        report_lines.append("# Evasion Technique Time Distribution Analysis Report")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Overall statistics
        total_packages_with_time = len(self.package_time_data)
        total_categories = len(category_stats)
        
        report_lines.append("## Overall Statistics")
        report_lines.append(f"- Total packages with time data: {total_packages_with_time}")
        report_lines.append(f"- Categories analyzed: {total_categories}")
        report_lines.append(f"- Time periods: {', '.join(self.time_periods)}")
        report_lines.append("")
        
        # Category statistics
        report_lines.append("## Category Time Statistics")
        report_lines.append("### Top Categories by Package Count")
        
        sorted_categories = sorted(category_stats.items(), 
                                 key=lambda x: x[1]['total_packages'], reverse=True)
        
        for category, stats in sorted_categories[:15]:
            report_lines.append(
                f"- {category}: {stats['total_packages']} packages "
                f"({stats['earliest_period']} - {stats['latest_period']}, "
                f"peak: {stats['peak_period']} with {stats['peak_count']} packages)"
            )
        
        report_lines.append("")
        
        # Period-by-period breakdown
        report_lines.append("## Period-by-Period Analysis")
        
        for period in self.time_periods:
            period_data = self.period_category_counts[period]
            total_period_packages = sum(period_data.values())
            
            if total_period_packages > 0:
                report_lines.append(f"### {period}")
                report_lines.append(f"Total packages: {total_period_packages}")
                
                # Top categories for this period
                sorted_period_categories = sorted(period_data.items(), key=lambda x: x[1], reverse=True)
                report_lines.append("Top categories:")
                for category, count in sorted_period_categories[:5]:
                    percentage = (count / total_period_packages) * 100 if total_period_packages > 0 else 0
                    report_lines.append(f"  - {category}: {count} packages ({percentage:.1f}%)")
                
                report_lines.append("")
        
        # Save report
        report_file = self.output_dir / 'evasion_time_analysis_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        print(f"Time analysis report saved to: {report_file}")
    
    def save_detailed_data(self):
        """Save detailed analysis data to CSV files"""
        print("Saving detailed analysis data...")
        
        # Save category time statistics
        category_stats = self.analysis_results.get('category_stats', {})
        if category_stats:
            stats_data = []
            for category, stats in category_stats.items():
                stats_data.append({
                    'category': category,
                    'total_packages': stats['total_packages'],
                    'earliest_period': stats['earliest_period'],
                    'latest_period': stats['latest_period'],
                    'peak_period': stats['peak_period'],
                    'peak_count': stats['peak_count'],
                    'periods_active': len(stats['periods'])
                })
            
            stats_df = pd.DataFrame(stats_data)
            stats_df = stats_df.sort_values('total_packages', ascending=False)
            stats_file = self.output_dir / 'category_time_statistics.csv'
            stats_df.to_csv(stats_file, index=False)
            print(f"Category time statistics saved to: {stats_file}")
        
        # Save period-category matrix
        if self.period_category_counts:
            categories = sorted(set().union(*[set(period_data.keys()) 
                                           for period_data in self.period_category_counts.values()]))
            
            matrix_data = []
            for period in self.time_periods:
                row_data = {'period': period}
                for category in categories:
                    row_data[category] = str(self.period_category_counts[period].get(category, 0))
                matrix_data.append(row_data)
            
            matrix_df = pd.DataFrame(matrix_data)
            matrix_file = self.output_dir / 'period_category_matrix.csv'
            matrix_df.to_csv(matrix_file, index=False)
            print(f"Period-category matrix saved to: {matrix_file}")
    
    def run_complete_analysis(self):
        """Run the complete time analysis pipeline"""
        print("Starting evasion technique time distribution analysis...")
        print("=" * 60)
        
        # Load data
        self.load_package_categories()
        self.load_time_data()
        
        # Perform analysis
        self.analyze_category_time_distribution()
        
        # Generate visualizations
        self.create_time_trend_visualization()
        self.create_category_distribution_by_period()
        
        # Generate reports and save data
        self.generate_time_analysis_report()
        self.save_detailed_data()
        
        print("\nAnalysis complete! Generated files:")
        print("- evasion_time_trends.png: Time trend lines for top categories")
        print("- evasion_categories_by_period.png: Stacked bar chart by period")
        print("- evasion_time_analysis_report.txt: Comprehensive analysis report")
        print("- category_time_statistics.csv: Statistical summary by category")
        print("- period_category_matrix.csv: Period-category count matrix")

def main():
    """Main function to run the analysis"""

    # Define file paths using relative paths
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent.parent  # Experiment/RQ2/code -> NPMAnalysis

    package_category_file = script_dir.parent / "statistic" / "input" / "package_category_summary.csv"
    malware_time_file = project_root / "Core" / "Data" / "timecollect" / "time" / "malware_time.csv"
    output_dir = script_dir.parent / "statistic" / "evasion_time"

    # Create analyzer and run analysis
    analyzer = EvasionTimeAnalyzerV2(package_category_file, malware_time_file, output_dir)
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()