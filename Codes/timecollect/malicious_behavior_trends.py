#!/usr/bin/env python3
"""
Malicious Behavior Trends Analysis Script

This script analyzes the evolution of malicious behaviors in NPM packages over time
by combining classification data with temporal information.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import ast
import os
import warnings
warnings.filterwarnings('ignore')

def load_and_process_data():
    """Load and merge the classification and time data"""
    
    # File paths
    classifications_file = '/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/behavior_annoation/key_results/package_all_classifications.csv'
    time_file = '/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/timecollect/time/filtered_malware_time.csv'
    
    print("Loading classification data...")
    classifications_df = pd.read_csv(classifications_file)
    
    print("Loading time data...")
    time_df = pd.read_csv(time_file)
    
    # Clean and merge data
    print("Merging datasets...")
    merged_df = pd.merge(classifications_df, time_df, on=['package_name', 'version'], how='inner')
    
    # Filter out rows with empty timestamps
    merged_df = merged_df[merged_df['timestamp'].notna() & (merged_df['timestamp'] != '')]
    
    print(f"Total packages with both classification and time data: {len(merged_df)}")
    
    return merged_df

def extract_behaviors(merged_df):
    """Extract and process behavior classifications"""
    
    print("Processing behavior classifications...")
    
    # Parse the classifications column
    behaviors_data = []
    
    for idx, row in merged_df.iterrows():
        try:
            # Parse the timestamp
            timestamp = pd.to_datetime(row['timestamp'])
            
            # Parse the classifications (remove quotes and brackets, then split)
            classifications_str = row['classifications'].strip('"')
            classifications = ast.literal_eval(classifications_str)
            
            # Group years: 2020 and earlier become "early 2020", 2024-2025 become "2024-2025"
            if timestamp.year <= 2020:
                year_label = "early 2020"
            elif timestamp.year >= 2024:
                year_label = "2024-2025"
            else:
                year_label = str(timestamp.year)
            
            # Add each behavior with its timestamp
            for behavior in classifications:
                behaviors_data.append({
                    'package_name': row['package_name'],
                    'version': row['version'],
                    'timestamp': timestamp,
                    'behavior': behavior.strip(),
                    'year': year_label
                })
                
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
    
    behaviors_df = pd.DataFrame(behaviors_data)
    print(f"Total behavior instances extracted: {len(behaviors_df)}")
    
    return behaviors_df

def create_behavior_trends_plot(behaviors_df, output_dir):
    """Create line plot showing behavior trends over time"""
    
    print("Creating behavior trends visualization...")
    
    # Define year sorting function
    def sort_key(x):
        if x == "early 2020":
            return 2019
        elif x == "2024-2025":
            return 2024.5
        else:
            return int(x)
    
    # Get all behaviors
    behavior_counts = behaviors_df['behavior'].value_counts()
    print("All behaviors:")
    print(behavior_counts)
    
    # Use ALL behaviors instead of just top ones
    all_behaviors = behavior_counts.index.tolist()
    
    # Analyze trends by year - use absolute counts instead of percentages
    yearly_trends = behaviors_df.groupby(['year', 'behavior']).size().unstack(fill_value=0)
    
    # Filter data for all behaviors
    plot_data = yearly_trends[all_behaviors]
    
    # Create the plot with similar style to reference image
    plt.figure(figsize=(14, 10))  # Larger figure size for more behaviors
    
    # Define more colors and line styles for all behaviors
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
              '#ff9896', '#98df8a', '#ffbb78', '#c5b0d5', '#c49c94', '#f7b6d3', '#c7c7c7', '#dbdb8d', '#9edae5', '#ffcc99']
    line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--',
                   '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '*',
               'X', 'P', '+', 'x', '|', '_', '1', '2', '3', '4']
    
    # Plot each behavior
    for i, behavior in enumerate(all_behaviors):
        if behavior in plot_data.columns:
            # Sort data according to year order
            years_sorted = sorted(plot_data.index, key=sort_key)
            y_values = [plot_data.loc[year, behavior] for year in years_sorted]
            
            plt.plot(range(len(years_sorted)), y_values, 
                    color=colors[i % len(colors)], 
                    linestyle=line_styles[i % len(line_styles)],
                    marker=markers[i % len(markers)],
                    markersize=6,  # Larger marker size
                    linewidth=2.5,  # Thicker lines
                    label=behavior,
                    alpha=0.8)
    
    # Customize the plot with larger fonts
    plt.ylabel('Number of Packages', fontsize=16, fontweight='bold')  # Changed to Count and larger font
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)  # Larger legend font
    
    # Set axis properties
    years = sorted(plot_data.index, key=sort_key)  # Sort years properly
    plt.xticks(range(len(years)), years, fontsize=14)  # Use range for proper spacing
    plt.yticks(fontsize=14)  # Larger tick labels
    
    # Add grid lines similar to reference
    plt.gca().set_axisbelow(True)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'malicious_behavior_trends.png'), 
                dpi=300, bbox_inches='tight')
    print(f"Saved behavior trends plot to {output_dir}/malicious_behavior_trends.png")
    
    # Save processed data (absolute counts)
    plot_data.to_csv(os.path.join(output_dir, 'behavior_trends_data.csv'))
    
    plt.show()

def main():
    """Main function to run the analysis"""
    
    print("Starting Malicious Behavior Trends Analysis...")
    print("=" * 50)
    
    # Set output directory
    output_dir = '/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/timecollect/time/time_classify'
    
    try:
        # Step 1: Load and process data
        merged_df = load_and_process_data()
        
        # Step 2: Extract behaviors
        behaviors_df = extract_behaviors(merged_df)
        
        if len(behaviors_df) == 0:
            print("No valid behavior data found. Exiting.")
            return
        
        # Step 3: Create the main trend visualization
        create_behavior_trends_plot(behaviors_df, output_dir)
        
        print("\n" + "=" * 50)
        print("Analysis completed successfully!")
        print(f"Results saved to: {output_dir}")
        print("Generated files:")
        print("  - malicious_behavior_trends.png (main trend plot)")
        print("  - behavior_trends_data.csv (trend data)")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 