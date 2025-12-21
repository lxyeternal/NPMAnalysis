#!/usr/bin/env python3
"""
Batch analysis script for GENIE tool.
Uses CodeQL to detect malicious code and obfuscation techniques in NPM packages.
"""

import os
import glob
import shutil
import subprocess
import time
from multiprocessing import Pool


# Configuration
# ====================================================
PROCESS_COUNT = 24
MALWARE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
BENIGN_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign"
OUTPUT_ROOT = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results/genie"
BENIGN_OUTPUT_DIR = os.path.join(OUTPUT_ROOT, "benign")
MALWARE_OUTPUT_DIR = os.path.join(OUTPUT_ROOT, "malware")
ANALYZE_MALWARE = True
ANALYZE_BENIGN = True
USE_OBFUSCATOR_QUERIES = True
SCAN_MODE = "BATCH"  # Options: "INDIVIDUAL" or "BATCH"
# ====================================================

# GENIE directory structure
GENIE_ROOT = "/home2/wenbo/Documents/NPMAnalysis/Tools/GENIE"
GENIE_SNAPSHOT = os.path.join(GENIE_ROOT, "snapshot")
GENIE_REGISTRY = os.path.join(GENIE_SNAPSHOT, "1_Registry/NPM")
GENIE_CODEBASE = os.path.join(GENIE_SNAPSHOT, "2_CodeBase/NPM")
GENIE_DATABASE = os.path.join(GENIE_SNAPSHOT, "3_DataBase/NPM")
GENIE_QUERY_OUTPUT = os.path.join(GENIE_SNAPSHOT, "4_query/output")
GENIE_MALWARE_QUERIES = os.path.join(GENIE_ROOT, "queries/malware")
GENIE_OBFUSCATOR_QUERIES = os.path.join(GENIE_ROOT, "queries/obfuscator")


def init_directories():
    """Ensure all required directories exist."""
    for directory in [GENIE_REGISTRY, GENIE_CODEBASE, GENIE_DATABASE, GENIE_QUERY_OUTPUT,
                      BENIGN_OUTPUT_DIR, MALWARE_OUTPUT_DIR]:
        os.makedirs(directory, exist_ok=True)


def get_package_id(package_path):
    """Generate unique ID from package path (package_name-version)."""
    return os.path.basename(package_path)


def is_already_analyzed(package_path, is_malware):
    """Check if package has already been analyzed."""
    package_id = get_package_id(package_path)
    output_dir = MALWARE_OUTPUT_DIR if is_malware else BENIGN_OUTPUT_DIR
    expected_output = os.path.join(output_dir, f"{package_id}.csv")
    return os.path.exists(expected_output)


def process_package(args):
    """Process a single package directory with full GENIE analysis pipeline."""
    package_path, is_malware = args
    package_id = get_package_id(package_path)
    label = "malware" if is_malware else "benign"
    print(f"Processing: {package_id} ({label})")

    try:
        if is_already_analyzed(package_path, is_malware):
            print(f"Skipping already analyzed: {package_id}")
            return (package_id, True, "Already analyzed, skipped")

        unique_id = f"{package_id}_{int(time.time())}"

        # 1. Copy to CodeBase directory
        codebase_dir = os.path.join(GENIE_CODEBASE, unique_id)
        os.makedirs(codebase_dir, exist_ok=True)

        for item in os.listdir(package_path):
            s = os.path.join(package_path, item)
            d = os.path.join(codebase_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        # 2. Create CodeQL database
        database_dir = os.path.join(GENIE_DATABASE, unique_id)
        os.makedirs(database_dir, exist_ok=True)

        create_db_cmd = [
            'codeql', 'database', 'create',
            '--source-root=' + codebase_dir,
            '--language=javascript',
            '--verbosity=progress',
            database_dir
        ]

        db_process = subprocess.run(create_db_cmd, capture_output=True, text=True)
        if db_process.returncode != 0:
            print(f"Database creation failed for {package_id}: {db_process.stderr}")
            shutil.rmtree(codebase_dir, ignore_errors=True)
            shutil.rmtree(database_dir, ignore_errors=True)
            return (package_id, False, "Database creation failed")

        # Create merged output file
        merged_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-merged-results.csv")
        with open(merged_output_file, 'w') as merged_file:
            pass

        malware_detected = False
        obfuscation_detected = False
        detected_malware_types = []
        detected_obfuscator_types = []

        # 3. Run queries based on scan mode
        if SCAN_MODE == "INDIVIDUAL":
            malware_queries = glob.glob(os.path.join(GENIE_MALWARE_QUERIES, "*.ql"))
            malware_successful_queries = 0
            total_malware_queries = len(malware_queries)

            print(f"  Running {total_malware_queries} malware queries...")

            for query_file in malware_queries:
                query_name = os.path.basename(query_file).replace(".ql", "")
                query_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-{query_name}-results.csv")

                query_cmd = [
                    'codeql', 'database', 'analyze',
                    '--format=csv',
                    '--output=' + query_output_file,
                    database_dir,
                    query_file
                ]

                try:
                    query_process = subprocess.run(query_cmd, capture_output=True, text=True)

                    if query_process.returncode == 0:
                        malware_successful_queries += 1

                        if os.path.exists(query_output_file) and os.path.getsize(query_output_file) > 0:
                            malware_detected = True
                            detected_malware_types.append(query_name)

                            with open(query_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                                dest.write(f"# Query: {query_name} (malware)\n")
                                dest.write(src.read())
                                dest.write("\n")
                    else:
                        print(f"  Query {query_name} failed: {query_process.stderr[:100]}...")
                except Exception as e:
                    print(f"  Query {query_name} exception: {str(e)}")

            print(f"  Malware queries completed: {malware_successful_queries}/{total_malware_queries} successful")
            if detected_malware_types:
                print(f"  Detected malware types: {', '.join(detected_malware_types)}")

            # 4. Run obfuscator queries if enabled
            if USE_OBFUSCATOR_QUERIES:
                obfuscator_queries = glob.glob(os.path.join(GENIE_OBFUSCATOR_QUERIES, "*.ql"))
                obfuscator_successful_queries = 0
                total_obfuscator_queries = len(obfuscator_queries)

                print(f"  Running {total_obfuscator_queries} obfuscator queries...")

                for query_file in obfuscator_queries:
                    query_name = os.path.basename(query_file).replace(".ql", "")
                    query_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-{query_name}-results.csv")

                    query_cmd = [
                        'codeql', 'database', 'analyze',
                        '--format=csv',
                        '--output=' + query_output_file,
                        database_dir,
                        query_file
                    ]

                    try:
                        query_process = subprocess.run(query_cmd, capture_output=True, text=True)

                        if query_process.returncode == 0:
                            obfuscator_successful_queries += 1

                            if os.path.exists(query_output_file) and os.path.getsize(query_output_file) > 0:
                                obfuscation_detected = True
                                detected_obfuscator_types.append(query_name)

                                with open(query_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                                    dest.write(f"# Query: {query_name} (obfuscator)\n")
                                    dest.write(src.read())
                                    dest.write("\n")
                        else:
                            print(f"  Query {query_name} failed: {query_process.stderr[:100]}...")
                    except Exception as e:
                        print(f"  Query {query_name} exception: {str(e)}")

                print(f"  Obfuscator queries completed: {obfuscator_successful_queries}/{total_obfuscator_queries} successful")
                if detected_obfuscator_types:
                    print(f"  Detected obfuscator types: {', '.join(detected_obfuscator_types)}")

            if malware_successful_queries == 0 and (not USE_OBFUSCATOR_QUERIES or obfuscator_successful_queries == 0):
                shutil.rmtree(codebase_dir, ignore_errors=True)
                shutil.rmtree(database_dir, ignore_errors=True)
                return (package_id, False, "All queries failed")

        else:  # SCAN_MODE == "BATCH"
            print("  Using batch scan mode...")

            # 3. Run malware queries
            malware_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-malware-results.csv")

            malware_analyze_cmd = [
                'codeql', 'database', 'analyze',
                '--format=csv',
                '--output=' + malware_output_file,
                database_dir,
                GENIE_MALWARE_QUERIES
            ]

            print("  Running malware queries...")
            malware_process = subprocess.run(malware_analyze_cmd, capture_output=True, text=True)
            malware_success = malware_process.returncode == 0

            if malware_success:
                if os.path.exists(malware_output_file) and os.path.getsize(malware_output_file) > 0:
                    malware_detected = True
                    try:
                        with open(malware_output_file, 'r') as f:
                            first_line = f.readline().strip()
                            if first_line and len(first_line.split(',')) > 0:
                                query_name = first_line.split(',')[0].strip('"')
                                detected_malware_types.append(query_name)
                    except:
                        detected_malware_types.append("unknown-malware")

                    with open(malware_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                        dest.write("# Batch malware query results\n")
                        dest.write(src.read())
                        dest.write("\n")
                print("  Malware queries completed")
            else:
                print(f"  Malware analysis failed: {malware_process.stderr[:100]}...")

            # 4. Run obfuscator queries if enabled
            if USE_OBFUSCATOR_QUERIES:
                obfuscator_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-obfuscator-results.csv")

                obfuscator_analyze_cmd = [
                    'codeql', 'database', 'analyze',
                    '--format=csv',
                    '--output=' + obfuscator_output_file,
                    database_dir,
                    GENIE_OBFUSCATOR_QUERIES
                ]

                print("  Running obfuscator queries...")
                obfuscator_process = subprocess.run(obfuscator_analyze_cmd, capture_output=True, text=True)
                obfuscator_success = obfuscator_process.returncode == 0

                if obfuscator_success:
                    if os.path.exists(obfuscator_output_file) and os.path.getsize(obfuscator_output_file) > 0:
                        obfuscation_detected = True
                        try:
                            with open(obfuscator_output_file, 'r') as f:
                                first_line = f.readline().strip()
                                if first_line and len(first_line.split(',')) > 0:
                                    query_name = first_line.split(',')[0].strip('"')
                                    detected_obfuscator_types.append(query_name)
                        except:
                            detected_obfuscator_types.append("unknown-obfuscator")

                        with open(obfuscator_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                            dest.write("# Batch obfuscator query results\n")
                            dest.write(src.read())
                    print("  Obfuscator queries completed")
                else:
                    print(f"  Obfuscator analysis failed: {obfuscator_process.stderr[:100]}...")

            if not malware_success and (USE_OBFUSCATOR_QUERIES and not obfuscator_success):
                shutil.rmtree(codebase_dir, ignore_errors=True)
                shutil.rmtree(database_dir, ignore_errors=True)
                return (package_id, False, "Batch queries failed")

        # 6. Move results to final directory
        output_dir = MALWARE_OUTPUT_DIR if is_malware else BENIGN_OUTPUT_DIR
        final_output_file = os.path.join(output_dir, f"{package_id}.csv")

        os.makedirs(os.path.dirname(final_output_file), exist_ok=True)
        shutil.copy2(merged_output_file, final_output_file)

        # 7. Determine analysis status
        if malware_detected and obfuscation_detected:
            result_status = f"Found malware ({len(detected_malware_types)} types) and obfuscation ({len(detected_obfuscator_types)} types)"
        elif malware_detected:
            result_status = f"Found malware ({len(detected_malware_types)} types)"
        elif obfuscation_detected:
            result_status = f"Found obfuscation ({len(detected_obfuscator_types)} types)"
        else:
            result_status = "No malware or obfuscation detected"

        # 8. Cleanup work directories
        shutil.rmtree(codebase_dir, ignore_errors=True)
        shutil.rmtree(database_dir, ignore_errors=True)

        return (package_id, True, result_status, detected_malware_types, detected_obfuscator_types)

    except Exception as e:
        print(f"Error processing {package_id}: {str(e)}")
        return (package_id, False, f"Error: {str(e)}")


def collect_packages():
    """Collect all package directories to analyze."""
    packages = []

    if ANALYZE_MALWARE:
        for package_dir in sorted(glob.glob(os.path.join(MALWARE_DIR, "*"))):
            if os.path.isdir(package_dir):
                packages.append((package_dir, True))

    if ANALYZE_BENIGN:
        for package_dir in sorted(glob.glob(os.path.join(BENIGN_DIR, "*"))):
            if os.path.isdir(package_dir):
                packages.append((package_dir, False))

    return packages


def main():
    """Main function to run batch analysis."""
    init_directories()

    all_packages = collect_packages()

    packages_to_analyze = []
    skipped_packages = []

    for package_info in all_packages:
        package_path, is_malware = package_info
        if is_already_analyzed(package_path, is_malware):
            skipped_packages.append((get_package_id(package_path), is_malware))
        else:
            packages_to_analyze.append(package_info)

    if not packages_to_analyze:
        print("All packages already analyzed, nothing to do")
        return

    print(f"Total packages found: {len(all_packages)}")
    print(f"Skipping already analyzed: {len(skipped_packages)}")
    print(f"Packages to analyze: {len(packages_to_analyze)}")
    print(f"Using {PROCESS_COUNT} processes")
    print(f"Obfuscator queries: {'enabled' if USE_OBFUSCATOR_QUERIES else 'disabled'}")
    print(f"Scan mode: {'individual' if SCAN_MODE == 'INDIVIDUAL' else 'batch'}")

    for i, (package_id, is_malware) in enumerate(skipped_packages[:10]):
        label = "malware" if is_malware else "benign"
        print(f"  Skipping: {package_id} ({label})")
    if len(skipped_packages) > 10:
        print(f"  ...and {len(skipped_packages) - 10} more")

    for i, (package_path, is_malware) in enumerate(packages_to_analyze[:10]):
        label = "malware" if is_malware else "benign"
        print(f"  Analyzing: {get_package_id(package_path)} ({label})")
    if len(packages_to_analyze) > 10:
        print(f"  ...and {len(packages_to_analyze) - 10} more")

    start_time = time.time()
    with Pool(processes=PROCESS_COUNT) as pool:
        results = pool.map(process_package, packages_to_analyze)

    # Statistics
    successful = sum(1 for r in results if r[1])
    malicious = sum(1 for r in results if r[1] and "Found malware" in r[2])
    obfuscated = sum(1 for r in results if r[1] and "Found obfuscation" in r[2])

    malware_type_counts = {}
    obfuscator_type_counts = {}

    for r in results:
        if r[1]:
            if len(r) > 3:
                if len(r) > 3 and r[3]:
                    for malware_type in r[3]:
                        malware_type_counts[malware_type] = malware_type_counts.get(malware_type, 0) + 1

                if len(r) > 4 and r[4]:
                    for obfuscator_type in r[4]:
                        obfuscator_type_counts[obfuscator_type] = obfuscator_type_counts.get(obfuscator_type, 0) + 1

    print(f"\nAnalysis completed: {len(results)} packages total")
    print(f"Successful: {successful}, Failed: {len(results) - successful}")
    print(f"Malicious packages detected: {malicious}")

    if malware_type_counts:
        print("\nMalware type statistics:")
        for malware_type, count in sorted(malware_type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {malware_type}: {count} packages")

    if USE_OBFUSCATOR_QUERIES and obfuscator_type_counts:
        print("\nObfuscator type statistics:")
        for obfuscator_type, count in sorted(obfuscator_type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {obfuscator_type}: {count} packages")

    print(f"\nTotal time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
