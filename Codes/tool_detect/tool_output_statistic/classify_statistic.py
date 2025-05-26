import pandas as pd
import json
import os
from collections import defaultdict, Counter
import ast

def load_classifications(csv_file_path):
    """Load package classifications from CSV file"""
    classifications = {}
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            # Parse the CSV line
            parts = line.split(',', 3)  # Split into 4 parts max
            if len(parts) >= 4:
                package_id = parts[0].strip()
                package_name = parts[1].strip()
                version = parts[2].strip()
                classifications_str = parts[3].strip()
                
                # Parse the classifications list
                try:
                    # Remove quotes and parse as Python list
                    classifications_str = classifications_str.strip('"')
                    package_classifications = ast.literal_eval(classifications_str)
                    classifications[package_id] = {
                        'package_name': package_name,
                        'version': version,
                        'classifications': package_classifications
                    }
                except:
                    print(f"Error parsing classifications for {package_id}")
    
    return classifications

def load_json_reports(base_dir):
    """Load all JSON reports from tool directories"""
    reports = {}
    
    # Get all tool directories
    if not os.path.exists(base_dir):
        print(f"Base directory {base_dir} does not exist")
        return reports
    
    for tool_name in os.listdir(base_dir):
        tool_path = os.path.join(base_dir, tool_name)
        if os.path.isdir(tool_path):
            reports[tool_name] = {}
            
            # Load each JSON file
            json_files = ['benign_reports.json', 'false_negatives.json', 
                         'false_positives.json', 'malicious_reports.json']
            
            for json_file in json_files:
                json_path = os.path.join(tool_path, json_file)
                if os.path.exists(json_path):
                    try:
                        with open(json_path, 'r', encoding='utf-8') as f:
                            reports[tool_name][json_file.replace('.json', '')] = json.load(f)
                    except Exception as e:
                        print(f"Error loading {json_path}: {e}")
                        reports[tool_name][json_file.replace('.json', '')] = {}
    
    return reports

def extract_package_info(package_key):
    """Extract package name and version from package key"""
    # Handle different formats: "package-name/version" or "package-name-version"
    if '/' in package_key:
        parts = package_key.rsplit('/', 1)
        return parts[0], parts[1]
    else:
        # Try to split by last dash for version
        parts = package_key.rsplit('-', 1)
        if len(parts) == 2 and parts[1].replace('.', '').isdigit():
            return parts[0], parts[1]
        else:
            return package_key, "unknown"

def analyze_classifications_by_category(classifications, reports):
    """Analyze classifications for packages in different categories"""
    
    # Initialize counters
    category_stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    classification_counts = defaultdict(lambda: defaultdict(int))
    
    # Process each tool's reports
    for tool_name, tool_reports in reports.items():
        for category, packages in tool_reports.items():
            for package_key in packages.keys():
                # Extract package info
                package_name, version = extract_package_info(package_key)
                
                # Try to find matching classification
                package_id = f"{package_name}-{version}"
                alt_package_id = f"{package_name}/{version}"
                
                found_classifications = None
                if package_id in classifications:
                    found_classifications = classifications[package_id]['classifications']
                elif alt_package_id in classifications:
                    found_classifications = classifications[alt_package_id]['classifications']
                
                # Count classifications
                if found_classifications:
                    for classification in found_classifications:
                        category_stats[tool_name][category][classification] += 1
                        classification_counts[classification][category] += 1
    
    return category_stats, classification_counts

def generate_statistics_csv(category_stats, classification_counts, output_dir):
    """Generate CSV statistics files"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Tool-specific statistics
    for tool_name, tool_data in category_stats.items():
        tool_stats = []
        for category, classifications in tool_data.items():
            for classification, count in classifications.items():
                tool_stats.append({
                    'tool': tool_name,
                    'category': category,
                    'classification': classification,
                    'count': count
                })
        
        if tool_stats:
            df = pd.DataFrame(tool_stats)
            df.to_csv(os.path.join(output_dir, f'{tool_name}_classification_stats.csv'), index=False)
    
    # 2. Overall classification statistics
    overall_stats = []
    for classification, categories in classification_counts.items():
        for category, count in categories.items():
            overall_stats.append({
                'classification': classification,
                'category': category,
                'count': count
            })
    
    if overall_stats:
        df_overall = pd.DataFrame(overall_stats)
        df_overall.to_csv(os.path.join(output_dir, 'overall_classification_stats.csv'), index=False)
    
    # 3. Summary statistics
    summary_stats = []
    all_classifications = set()
    all_categories = set()
    all_tools = set()
    
    for tool_name, tool_data in category_stats.items():
        all_tools.add(tool_name)
        for category, classifications in tool_data.items():
            all_categories.add(category)
            for classification in classifications.keys():
                all_classifications.add(classification)
    
    # Create pivot table for summary
    summary_data = []
    for classification in sorted(all_classifications):
        row = {'classification': classification}
        for category in sorted(all_categories):
            total_count = sum(category_stats[tool][category][classification] 
                            for tool in all_tools 
                            if category in category_stats[tool])
            row[category] = total_count
        summary_data.append(row)
    
    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_csv(os.path.join(output_dir, 'classification_summary.csv'), index=False)
    
    return len(overall_stats), len(all_classifications), len(all_tools)

def main():
    # Configuration
    csv_file_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/behavior_annoation/key_results/package_all_classifications.csv"
    
    base_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    output_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/malware_analysis_output"
    
    print("Loading package classifications...")
    classifications = load_classifications(csv_file_path)
    print(f"Loaded {len(classifications)} package classifications")
    
    print("Loading JSON reports...")
    reports = load_json_reports(base_dir)
    print(f"Loaded reports for {len(reports)} tools")
    
    print("Analyzing classifications...")
    category_stats, classification_counts = analyze_classifications_by_category(classifications, reports)
    
    print("Generating statistics CSV files...")
    total_records, total_classifications, total_tools = generate_statistics_csv(
        category_stats, classification_counts, output_dir)
    
    print(f"\nAnalysis complete!")
    print(f"- Total tools analyzed: {total_tools}")
    print(f"- Total unique classifications: {total_classifications}")
    print(f"- Total records generated: {total_records}")
    print(f"- Output files saved to: {output_dir}")
    
    # Display sample statistics
    print("\nSample classification counts:")
    for classification, categories in list(classification_counts.items())[:5]:
        print(f"  {classification}: {dict(categories)}")

if __name__ == "__main__":
    main()