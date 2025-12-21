#!/usr/bin/env python3
import os
import shutil

def check_and_remove_timeout_folders(base_path):
    """
    Check all result.txt files in the given path.
    If a file contains 'ERROR: Timeout', delete its parent folder.
    """
    # Categories: benign and malware
    categories = ['benign', 'malware']
    
    # Counter for statistics
    removed_count = 0
    
    for category in categories:
        category_path = os.path.join(base_path, category)
        
        # Skip if category folder doesn't exist
        if not os.path.exists(category_path):
            print(f"Warning: {category_path} does not exist")
            continue
        
        # List all package folders
        for package_name in os.listdir(category_path):
            package_path = os.path.join(category_path, package_name)
            
            # Skip if not a directory
            if not os.path.isdir(package_path):
                continue
            
            # List all version folders
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                
                # Skip if not a directory
                if not os.path.isdir(version_path):
                    continue
                
                # Check result.txt file
                result_file = os.path.join(version_path, "result.txt")
                if os.path.exists(result_file):
                    try:
                        with open(result_file, 'r') as f:
                            content = f.read().strip()
                            
                        if content == "ERROR: Timeout":
                            print(f"Removing: {version_path}")
                            shutil.rmtree(version_path)
                            removed_count += 1
                    except Exception as e:
                        print(f"Error processing {result_file}: {e}")
    
    print(f"Total folders removed: {removed_count}")

if __name__ == "__main__":
    base_path = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/packj/result_trace"
    check_and_remove_timeout_folders(base_path)
