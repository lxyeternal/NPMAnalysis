#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GuardDog Pattern Extractor

Extract and analyze malicious code patterns from GuardDog detection reports.
This script processes GuardDog output files and generates statistics about
common malicious code patterns found in NPM packages.

Output:
    - malware_pattern_stats.json: Complete statistics report
    - malware_pattern_summary.txt: Human-readable summary
    - malware_code_{type}.json: Code snippets grouped by malware type
    - npm_install_script_stats.json: NPM install script statistics
"""

import os
import re
import json
import hashlib
import logging
from pathlib import Path
from collections import defaultdict
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Configuration
# =============================================================================

# Get the script directory for relative path resolution
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parents[2]  # Core/Analysis/behavior -> NPMAnalysis root

# Default paths (can be overridden)
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "Experiment" / "Results" / "guarddog" / "malware"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "results" / "guarddog_patterns"


# =============================================================================
# Core Functions
# =============================================================================

def extract_malicious_code_from_report(
    report_content: str,
    package_name: str,
    package_version: str,
    report_file_path: str
) -> list[dict]:
    """
    Extract all malicious code snippets from a GuardDog report.

    Args:
        report_content: The text content of the GuardDog report
        package_name: Name of the NPM package
        package_version: Version of the package
        report_file_path: Path to the report file

    Returns:
        List of dictionaries containing code snippet information
    """
    lines = report_content.split('\n')
    code_snippets = []

    # Extract archive path from report header
    archive_pattern = r'Found \d+ potentially malicious indicators in (.*?)(\.tar\.gz|\.zip|\.whl)'
    archive_match = re.search(archive_pattern, report_content)
    archive_path = ""
    if archive_match:
        archive_path = archive_match.group(1) + archive_match.group(2)

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Match file location lines: "* ... at package-name/file.py:21"
        location_match = re.search(
            r'\*.*?\s+at\s+([\w\-\.\/]+\.[a-zA-Z0-9]+):(\d+)',
            line
        )

        if location_match:
            relative_path = location_match.group(1)
            line_number = location_match.group(2)

            # Look for malware type in previous lines
            malware_type = ""
            for j in range(max(0, i - 5), i):
                type_match = re.match(
                    r'^([\w\-]+): found \d+ .* matches',
                    lines[j].strip()
                )
                if type_match:
                    malware_type = type_match.group(1)
                    break

            # Extract code snippet (collect following lines)
            code_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # Stop at empty line, new indicator (*), or new type section
                if (not next_line or
                    next_line.startswith('*') or
                    re.match(r'^[\w\-]+: found \d+ .* matches', next_line)):
                    break
                # Remove leading whitespace
                code_line = re.sub(r'^\s+', '', next_line)
                code_lines.append(code_line)
                j += 1

            code_snippet = '\n'.join(code_lines)

            if code_snippet.strip():
                # Build source code path
                unzip_path = ""
                archive_name = ""
                if archive_path:
                    unzip_path = (archive_path
                                  .replace('zip_malware', 'unzip_malware')
                                  .replace('.tar.gz', '')
                                  .replace('.zip', '')
                                  .replace('.whl', ''))
                    archive_name = os.path.basename(unzip_path)

                source_code_path = (
                    os.path.join(unzip_path, relative_path) if unzip_path else ""
                )

                snippet_info = {
                    'package': package_name,
                    'version': package_version,
                    'path': relative_path,
                    'line': line_number,
                    'type': malware_type,
                    'code': code_snippet,
                    'description': line,
                    'full_path': source_code_path,
                    'report_file': report_file_path,
                    'archive_path': archive_path,
                    'archive_name': archive_name
                }
                code_snippets.append(snippet_info)

            i = j
            continue

        i += 1

    return code_snippets


def extract_npm_install_script_types(report_content: str) -> Optional[dict]:
    """
    Extract NPM install script types from a GuardDog report.

    Args:
        report_content: The text content of the GuardDog report

    Returns:
        Dictionary with script type counts, or None if no install scripts found
    """
    script_types = {
        'postinstall': 0,
        'preinstall': 0,
        'install': 0,
        'other': 0
    }

    if 'npm-install-script' not in report_content:
        return None

    patterns = {
        'postinstall': r'"postinstall"\s*:\s*"([^"]+)"',
        'preinstall': r'"preinstall"\s*:\s*"([^"]+)"',
        'install': r'"install"\s*:\s*"([^"]+)"'
    }

    for script_type, pattern in patterns.items():
        if re.search(pattern, report_content):
            script_types[script_type] += 1

    # If npm-install-script present but no known type matched
    if sum(script_types.values()) == 0:
        script_types['other'] += 1

    return script_types


def is_benign_report(report_content: str) -> bool:
    """Check if the report indicates no malicious code found."""
    return (
        "Found 0 potentially malicious indicators" in report_content or
        "benign" in report_content.lower()
    )


def normalize_code(code_snippet: str) -> str:
    """Normalize code snippet for comparison (remove whitespace, lowercase)."""
    normalized = re.sub(r'\s+', '', code_snippet)
    return normalized.lower()


def hash_code(code_snippet: str) -> str:
    """Generate MD5 hash of normalized code snippet."""
    normalized = normalize_code(code_snippet)
    return hashlib.md5(normalized.encode()).hexdigest()


# =============================================================================
# Report Generation
# =============================================================================

def generate_summary_report(report: dict, output_dir: Path) -> None:
    """Generate human-readable summary report."""
    summary_path = output_dir / "malware_pattern_summary.txt"

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("Malicious Code Pattern Statistics Report\n")
        f.write("=" * 40 + "\n\n")

        # Summary statistics
        summary = report['summary']
        f.write(f"Total package versions analyzed: {summary['total_package_versions']}\n")
        f.write(f"Malicious package versions: {summary['malicious_package_versions']}\n")
        f.write(f"Benign package versions: {summary['benign_package_versions']}\n")
        f.write(f"Unique code patterns: {summary['unique_code_patterns']}\n\n")

        # NPM install script statistics
        npm_stats = report['npm_install_script_stats']
        f.write("NPM Install Script Statistics\n")
        f.write("-" * 30 + "\n\n")
        f.write(f"Total: {npm_stats['total']} package versions\n")
        f.write(f"  - postinstall: {npm_stats['postinstall']}\n")
        f.write(f"  - preinstall: {npm_stats['preinstall']}\n")
        f.write(f"  - install: {npm_stats['install']}\n")
        f.write(f"  - other: {npm_stats['other']}\n\n")

        # Top 10 most common patterns
        f.write("Top 10 Most Common Malicious Patterns\n")
        f.write("-" * 40 + "\n\n")

        for i, pattern in enumerate(report["pattern_frequency"][:10], 1):
            f.write(f"{i}. Count: {pattern['count']} packages (Type: {pattern['type']})\n")
            f.write("   Code:\n")
            for line in pattern['example_code'].split('\n'):
                f.write(f"      {line}\n")
            f.write(f"   Hash: {pattern['hash']}\n")
            packages_preview = pattern['package_versions'][:5]
            more = '...' if len(pattern['package_versions']) > 5 else ''
            f.write(f"   Packages: {', '.join(packages_preview)}{more}\n\n")

    logger.info(f"Summary report saved to {summary_path}")


def save_code_snippets_by_type(
    all_snippets: list[dict],
    output_dir: Path
) -> None:
    """Save code snippets grouped by malware type."""
    code_by_type = defaultdict(list)
    for snippet in all_snippets:
        type_name = snippet['type'] or 'unknown'
        code_by_type[type_name].append(snippet)

    for type_name, snippets in code_by_type.items():
        # Sanitize filename
        safe_name = re.sub(r'[^\w\-]', '_', type_name)
        output_path = output_dir / f"malware_code_{safe_name}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(snippets, f, ensure_ascii=False, indent=2)
        logger.info(f"Saved {len(snippets)} snippets to {output_path.name}")


# =============================================================================
# Main Processing
# =============================================================================

class GuardDogPatternExtractor:
    """Extract and analyze malicious code patterns from GuardDog reports."""

    def __init__(self, source_dir: Path, output_dir: Path):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Statistics
        self.code_pattern_count = defaultdict(list)
        self.package_version_code_map = defaultdict(lambda: defaultdict(list))
        self.all_code_snippets = []

        self.malicious_count = 0
        self.benign_count = 0
        self.total_count = 0

        # NPM install script stats
        self.npm_script_stats = {
            'postinstall': 0,
            'preinstall': 0,
            'install': 0,
            'other': 0
        }
        self.npm_script_packages = {
            'postinstall': [],
            'preinstall': [],
            'install': [],
            'other': []
        }

    def process_all_packages(self) -> dict:
        """Process all packages and generate statistics report."""
        if not self.source_dir.exists():
            logger.error(f"Source directory not found: {self.source_dir}")
            return {}

        # Iterate through package directories
        for package_dir in self.source_dir.iterdir():
            if not package_dir.is_dir():
                continue

            package_name = package_dir.name

            # Iterate through version directories
            for version_dir in package_dir.iterdir():
                if not version_dir.is_dir():
                    continue

                version = version_dir.name
                self._process_package_version(package_name, version, version_dir)

        # Generate and save report
        report = self._build_report()
        self._save_report(report)

        return report

    def _process_package_version(
        self,
        package_name: str,
        version: str,
        version_dir: Path
    ) -> None:
        """Process a single package version."""
        # Find report file
        txt_files = list(version_dir.glob("*.txt"))
        if not txt_files:
            return

        report_path = txt_files[0]
        package_key = f"{package_name}@{version}"
        self.total_count += 1

        try:
            report_content = report_path.read_text(encoding='utf-8', errors='ignore')

            # Check if benign
            if is_benign_report(report_content):
                logger.debug(f"{package_key}: No malicious code found")
                self.benign_count += 1
                return

            # Extract NPM install script types
            npm_scripts = extract_npm_install_script_types(report_content)
            if npm_scripts:
                for script_type, count in npm_scripts.items():
                    if count > 0:
                        self.npm_script_stats[script_type] += count
                        self.npm_script_packages[script_type].append(package_key)

            # Extract code snippets
            snippets = extract_malicious_code_from_report(
                report_content,
                package_name,
                version,
                str(report_path)
            )

            if not snippets:
                logger.debug(f"{package_key}: No code snippets extracted")
                return

            self.malicious_count += 1
            self.all_code_snippets.extend(snippets)

            # Process each snippet
            for snippet in snippets:
                code = snippet['code']
                if not code.strip():
                    continue

                code_hash = hash_code(code)
                pkg_version_tuple = (package_name, version)

                if pkg_version_tuple not in self.code_pattern_count[code_hash]:
                    self.code_pattern_count[code_hash].append(pkg_version_tuple)

                self.package_version_code_map[package_name][version].append({
                    'hash': code_hash,
                    'code': code,
                    'path': f"{snippet['path']}:{snippet['line']}",
                    'type': snippet['type'],
                    'report_file': snippet['report_file'],
                    'full_path': snippet['full_path'],
                    'archive_path': snippet['archive_path']
                })

            logger.info(f"{package_key}: Extracted {len(snippets)} code snippets")

        except Exception as e:
            logger.error(f"Error processing {package_key}: {e}")

    def _build_report(self) -> dict:
        """Build the complete statistics report."""
        # Sort patterns by frequency
        pattern_frequency = [
            (h, len(pkgs), pkgs)
            for h, pkgs in self.code_pattern_count.items()
        ]
        pattern_frequency.sort(key=lambda x: x[1], reverse=True)

        report = {
            "summary": {
                "total_package_versions": self.total_count,
                "malicious_package_versions": self.malicious_count,
                "benign_package_versions": self.benign_count,
                "unique_code_patterns": len(self.code_pattern_count)
            },
            "npm_install_script_stats": {
                **self.npm_script_stats,
                "total": sum(self.npm_script_stats.values()),
                "packages": self.npm_script_packages
            },
            "pattern_frequency": [],
            "pattern_details": {},
            "all_code_snippets": []
        }

        # Add pattern frequency data
        for code_hash, count, package_versions in pattern_frequency:
            example = self._find_example_for_hash(code_hash, package_versions)
            formatted_packages = [f"{pkg}@{ver}" for pkg, ver in package_versions]

            report["pattern_frequency"].append({
                "hash": code_hash,
                "count": count,
                "package_versions": formatted_packages,
                **example
            })

        # Add pattern details per package
        for pkg_name, versions in self.package_version_code_map.items():
            report["pattern_details"][pkg_name] = {}
            for ver, code_list in versions.items():
                report["pattern_details"][pkg_name][ver] = [
                    {
                        **item,
                        "shared_with": len(self.code_pattern_count[item['hash']])
                    }
                    for item in code_list
                ]

        # Add all code snippets
        report["all_code_snippets"] = [
            {
                **snippet,
                "hash": hash_code(snippet['code'])
            }
            for snippet in self.all_code_snippets
        ]

        return report

    def _find_example_for_hash(
        self,
        code_hash: str,
        package_versions: list
    ) -> dict:
        """Find an example code snippet for a given hash."""
        for pkg_name, ver in package_versions:
            for item in self.package_version_code_map[pkg_name][ver]:
                if item['hash'] == code_hash:
                    return {
                        "example_code": item['code'],
                        "type": item['type'],
                        "example_report_file": item['report_file'],
                        "example_full_path": item['full_path'],
                        "example_archive_path": item['archive_path']
                    }
        return {
            "example_code": "",
            "type": "",
            "example_report_file": "",
            "example_full_path": "",
            "example_archive_path": ""
        }

    def _save_report(self, report: dict) -> None:
        """Save all report files."""
        # Main JSON report
        main_report_path = self.output_dir / "malware_pattern_stats.json"
        with open(main_report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logger.info(f"Main report saved to {main_report_path}")

        # Human-readable summary
        generate_summary_report(report, self.output_dir)

        # Code snippets by type
        save_code_snippets_by_type(self.all_code_snippets, self.output_dir)

        # NPM install script stats
        npm_stats_path = self.output_dir / "npm_install_script_stats.json"
        with open(npm_stats_path, 'w', encoding='utf-8') as f:
            json.dump(report["npm_install_script_stats"], f, ensure_ascii=False, indent=2)
        logger.info(f"NPM script stats saved to {npm_stats_path}")

    def print_summary(self) -> None:
        """Print summary statistics to console."""
        print(f"\n{'=' * 50}")
        print("GuardDog Pattern Extraction Complete")
        print('=' * 50)
        print(f"Total packages analyzed: {self.total_count}")
        print(f"Malicious packages: {self.malicious_count}")
        print(f"Benign packages: {self.benign_count}")
        print(f"Unique code patterns: {len(self.code_pattern_count)}")
        print(f"\nNPM Install Script Statistics:")
        print(f"  Total: {sum(self.npm_script_stats.values())}")
        for script_type, count in self.npm_script_stats.items():
            print(f"  - {script_type}: {count}")
        print(f"\nResults saved to: {self.output_dir}")


# =============================================================================
# Entry Point
# =============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract malicious code patterns from GuardDog reports"
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Directory containing GuardDog output"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for results"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info(f"Source directory: {args.source}")
    logger.info(f"Output directory: {args.output}")

    extractor = GuardDogPatternExtractor(args.source, args.output)
    extractor.process_all_packages()
    extractor.print_summary()


if __name__ == "__main__":
    main()
