import json
import csv
import os
from collections import defaultdict, Counter
import pandas as pd

def load_package_classifications(csv_file_path):
    """Load package classifications from CSV file"""
    classifications_dict = {}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if exists
        
        for row in csv_reader:
            if len(row) >= 4:
                package_id = row[0].strip()
                package_name = row[1].strip()
                version = row[2].strip()
                classifications_str = row[3].strip()
                
                # Parse classifications string (remove brackets and quotes)
                classifications_str = classifications_str.strip("[]\"'")
                classifications = [cls.strip().strip("'\"") for cls in classifications_str.split(',')]
                classifications = [cls for cls in classifications if cls]  # Remove empty strings
                
                # Create key in format "package-name/version"
                key = f"{package_name}/{version}"
                classifications_dict[key] = classifications
    
    return classifications_dict

def load_false_negatives(base_directory):
    """Load all false negative files from different tools"""
    false_negatives = {}
    tools_found = []
    
    if not os.path.exists(base_directory):
        print(f"Warning: Base directory {base_directory} does not exist")
        return false_negatives, tools_found
    
    for tool_name in os.listdir(base_directory):
        tool_path = os.path.join(base_directory, tool_name)
        if os.path.isdir(tool_path):
            false_negative_file = os.path.join(tool_path, 'false_negatives.json')
            
            if os.path.exists(false_negative_file):
                try:
                    with open(false_negative_file, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        false_negatives[tool_name] = data
                        tools_found.append(tool_name)
                        print(f"Loaded {len(data)} false negatives for tool: {tool_name}")
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON from {false_negative_file}: {e}")
                except Exception as e:
                    print(f"Error processing {false_negative_file}: {e}")
    
    return false_negatives, tools_found

def analyze_classifications(package_classifications, false_negatives):
    """Analyze classifications for false negative packages"""
    analysis_results = {}
    overall_classification_counts = Counter()
    
    for tool_name, fn_data in false_negatives.items():
        tool_classification_counts = Counter()
        tool_packages = []
        
        for package_key in fn_data.keys():
            if package_key in package_classifications:
                classifications = package_classifications[package_key]
                tool_packages.append({
                    'package': package_key,
                    'classifications': classifications,
                    'classification_count': len(classifications)
                })
                
                # Count each classification
                for classification in classifications:
                    tool_classification_counts[classification] += 1
                    overall_classification_counts[classification] += 1
            else:
                print(f"Warning: Package {package_key} not found in classifications")
        
        analysis_results[tool_name] = {
            'packages': tool_packages,
            'classification_counts': dict(tool_classification_counts),
            'total_packages': len(tool_packages),
            'total_fn_packages': len(fn_data)
        }
    
    return analysis_results, dict(overall_classification_counts)

def save_detailed_results(analysis_results, output_dir):
    """Save detailed results for each tool"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed package information for each tool
    for tool_name, results in analysis_results.items():
        detailed_file = os.path.join(output_dir, f'{tool_name}_detailed_classifications.csv')
        
        with open(detailed_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Package', 'Classifications', 'Classification_Count'])
            
            for package_info in results['packages']:
                classifications_str = '; '.join(package_info['classifications'])
                writer.writerow([
                    package_info['package'],
                    classifications_str,
                    package_info['classification_count']
                ])
        
        print(f"Saved detailed results for {tool_name} to {detailed_file}")

def save_summary_statistics(analysis_results, overall_counts, output_dir):
    """Save summary statistics"""
    os.makedirs(output_dir, exist_ok=True)
    
    # Tool-wise classification counts
    summary_file = os.path.join(output_dir, 'classification_summary_by_tool.csv')
    
    # Get all unique classifications
    all_classifications = set()
    for results in analysis_results.values():
        all_classifications.update(results['classification_counts'].keys())
    all_classifications = sorted(list(all_classifications))
    
    with open(summary_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['Tool', 'Total_FN_Packages', 'Packages_with_Classifications'] + all_classifications
        writer.writerow(header)
        
        for tool_name, results in analysis_results.items():
            row = [
                tool_name,
                results['total_fn_packages'],
                results['total_packages']
            ]
            
            for classification in all_classifications:
                count = results['classification_counts'].get(classification, 0)
                row.append(count)
            
            writer.writerow(row)
    
    print(f"Saved tool-wise summary to {summary_file}")
    
    # Overall classification statistics
    overall_file = os.path.join(output_dir, 'overall_classification_statistics.csv')
    
    with open(overall_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Classification', 'Total_Count', 'Percentage'])
        
        total_classifications = sum(overall_counts.values())
        
        for classification, count in sorted(overall_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_classifications * 100) if total_classifications > 0 else 0
            writer.writerow([classification, count, f"{percentage:.2f}%"])
    
    print(f"Saved overall statistics to {overall_file}")

def main():
    # Configuration
    csv_file_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/behavior_annoation/key_results/package_all_classifications.csv"
    base_directory = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    output_directory = "/Users/kzyinglili/Documents/malware_analysis_results"
    
    print("Starting malware classification analysis...")
    
    # Load package classifications
    print("Loading package classifications...")
    package_classifications = load_package_classifications(csv_file_path)
    print(f"Loaded classifications for {len(package_classifications)} packages")
    
    # Load false negatives
    print("Loading false negative data...")
    false_negatives, tools_found = load_false_negatives(base_directory)
    print(f"Found {len(tools_found)} tools: {', '.join(tools_found)}")
    
    if not false_negatives:
        print("No false negative data found. Please check the directory path and file structure.")
        return
    
    # Analyze classifications
    print("Analyzing classifications...")
    analysis_results, overall_counts = analyze_classifications(package_classifications, false_negatives)
    
    # Save results
    print("Saving results...")
    save_detailed_results(analysis_results, output_directory)
    save_summary_statistics(analysis_results, overall_counts, output_directory)
    
    # Print summary
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"Total tools analyzed: {len(analysis_results)}")
    print(f"Total unique classifications: {len(overall_counts)}")
    print(f"Results saved to: {output_directory}")
    
    print("\nTop 5 most common classifications:")
    for classification, count in sorted(overall_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {classification}: {count}")
    
    print("\nTool-wise summary:")
    for tool_name, results in analysis_results.items():
        print(f"  {tool_name}: {results['total_packages']}/{results['total_fn_packages']} packages with classifications")

if __name__ == "__main__":
    main()