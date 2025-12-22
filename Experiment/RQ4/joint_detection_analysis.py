#!/usr/bin/env python3
"""
RQ4: Joint Detection Analysis
Analyzes joint detection between pairs of tools to identify remaining false negatives.
"""

import json
import os
from pathlib import Path
from itertools import combinations
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the base directory
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # Experiment/RQ4 -> NPMAnalysis

# Input/Output paths
STATS_OUTPUT_DIR = PROJECT_ROOT / "Core" / "ToolDetection" / "DetectionResults"
OUTPUT_DIR = SCRIPT_DIR / "joint_detection"


class JointDetectionAnalyzer:
    def __init__(self, base_dir, output_dir):
        self.base_dir = Path(base_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_false_negatives(self, tool_name):
        """Load false negatives from a specific tool's JSON file."""
        fn_file = self.base_dir / tool_name / "false_negatives.json"
        if not fn_file.exists():
            logger.warning(f"False negatives file not found for tool: {tool_name}")
            return {}

        try:
            with open(fn_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading false negatives for {tool_name}: {e}")
            return {}

    def get_available_tools(self):
        """Get list of available tools (directories with false_negatives.json)."""
        tools = []
        for item in self.base_dir.iterdir():
            if item.is_dir():
                fn_file = item / "false_negatives.json"
                if fn_file.exists():
                    tools.append(item.name)
        return sorted(tools)

    def simulate_joint_detection(self, tool1_name, tool2_name):
        """
        Simulate joint detection between two tools.
        Returns false negatives that remain after joint detection.
        """
        tool1_fn = self.load_false_negatives(tool1_name)
        tool2_fn = self.load_false_negatives(tool2_name)

        if not tool1_fn or not tool2_fn:
            logger.warning(f"Cannot perform joint detection for {tool1_name} and {tool2_name}")
            return {}

        # Find packages that are false negatives in both tools
        # These represent cases where joint detection still fails
        joint_fn = {}

        for package, data in tool1_fn.items():
            if package in tool2_fn:
                # Package is false negative in both tools
                joint_fn[package] = {
                    "prediction": "benign",
                    "actual": "malware",
                    "tool1_prediction": data.get("prediction", "benign"),
                    "tool2_prediction": tool2_fn[package].get("prediction", "benign"),
                    "tools": f"{tool1_name}+{tool2_name}"
                }

        return joint_fn

    def calculate_statistics(self, tool1_name, tool2_name, tool1_fn, tool2_fn, joint_fn):
        """Calculate statistics for joint detection analysis."""
        tool1_fn_count = len(tool1_fn)
        tool2_fn_count = len(tool2_fn)
        joint_fn_count = len(joint_fn)

        # Calculate improvement
        improvement_over_tool1 = tool1_fn_count - joint_fn_count
        improvement_over_tool2 = tool2_fn_count - joint_fn_count

        improvement_rate_tool1 = (improvement_over_tool1 / tool1_fn_count * 100) if tool1_fn_count > 0 else 0
        improvement_rate_tool2 = (improvement_over_tool2 / tool2_fn_count * 100) if tool2_fn_count > 0 else 0

        return {
            "tool1_name": tool1_name,
            "tool2_name": tool2_name,
            "tool1_false_negatives": tool1_fn_count,
            "tool2_false_negatives": tool2_fn_count,
            "joint_false_negatives": joint_fn_count,
            "improvement_over_tool1": improvement_over_tool1,
            "improvement_over_tool2": improvement_over_tool2,
            "improvement_rate_tool1_percent": round(improvement_rate_tool1, 2),
            "improvement_rate_tool2_percent": round(improvement_rate_tool2, 2),
            "packages_detected_by_tool2_only": tool1_fn_count - joint_fn_count,
            "packages_detected_by_tool1_only": tool2_fn_count - joint_fn_count
        }

    def save_results(self, tool1_name, tool2_name, joint_fn, statistics):
        """Save joint detection results and statistics."""
        # Create output filename
        output_filename = f"{tool1_name}_and_{tool2_name}_joint_detection.json"
        output_path = self.output_dir / output_filename

        # Prepare complete output
        output_data = {
            "metadata": {
                "analysis_type": "joint_detection",
                "primary_tool": tool1_name,
                "secondary_tool": tool2_name,
                "description": f"False negatives remaining after joint detection with {tool1_name} and {tool2_name}"
            },
            "statistics": statistics,
            "remaining_false_negatives": joint_fn
        }

        # Save to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved joint detection results to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving results for {tool1_name} and {tool2_name}: {e}")

    def analyze_all_combinations(self):
        """Analyze all possible tool combinations."""
        tools = self.get_available_tools()
        logger.info(f"Found {len(tools)} tools: {tools}")

        if len(tools) < 2:
            logger.error("Need at least 2 tools for joint detection analysis")
            return

        # Analyze all pairs
        combination_count = 0
        summary_stats = []

        for tool1, tool2 in combinations(tools, 2):
            logger.info(f"Analyzing joint detection: {tool1} + {tool2}")

            # Load false negatives
            tool1_fn = self.load_false_negatives(tool1)
            tool2_fn = self.load_false_negatives(tool2)

            if not tool1_fn or not tool2_fn:
                continue

            # Simulate joint detection
            joint_fn = self.simulate_joint_detection(tool1, tool2)

            # Calculate statistics
            stats = self.calculate_statistics(tool1, tool2, tool1_fn, tool2_fn, joint_fn)
            summary_stats.append(stats)

            # Save results
            self.save_results(tool1, tool2, joint_fn, stats)

            combination_count += 1

        # Save summary statistics
        self.save_summary_statistics(summary_stats)

        logger.info(f"Completed analysis for {combination_count} tool combinations")

    def save_summary_statistics(self, summary_stats):
        """Save overall summary statistics."""
        summary_path = self.output_dir / "joint_detection_summary.json"

        summary_data = {
            "metadata": {
                "analysis_type": "joint_detection_summary",
                "total_combinations": len(summary_stats),
                "description": "Summary of all joint detection analyses"
            },
            "combinations": summary_stats
        }

        # Add rankings
        if summary_stats:
            # Sort by improvement rate over tool1
            summary_data["best_combinations_by_improvement"] = sorted(
                summary_stats,
                key=lambda x: x["improvement_rate_tool1_percent"],
                reverse=True
            )[:10]

        try:
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved summary statistics to: {summary_path}")
        except Exception as e:
            logger.error(f"Error saving summary statistics: {e}")


def main():
    print(f"Stats output dir: {STATS_OUTPUT_DIR}")
    print(f"Output dir: {OUTPUT_DIR}")

    # Create analyzer and run analysis
    analyzer = JointDetectionAnalyzer(STATS_OUTPUT_DIR, OUTPUT_DIR)
    analyzer.analyze_all_combinations()

    print(f"\nJoint detection analysis completed. Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
