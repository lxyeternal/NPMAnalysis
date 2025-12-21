#!/usr/bin/env python3
"""
Run detection tools (GuardDog, OSSGadget) on NPM package datasets.
Processes both benign and malware samples with multi-processing support.
"""

import os
import subprocess
import multiprocessing
import time


# Configuration
NUM_PROCESSES = 24
TOOL_TIMEOUT = 300  # seconds

# Paths
DATASET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset"
RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"
TOOLS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Tools"


def run_with_timeout(cmd, timeout=TOOL_TIMEOUT):
    """Run command with timeout, return (code, stdout, stderr, time)."""
    start_time = time.time()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return_code = process.returncode
        execution_time = time.time() - start_time
        return (return_code, stdout, stderr, execution_time)
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            process.wait(timeout=5)
        except:
            pass
        return (-1, f"Command timed out after {timeout} seconds", "", timeout)


class NPMToolDetector:
    def __init__(self):
        # Dataset paths
        self.zip_benign_path = os.path.join(DATASET_DIR, "zip_benign")
        self.zip_malware_path = os.path.join(DATASET_DIR, "zip_malware")
        self.unzip_benign_path = os.path.join(DATASET_DIR, "unzip_benign")
        self.unzip_malware_path = os.path.join(DATASET_DIR, "unzip_malware")

        # Output paths
        self.output_paths = {
            "guarddog": {
                "benign": os.path.join(RESULTS_DIR, "guarddog/benign"),
                "malware": os.path.join(RESULTS_DIR, "guarddog/malware")
            },
            "ossgadget": {
                "benign": os.path.join(RESULTS_DIR, "ossgadget/benign"),
                "malware": os.path.join(RESULTS_DIR, "ossgadget/malware")
            }
        }

        # Timeout logs
        self.timeout_log_dir = os.path.join(RESULTS_DIR, "timeout_logs")
        os.makedirs(self.timeout_log_dir, exist_ok=True)
        self.guarddog_timeout_log = os.path.join(self.timeout_log_dir, "guarddog_timeout.txt")
        self.ossgadget_timeout_log = os.path.join(self.timeout_log_dir, "ossgadget_timeout.txt")

        # Ensure output directories exist
        self._ensure_output_dirs()

        # Counters
        self.processed_count = 0
        self.skipped_count = 0

    def _ensure_output_dirs(self):
        """Ensure all output directories exist."""
        for tool in self.output_paths:
            for category in self.output_paths[tool]:
                os.makedirs(self.output_paths[tool][category], exist_ok=True)

    def _create_output_path(self, tool, category, package_name, version):
        """Create output file path with directory structure."""
        base_dir = self.output_paths[tool][category]

        # Create package directory
        package_dir = os.path.join(base_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)

        # Create version directory
        version_dir = os.path.join(package_dir, version)
        os.makedirs(version_dir, exist_ok=True)

        return os.path.join(version_dir, "result.txt")

    def _log_timeout(self, tool, category, package_name, version, input_path):
        """Log timeout information."""
        log_file = self.guarddog_timeout_log if tool == "guarddog" else self.ossgadget_timeout_log
        log_entry = f"{category},{package_name},{version},{input_path}\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def run_guarddog(self, zip_file_path, package_name, version, category):
        """Run GuardDog tool and save results."""
        output_file = self._create_output_path("guarddog", category, package_name, version)

        # Skip if already processed
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Skipping GuardDog (already processed): {package_name}@{version}")
            return None

        cmd = ["guarddog", "npm", "scan", zip_file_path]
        print(f"Running GuardDog: {package_name}@{version}")
        return_code, stdout, stderr, execution_time = run_with_timeout(cmd)

        if return_code == -1:  # Timeout
            print(f"GuardDog timeout: {package_name}@{version}")
            self._log_timeout("guarddog", category, package_name, version, zip_file_path)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("TIMEOUT")
            return "TIMEOUT"
        else:
            output = stdout if stdout.strip() else "benign"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"GuardDog completed: {package_name}@{version} ({execution_time:.2f}s)")
            return output

    def run_ossgadget(self, unzip_dir_path, package_name, version, category):
        """Run OSSGadget tool and save results."""
        output_file = self._create_output_path("ossgadget", category, package_name, version)

        # Skip if already processed
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Skipping OSSGadget (already processed): {package_name}@{version}")
            return None

        ossgadget_bin = os.path.join(TOOLS_DIR, "OSSGadget/oss-detect-backdoor")
        cmd = [ossgadget_bin, unzip_dir_path]
        print(f"Running OSSGadget: {package_name}@{version}")
        return_code, stdout, stderr, execution_time = run_with_timeout(cmd)

        if return_code == -1:  # Timeout
            print(f"OSSGadget timeout: {package_name}@{version}")
            self._log_timeout("ossgadget", category, package_name, version, unzip_dir_path)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("TIMEOUT")
            return "TIMEOUT"
        else:
            output = stdout if stdout.strip() else "benign"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"OSSGadget completed: {package_name}@{version} ({execution_time:.2f}s)")
            return output

    def process_package(self, category, package_name):
        """Process all versions of a single package."""
        try:
            # Determine paths based on category
            if category == "benign":
                zip_package_path = os.path.join(self.zip_benign_path, package_name)
                unzip_package_path = os.path.join(self.unzip_benign_path, package_name)
            else:
                zip_package_path = os.path.join(self.zip_malware_path, package_name)
                unzip_package_path = os.path.join(self.unzip_malware_path, package_name)

            # Check paths exist
            if not os.path.exists(zip_package_path) or not os.path.exists(unzip_package_path):
                print(f"Warning: Path not found for {package_name}")
                return

            # Get all versions
            versions = os.listdir(zip_package_path)

            for version in versions:
                zip_version_path = os.path.join(zip_package_path, version)
                unzip_version_path = os.path.join(unzip_package_path, version)

                if not os.path.isdir(zip_version_path) or not os.path.isdir(unzip_version_path):
                    continue

                print(f"Processing {category}/{package_name} (version: {version})...")

                # Find archive file
                zip_files = [f for f in os.listdir(zip_version_path) if f.endswith(('.tgz', '.tar.gz', '.zip'))]
                if not zip_files:
                    print(f"Warning: No archive found in {zip_version_path}")
                    continue

                zip_file_path = os.path.join(zip_version_path, zip_files[0])

                # Run tools
                guarddog_result = self.run_guarddog(zip_file_path, package_name, version, category)
                ossgadget_result = self.run_ossgadget(unzip_version_path, package_name, version, category)

                if guarddog_result is None and ossgadget_result is None:
                    self.skipped_count += 1
                else:
                    self.processed_count += 1

                print(f"Completed {category}/{package_name} (version: {version})")

        except Exception as e:
            print(f"Error processing {category}/{package_name}: {str(e)}")

    def process_all_packages(self, num_processes=NUM_PROCESSES):
        """Process all packages using multiprocessing."""
        # Clear timeout logs
        open(self.guarddog_timeout_log, 'w').close()
        open(self.ossgadget_timeout_log, 'w').close()

        # Get all package names
        benign_packages = os.listdir(self.zip_benign_path)
        malware_packages = os.listdir(self.zip_malware_path)

        # Create task list
        tasks = []
        for package in benign_packages:
            tasks.append(("benign", package))
        for package in malware_packages:
            tasks.append(("malware", package))

        print(f"Found {len(benign_packages)} benign and {len(malware_packages)} malware packages")

        # Process with multiprocessing
        if num_processes > 1 and tasks:
            with multiprocessing.Pool(processes=num_processes) as pool:
                pool.starmap(self.process_package, tasks)
        else:
            for task in tasks:
                self.process_package(*task)

        # Summary
        guarddog_timeout_count = sum(1 for _ in open(self.guarddog_timeout_log))
        ossgadget_timeout_count = sum(1 for _ in open(self.ossgadget_timeout_log))

        print(f"\nProcessing complete! Processed: {self.processed_count}, Skipped: {self.skipped_count}")
        print(f"Timeouts - GuardDog: {guarddog_timeout_count}, OSSGadget: {ossgadget_timeout_count}")
        print(f"Timeout logs saved to: {self.timeout_log_dir}")


if __name__ == "__main__":
    # Cleanup zombie processes
    try:
        print("Cleaning up zombie processes...")
        cleanup_cmd = "pkill -f guarddog || true; pkill -f oss-detect-backdoor || true"
        subprocess.call(cleanup_cmd, shell=True)
        print("Cleanup complete")
    except:
        print("Cleanup error, continuing...")

    print(f"Using {NUM_PROCESSES} processes, tool timeout: {TOOL_TIMEOUT}s")

    detector = NPMToolDetector()
    detector.process_all_packages()
