#!/usr/bin/env python3
"""
NPM Package Timestamp Collector
Collects publication timestamps for NPM packages from the NPM Registry API.
"""

import pandas as pd
import requests
import json
import time
import re
from datetime import datetime
from collections import Counter
import sys
from pathlib import Path

# Configuration
BATCH_SIZE = 50
BASE_URL = "https://registry.npmjs.org/"

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
INPUT_CSV = SCRIPT_DIR / "malware_packages.csv"
OUTPUT_CSV = SCRIPT_DIR / "malware_time.csv"


def save_batch(dataframe, batch_num, output_prefix="malware_time_batch"):
    """Save intermediate batch results"""
    temp_file = SCRIPT_DIR / f'{output_prefix}_{batch_num}.csv'
    dataframe.to_csv(temp_file, index=False)
    print(f"Saved batch {batch_num} to {temp_file}")


def show_progress(current, total):
    """Display progress bar"""
    progress = current / total * 100
    sys.stdout.write(f"\rProgress: [{current}/{total}] {progress:.2f}% complete")
    sys.stdout.flush()


def fetch_timestamp(package_name, version):
    """
    Fetch timestamp for a specific package version from NPM Registry.

    Returns:
        tuple: (timestamp_str, year) or (None, None) if failed
    """
    url = BASE_URL + package_name

    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            return None, None

        package_data = response.json()

        if 'time' not in package_data:
            return None, None

        # Try direct version match
        if version in package_data['time']:
            timestamp_str = package_data['time'][version]
            try:
                year = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).year
                return timestamp_str, year
            except ValueError:
                return timestamp_str, None

        # Handle special case: find security versions
        security_versions = []
        for ver in package_data['time']:
            if ver not in ['created', 'modified', 'unpublished']:
                if '-security.' in ver:
                    match = re.search(r'-security\.(\d+)$', ver)
                    if match:
                        security_num = int(match.group(1))
                        security_versions.append((ver, security_num))

        # If security versions found, use the highest numbered one
        if security_versions:
            security_versions.sort(key=lambda x: x[1], reverse=True)
            best_match = security_versions[0][0]
            timestamp_str = package_data['time'][best_match]
            print(f"\nVersion {version} not found, using {best_match} for {package_name}")
            try:
                year = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).year
                return timestamp_str, year
            except ValueError:
                return timestamp_str, None

        # Fallback: use the last available version
        available_versions = [v for v in package_data['time']
                            if v not in ['created', 'modified', 'unpublished']]
        if available_versions:
            closest_version = available_versions[-1]
            timestamp_str = package_data['time'][closest_version]
            print(f"\nVersion {version} not found, using {closest_version} for {package_name}")
            try:
                year = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).year
                return timestamp_str, year
            except ValueError:
                return timestamp_str, None

        return None, None

    except Exception as e:
        print(f"\nError processing {package_name}: {str(e)}")
        return None, None


def collect_timestamps(input_csv, output_csv):
    """
    Main function to collect timestamps for all packages in the input CSV.

    Args:
        input_csv: Path to input CSV with package_name and version columns
        output_csv: Path to output CSV with added timestamp column
    """
    print(f"Reading input CSV: {input_csv}")
    df = pd.read_csv(input_csv)
    total_rows = len(df)

    # Initialize timestamp column
    df['timestamp'] = None

    # Statistics
    year_counts = Counter()
    failed_count = 0
    processed_count = 0

    print(f"Processing {total_rows} packages...")

    for index, row in df.iterrows():
        package_name = row['package_name']
        version = row['version']

        timestamp_str, year = fetch_timestamp(package_name, version)

        if timestamp_str:
            df.at[index, 'timestamp'] = timestamp_str
            if year:
                year_counts[year] += 1
        else:
            failed_count += 1

        processed_count += 1
        show_progress(processed_count, total_rows)

        # Save batch periodically
        if processed_count % BATCH_SIZE == 0:
            save_batch(df[:processed_count], processed_count // BATCH_SIZE)

        # Rate limiting
        time.sleep(0.5)

    # Save final results
    df.to_csv(output_csv, index=False)
    print(f"\n\nSaved final results to {output_csv}")

    # Print statistics
    print("\n=== Statistics ===")
    print(f"Total packages: {total_rows}")
    print(f"Failed to get timestamp: {failed_count}")
    print(f"Successfully retrieved: {total_rows - failed_count}")

    print("\nDistribution by year:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]} packages")

    if total_rows > 0:
        success_rate = (total_rows - failed_count) / total_rows * 100
        print(f"\nSuccess rate: {success_rate:.2f}%")

    return df


def main():
    """Main entry point"""
    print("NPM Package Timestamp Collector")
    print("=" * 40)

    if not INPUT_CSV.exists():
        print(f"Error: Input file not found: {INPUT_CSV}")
        return

    collect_timestamps(INPUT_CSV, OUTPUT_CSV)


if __name__ == "__main__":
    main()
