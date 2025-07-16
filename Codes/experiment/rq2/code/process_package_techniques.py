#!/usr/bin/env python3
"""
Process package technique mapping based on new evasion classification
Author: Assistant
Date: 2024
"""

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import os

def load_classification_mapping():
    """Load the new evasion classification and create technique to category mapping"""
    classification_file = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/experiment/rq2/statistic/evation_classification.csv"
    
    df_classification = pd.read_csv(classification_file)
    
    # Create mapping from technique to category
    technique_to_category = {}
    
    for _, row in df_classification.iterrows():
        category = str(row['category'])
        techniques_str = str(row['techniques'])
        techniques = [t.strip() for t in techniques_str.split(',')]
        
        for technique in techniques:
            if technique:  # Skip empty techniques
                technique_to_category[technique] = category
    
    return technique_to_category

def process_package_categories():
    """Process package technique mapping and generate category-based statistics"""
    
    # Load data
    input_file = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/code_snipptes/statistic_code/package_technique_mapping.csv"
    output_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/experiment/rq2/statistic"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading classification mapping...")
    technique_to_category = load_classification_mapping()
    
    print("Loading package technique mapping...")
    df_packages = pd.read_csv(input_file)
    
    print(f"Loaded {len(df_packages)} rows of package-technique mappings")
    
    # Group by package_id and aggregate categories
    print("Grouping packages and aggregating categories...")
    package_groups = df_packages.groupby('package_id')
    
    # Prepare data for output
    output_data = []
    package_stats = {}
    
    for package_id, group in package_groups:
        # Get unique techniques for this package
        unique_techniques = group['technique'].unique()
        
        # Map techniques to categories (skip unknown techniques)
        package_categories = set()
        unknown_techniques = []
        
        for technique in unique_techniques:
            technique = str(technique).strip()
            if technique in technique_to_category:
                category = technique_to_category[technique]
                package_categories.add(category)
            else:
                # Skip unknown techniques completely
                unknown_techniques.append(technique)
        
        # Convert to sorted list
        unique_categories = sorted(list(package_categories))
        
        # Only include packages with at least one known category
        if len(unique_categories) > 0:
            # Store package information
            package_stats[package_id] = {
                'categories': unique_categories,
                'category_count': len(unique_categories),
                'unknown_techniques': unknown_techniques
            }
            
            # Prepare output row
            output_data.append({
                'package_id': package_id,
                'category_count': len(unique_categories),
                'categories': ';'.join(unique_categories)
            })
        else:
            # Skip packages with no known categories
            if unknown_techniques:
                print(f"Skipping package '{package_id}' - only unknown techniques: {unknown_techniques}")
    
    # Create output DataFrame
    df_output = pd.DataFrame(output_data)
    
    # Save processed data
    output_csv = os.path.join(output_dir, "package_category_summary.csv")
    df_output.to_csv(output_csv, index=False)
    print(f"Saved processed data to: {output_csv}")
    
    # Generate statistics
    generate_category_statistics(package_stats, output_dir)
    
    return df_output, package_stats

def generate_category_statistics(package_stats, output_dir):
    """Generate and save category-based statistics"""
    
    # Basic statistics
    total_packages = len(package_stats)
    
    # Count packages by number of categories
    category_count_distribution = Counter()
    packages_with_multiple_categories = 0
    
    all_categories = []
    
    for package_id, stats in package_stats.items():
        category_count = stats['category_count']
        
        category_count_distribution[category_count] += 1
        
        if category_count > 1:
            packages_with_multiple_categories += 1
        
        all_categories.extend(stats['categories'])
    
    # Count category frequencies
    category_frequency = Counter(all_categories)
    
    # Generate statistics report
    stats_file = os.path.join(output_dir, "category_statistics.txt")
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write("=== EVASION CATEGORY STATISTICS ===\n\n")
        
        f.write("BASIC STATISTICS:\n")
        f.write(f"Total number of package versions with evasion categories: {total_packages}\n")
        f.write(f"Package versions with multiple evasion categories: {packages_with_multiple_categories}\n")
        f.write(f"Percentage with multiple categories: {packages_with_multiple_categories/total_packages*100:.2f}%\n\n")
        
        f.write("DISTRIBUTION BY NUMBER OF CATEGORIES:\n")
        for count in sorted(category_count_distribution.keys()):
            num_packages = category_count_distribution[count]
            percentage = num_packages / total_packages * 100
            f.write(f"{count} categories: {num_packages} packages ({percentage:.2f}%)\n")
        f.write("\n")
        
        f.write("CATEGORY FREQUENCY (Top Categories):\n")
        for category, count in category_frequency.most_common():
            percentage = count / sum(category_frequency.values()) * 100
            f.write(f"{category}: {count} occurrences ({percentage:.2f}%)\n")
        f.write("\n")
        
        # Additional analysis
        f.write("DETAILED ANALYSIS:\n")
        f.write(f"Average categories per package: {sum(category_frequency.values())/total_packages:.2f}\n")
        f.write(f"Total unique categories found: {len(category_frequency)}\n")
        
        # Most complex packages (those with most categories)
        max_categories = max(category_count_distribution.keys()) if category_count_distribution else 0
        f.write(f"Maximum categories in a single package: {max_categories}\n")
        
        # Packages with maximum complexity
        if max_categories > 1:
            complex_packages = [pkg_id for pkg_id, stats in package_stats.items() 
                              if stats['category_count'] == max_categories]
            f.write(f"Packages with {max_categories} categories: {len(complex_packages)}\n")
            if complex_packages:
                f.write("Examples of most complex packages:\n")
                for pkg in complex_packages[:5]:  # Show top 5 examples
                    categories = ';'.join(package_stats[pkg]['categories'])
                    f.write(f"  - {pkg}: {categories}\n")
    
    print(f"Category statistics saved to: {stats_file}")
    
    # Print summary to console
    print("\n=== SUMMARY ===")
    print(f"Total package versions with evasion categories: {total_packages}")
    print(f"Package versions with multiple categories: {packages_with_multiple_categories} ({packages_with_multiple_categories/total_packages*100:.2f}%)")
    print(f"Most frequent categories:")
    for category, count in category_frequency.most_common(5):
        percentage = count / sum(category_frequency.values()) * 100
        print(f"  - {category}: {count} occurrences ({percentage:.2f}%)")

def main():
    """Main function"""
    print("Processing package evasion categories...")
    print("=" * 50)
    
    try:
        df_output, package_stats = process_package_categories()
        
        print("\n=== PROCESSING COMPLETED SUCCESSFULLY ===")
        print(f"Processed {len(df_output)} unique package versions")
        print("Output files:")
        print("- package_category_summary.csv: Processed package data by categories")
        print("- category_statistics.txt: Detailed category statistics")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
