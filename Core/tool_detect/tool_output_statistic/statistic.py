#!/usr/bin/env python3
# filepath: /Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/count_npm_reports.py
import os
import glob
import fnmatch
import pandas as pd
import numpy as np
import json
from collections import defaultdict
import sys
import os

# 获取当前文件所在目录的上一级目录
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 添加到系统路径中
sys.path.append(parent_dir)
# Import the functions from accuracy_npm.py
from accuracy_npm import (load_skip_list, analyze_guarddog, analyze_ossgadget, 
                         analyze_packj, analyze_genie, analyze_socketai, extract_package_info, 
                         find_package_files)

def save_detection_results(tool_name, sub_tool=None):
    """
    Counts and saves detection results for each tool including:
    - malicious reports (true positives and false positives)
    - benign reports (true negatives and false negatives)
    - false negatives (malware classified as benign)
    - false positives (benign classified as malware)
    """
    base_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output"
    output_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    
    # Load skip lists
    malware_benign_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/dataclean/malware_benign.txt"
    selected_benign_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"
    
    malware_benign_skip_list = load_skip_list(malware_benign_path)
    selected_benign_skip_list = load_skip_list(selected_benign_path)
    
    # Determine tool function based on tool name
    if tool_name == "ossgadget":
        tool_function = analyze_ossgadget
    elif tool_name == "guarddog":
        tool_function = analyze_guarddog
    elif tool_name == "genie":
        tool_function = analyze_genie
    elif tool_name == "packj":
        tool_function = analyze_packj
    elif tool_name == "socketai":
        tool_function = analyze_socketai
    else:
        print(f"Unknown tool: {tool_name}")
        return
    
    # For packj tool with sub-tools
    if sub_tool:
        tool_path = os.path.join(base_path, tool_name, sub_tool)
        tool_output_dir = os.path.join(output_dir, f"{tool_name}_{sub_tool.replace('result_', '')}")
    else:
        tool_path = os.path.join(base_path, tool_name)
        tool_output_dir = os.path.join(output_dir, tool_name)
    
    # Create output directory if it doesn't exist
    os.makedirs(tool_output_dir, exist_ok=True)
    
    # Initialize data structures for storing results
    malicious_reports = {}  # TP (malware detected as malware)
    benign_reports = {}     # TN (benign detected as benign)
    false_negatives = {}    # FN (malware detected as benign)
    false_positives = {}    # FP (benign detected as malware)
    
    # Process benign samples
    benign_files = find_package_files(tool_path, "benign", tool_name)
    for file_path in benign_files:
        package_info = extract_package_info(file_path, "benign")
        
        # Skip packages in the skip list
        if package_info in selected_benign_skip_list:
            continue
        
        prediction = tool_function(file_path, "benign")
        
        if prediction == "benign":
            # True negative
            benign_reports[package_info] = {
                "file_path": file_path,
                "prediction": prediction,
                "actual": "benign"
            }
        elif prediction == "malware":
            # False positive
            false_positives[package_info] = {
                "file_path": file_path,
                "prediction": prediction,
                "actual": "benign"
            }
    
    # Process malware samples
    malware_files = find_package_files(tool_path, "malware", tool_name)
    for file_path in malware_files:
        package_info = extract_package_info(file_path, "malware")
        
        # Skip packages in the skip list
        if package_info in malware_benign_skip_list:
            continue
        
        prediction = tool_function(file_path, "malware")
        
        if prediction == "malware":
            # True positive
            malicious_reports[package_info] = {
                "file_path": file_path,
                "prediction": prediction,
                "actual": "malware"
            }
        elif prediction == "benign":
            # False negative
            false_negatives[package_info] = {
                "file_path": file_path,
                "prediction": prediction,
                "actual": "malware"
            }
    
    # Save results to JSON files
    with open(os.path.join(tool_output_dir, 'malicious_reports.json'), 'w') as f:
        json.dump(malicious_reports, f, indent=2)
    
    with open(os.path.join(tool_output_dir, 'benign_reports.json'), 'w') as f:
        json.dump(benign_reports, f, indent=2)
    
    with open(os.path.join(tool_output_dir, 'false_negatives.json'), 'w') as f:
        json.dump(false_negatives, f, indent=2)
    
    with open(os.path.join(tool_output_dir, 'false_positives.json'), 'w') as f:
        json.dump(false_positives, f, indent=2)
    
    # Print summary
    print(f"{tool_name}{' (' + sub_tool + ')' if sub_tool else ''} detection results:")
    print(f"Total malicious reports (TP): {len(malicious_reports)}")
    print(f"Total benign reports (TN): {len(benign_reports)}")
    print(f"Total false negatives (FN): {len(false_negatives)}")
    print(f"Total false positives (FP): {len(false_positives)}")
    print("-" * 50)

def save_sap_detection_results():
    """Save SAP ML algorithm detection results as JSON files"""
    base_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Tools/sap/scripts"
    output_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    
    # Load skip lists
    malware_benign_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/dataclean/malware_benign.txt"
    selected_benign_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/dataclean/selected_benign_packages.txt"
    
    malware_benign_skip_list = load_skip_list(malware_benign_path)
    selected_benign_skip_list = load_skip_list(selected_benign_path)
    
    # Convert skip lists to the format used in SAP results
    malware_benign_skip_converted = set()
    for item in malware_benign_skip_list:
        converted = item.replace('/', '$$')
        malware_benign_skip_converted.add(converted)
    
    selected_benign_skip_converted = set()
    for item in selected_benign_skip_list:
        converted = item.replace('/', '$$')
        selected_benign_skip_converted.add(converted)
    
    # Read SAP results
    sap_file_path = os.path.join(base_path, "sap_detection_results.csv")
    df = pd.read_csv(sap_file_path)
    
    # Process each ML algorithm
    algorithms = ['DT', 'RF', 'XGB']
    
    for algo in algorithms:
        # Create output directory for this algorithm
        algo_output_dir = os.path.join(output_dir, f"sap_{algo}")
        os.makedirs(algo_output_dir, exist_ok=True)
        
        # Initialize data structures for storing results
        malicious_reports = {}  # TP
        benign_reports = {}     # TN
        false_negatives = {}    # FN
        false_positives = {}    # FP
        
        # Process each package in the dataset
        for idx, row in df.iterrows():
            package_name = row['Package Name']
            sample_type = row['type']
            prediction = row[algo]
            
            # Skip packages in the skip lists
            if sample_type == 'malware' and package_name in malware_benign_skip_converted:
                continue
            if sample_type == 'benign' and package_name in selected_benign_skip_converted:
                continue
            
            # Convert package name to the standard format
            standard_package_name = str(package_name).replace('$$', '/')
            
            if sample_type == 'malware' and prediction == 1:
                # True positive
                malicious_reports[standard_package_name] = {
                    "prediction": "malware",
                    "actual": "malware"
                }
            elif sample_type == 'benign' and prediction == 0:
                # True negative
                benign_reports[standard_package_name] = {
                    "prediction": "benign",
                    "actual": "benign"
                }
            elif sample_type == 'malware' and prediction == 0:
                # False negative
                false_negatives[standard_package_name] = {
                    "prediction": "benign",
                    "actual": "malware"
                }
            elif sample_type == 'benign' and prediction == 1:
                # False positive
                false_positives[standard_package_name] = {
                    "prediction": "malware",
                    "actual": "benign"
                }
        
        # Save results to JSON files
        with open(os.path.join(algo_output_dir, 'malicious_reports.json'), 'w') as f:
            json.dump(malicious_reports, f, indent=2)
        
        with open(os.path.join(algo_output_dir, 'benign_reports.json'), 'w') as f:
            json.dump(benign_reports, f, indent=2)
        
        with open(os.path.join(algo_output_dir, 'false_negatives.json'), 'w') as f:
            json.dump(false_negatives, f, indent=2)
        
        with open(os.path.join(algo_output_dir, 'false_positives.json'), 'w') as f:
            json.dump(false_positives, f, indent=2)
        
        # Print summary
        print(f"SAP {algo} detection results:")
        print(f"Total malicious reports (TP): {len(malicious_reports)}")
        print(f"Total benign reports (TN): {len(benign_reports)}")
        print(f"Total false negatives (FN): {len(false_negatives)}")
        print(f"Total false positives (FP): {len(false_positives)}")
        print("-" * 50)

def main():
    """Main function to run the detection results saving"""
    # Create the stats output directory
    output_dir = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPMAnalysis/Codes/tool_detect/tool_output_statistic/reports/stats_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Starting to count and save NPM package detection reports...\n")
    
    # Process basic tools
    basic_tools = ["ossgadget", "guarddog", "genie", "socketai"]
    for tool_name in basic_tools:
        save_detection_results(tool_name)
    
    # Process packj tool with its sub-types
    packj_subtypes = ["result_static", "result_trace"]
    for subtype in packj_subtypes:
        save_detection_results("packj", subtype)
    
    # Process SAP ML algorithms
    save_sap_detection_results()
    
    print("\nCompleted saving all detection results!")
    print(f"Results saved to: {output_dir}")

if __name__ == "__main__":
    main()