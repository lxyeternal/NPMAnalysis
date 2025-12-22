#!/usr/bin/env python3
"""
Count packages and versions for each detection tool in the Results directory.
Reports dataset coverage statistics for all tools, including common samples.
"""

import os


RESULTS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Experiment/Results"


def get_packages_and_versions(base_path, label):
    """
    Get sets of packages and versions in a directory.
    Returns (package_set, version_set).
    Version format: "package_name/version"
    """
    target_dir = os.path.join(base_path, label)
    if not os.path.exists(target_dir):
        return set(), set()

    packages = set()
    versions = set()

    for package_name in os.listdir(target_dir):
        package_dir = os.path.join(target_dir, package_name)
        if not os.path.isdir(package_dir):
            continue

        packages.add(package_name)
        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            if os.path.isdir(version_dir):
                versions.add(f"{package_name}/{version}")

    return packages, versions


def analyze_tool(tool_name, sub_tool=None):
    """Analyze a single tool's dataset coverage."""
    if sub_tool:
        base_path = os.path.join(RESULTS_DIR, tool_name, sub_tool)
    else:
        base_path = os.path.join(RESULTS_DIR, tool_name)

    benign_pkgs, benign_vers = get_packages_and_versions(base_path, "benign")
    malware_pkgs, malware_vers = get_packages_and_versions(base_path, "malware")

    return {
        "benign_packages": benign_pkgs,
        "benign_versions": benign_vers,
        "malware_packages": malware_pkgs,
        "malware_versions": malware_vers,
        "benign_pkg_count": len(benign_pkgs),
        "benign_ver_count": len(benign_vers),
        "malware_pkg_count": len(malware_pkgs),
        "malware_ver_count": len(malware_vers),
        "total_versions": len(benign_vers) + len(malware_vers)
    }


def main():
    """Main function to count samples for all tools."""
    tools_config = [
        ("GuardDog", "guarddog", None),
        ("OSSGadget", "ossgadget", None),
        ("Genie", "genie", None),
        ("Socket.AI", "socketai", None),
        ("Packj_static", "packj", "result_static"),
        ("Packj_trace", "packj", "result_trace"),
        ("SAP_DT", "sap", "DT"),
        ("SAP_RF", "sap", "RF"),
        ("SAP_XGB", "sap", "XGB"),
        ("MalPacDetector", "MalPacDetector", None),
    ]

    all_results = {}
    for display_name, tool_name, sub_tool in tools_config:
        all_results[display_name] = analyze_tool(tool_name, sub_tool)

    # Print summary table
    print("\n" + "=" * 90)
    print("Dataset Coverage Statistics for Detection Tools")
    print("=" * 90 + "\n")
    print("| Tool | Benign Pkgs | Benign Vers | Malware Pkgs | Malware Vers | Total Vers |")
    print("| ---- | ----------- | ----------- | ------------ | ------------ | ---------- |")

    for tool_name, r in all_results.items():
        print(f"| {tool_name:<15} | {r['benign_pkg_count']:>11} | {r['benign_ver_count']:>11} | "
              f"{r['malware_pkg_count']:>12} | {r['malware_ver_count']:>12} | {r['total_versions']:>10} |")

    # Calculate common packages and versions across all tools
    print("\n" + "=" * 90)
    print("Common Samples Across All Tools")
    print("=" * 90 + "\n")

    # Initialize with first tool's data
    first_result = list(all_results.values())[0]
    common_benign_pkgs = first_result["benign_packages"].copy()
    common_benign_vers = first_result["benign_versions"].copy()
    common_malware_pkgs = first_result["malware_packages"].copy()
    common_malware_vers = first_result["malware_versions"].copy()

    # Intersect with all other tools
    for tool_name, r in all_results.items():
        common_benign_pkgs &= r["benign_packages"]
        common_benign_vers &= r["benign_versions"]
        common_malware_pkgs &= r["malware_packages"]
        common_malware_vers &= r["malware_versions"]

    print(f"Common Benign Packages:  {len(common_benign_pkgs)}")
    print(f"Common Benign Versions:  {len(common_benign_vers)}")
    print(f"Common Malware Packages: {len(common_malware_pkgs)}")
    print(f"Common Malware Versions: {len(common_malware_vers)}")
    print(f"Common Total Versions:   {len(common_benign_vers) + len(common_malware_vers)}")


if __name__ == "__main__":
    main()
