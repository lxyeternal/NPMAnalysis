#!/usr/bin/env python3
"""
Analyze Packj trace results to extract syscall statistics (process, files, network).
"""

import os
import re
import json
from pathlib import Path


TRACE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/packj/result_trace"
OUTPUT_FILE = "/home2/wenbo/Documents/NPMAnalysis/Core/tool_detect/packj_trace_analysis.json"


def extract_syscall_data(file_path):
    """
    Extract process, files, network syscall counts from result.txt.
    Only processes files containing "risk(s) apply to you".
    Returns (process_count, files_count, network_count) or None.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if "risk(s) apply to you" not in content:
            return None

        # Match pattern: found 161 process,15 files,558 network syscalls
        pattern = r'found (\d+) process,(\d+) files,(\d+) network syscalls'
        match = re.search(pattern, content)

        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return None

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def analyze_directory(base_dir, label):
    """Analyze all result files in a directory (benign or malware)."""
    target_dir = os.path.join(base_dir, label)
    if not os.path.exists(target_dir):
        print(f"Directory not found: {target_dir}")
        return []

    valid_packages = []
    total_files = 0

    for package_name in os.listdir(target_dir):
        package_dir = os.path.join(target_dir, package_name)
        if not os.path.isdir(package_dir):
            continue

        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            if not os.path.isdir(version_dir):
                continue

            # Find result file
            files = [f for f in os.listdir(version_dir) if os.path.isfile(os.path.join(version_dir, f))]
            if not files:
                continue

            total_files += 1
            file_path = os.path.join(version_dir, files[0])
            data = extract_syscall_data(file_path)

            if data:
                valid_packages.append({
                    'package_name': package_name.replace('##', '/'),
                    'version': version,
                    'label': label,
                    'process_count': data[0],
                    'files_count': data[1],
                    'network_count': data[2]
                })

    print(f"{label}: {len(valid_packages)}/{total_files} packages with risk syscalls")
    return valid_packages


def compute_stats(packages, field):
    """Compute statistics for a given field."""
    values = [p[field] for p in packages]
    if not values:
        return {'count': 0, 'avg': 0, 'min': 0, 'max': 0, 'total': 0}

    return {
        'count': len(values),
        'avg': round(sum(values) / len(values), 2),
        'min': min(values),
        'max': max(values),
        'total': sum(values),
        'non_zero': sum(1 for v in values if v > 0)
    }


def main():
    if not os.path.exists(TRACE_DIR):
        print(f"Error: Directory not found {TRACE_DIR}")
        return

    print(f"Analyzing Packj trace results in: {TRACE_DIR}\n")

    # Analyze both benign and malware
    all_packages = []
    for label in ['benign', 'malware']:
        packages = analyze_directory(TRACE_DIR, label)
        all_packages.extend(packages)

    if not all_packages:
        print("No valid packages found.")
        return

    # Compute statistics
    print(f"\n{'='*60}")
    print("Syscall Statistics Summary")
    print('='*60)

    for field, name in [('process_count', 'Process'), ('files_count', 'Files'), ('network_count', 'Network')]:
        stats = compute_stats(all_packages, field)
        print(f"\n{name} syscalls:")
        print(f"  Packages with data: {stats['non_zero']}/{stats['count']}")
        print(f"  Average: {stats['avg']}, Min: {stats['min']}, Max: {stats['max']}")
        print(f"  Total: {stats['total']}")

    # Compare benign vs malware
    benign = [p for p in all_packages if p['label'] == 'benign']
    malware = [p for p in all_packages if p['label'] == 'malware']

    print(f"\n{'='*60}")
    print("Benign vs Malware Comparison")
    print('='*60)
    print(f"{'Metric':<20} {'Benign Avg':>12} {'Malware Avg':>12}")
    print('-'*44)

    for field, name in [('process_count', 'Process'), ('files_count', 'Files'), ('network_count', 'Network')]:
        benign_stats = compute_stats(benign, field)
        malware_stats = compute_stats(malware, field)
        print(f"{name:<20} {benign_stats['avg']:>12.2f} {malware_stats['avg']:>12.2f}")

    # Save results
    results = {
        'summary': {
            'total_packages': len(all_packages),
            'benign_count': len(benign),
            'malware_count': len(malware),
            'process_stats': compute_stats(all_packages, 'process_count'),
            'files_stats': compute_stats(all_packages, 'files_count'),
            'network_stats': compute_stats(all_packages, 'network_count')
        },
        'packages': all_packages
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
