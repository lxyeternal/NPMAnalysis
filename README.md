# NPM Malware Detection Benchmark

A large-scale empirical study evaluating NPM malware detection tools across multiple dimensions: detection effectiveness, behavioral analysis, temporal robustness, and tool complementarity.

## Overview

This project provides the first comprehensive benchmark for NPM malicious package detection tools. We curate a dataset of **6,420 malicious packages** and **7,288 benign packages**, define a fine-grained taxonomy of **11 malicious behavior categories** and **14 evasion technique categories**, and systematically evaluate **8 detection tools** (13 tool variants) across four research questions.

## Project Structure

```
NPMAnalysis/
├── Core/                                  # Core analysis infrastructure
│   ├── Analysis/                          # Behavior and code analysis
│   │   ├── behavior/                      # Malicious behavior taxonomy & classification
│   │   └── code_snipptes/                 # Malicious code pattern extraction & validation
│   ├── Data/                              # Data management pipeline
│   │   ├── collection/                    # Package downloading & extraction
│   │   ├── cleaning/                      # Dataset cleaning & validation
│   │   └── timecollect/                   # Package timestamp collection
│   └── ToolDetection/                     # Detection tool execution framework
│       └── DetectionResults/              # Raw detection outputs from each tool
│
├── Experiment/                            # Research experiments
│   ├── RQ1/                               # Overall accuracy evaluation
│   │   ├── accuracy_npm.py                # Precision, recall, F1 measurement
│   │   ├── false_negative/                # False negative analysis
│   │   └── false_positive/                # False positive analysis
│   ├── RQ2/                               # Behavior & evasion detection analysis
│   │   ├── code/                          # Heatmap, arc plot, distribution scripts
│   │   └── statistic/                     # Figures and result data
│   ├── RQ3/                               # Temporal evolution analysis
│   │   ├── code/                          # Trend analysis scripts
│   │   └── statistic/                     # Time series results and figures
│   ├── RQ4/                               # Tool complementarity analysis
│   │   ├── code/                          # Multi-tool combination analysis
│   │   └── statistic/                     # Combination results and figures
│   └── Results/                           # Aggregated experiment results
│
├── Tools/                                 # Detection tool implementations
│   ├── GENIE/                             # CodeQL-based taint-tracking analysis
│   ├── guarddog/                          # Semgrep rule-based detection
│   ├── MalPacDetector/                    # ML-based detection (MLP, NB, SVM)
│   ├── MalTracker/                        # Malware tracking tool
│   ├── OSSGadget/                         # Pattern-based backdoor detection
│   ├── packj/                             # Hybrid static + dynamic analysis
│   ├── sap/                               # Static Analysis for Packages (DT, RF, XGB)
│   └── SecurityAI/                        # LLM-based semantic analysis
│
├── Dataset/                               # Malware and benign package samples
│   ├── raw_dataset/                       # Source datasets (BKC, DONAPI, GuardDog, etc.)
│   ├── zip_malware/                       # Compressed malicious packages
│   ├── zip_benign/                        # Compressed benign packages
│   ├── unzip_malware/                     # Extracted malicious packages
│   └── unzip_benign/                      # Extracted benign packages
│
├── Resource/                              # Analysis resources
│   └── Prompts/                           # LLM analysis prompt templates
│
├── Utils/                                 # Shared utilities
│   └── llm_client.py                      # LLM API client (Azure, OpenAI, Ollama)
│
└── Configs/                               # Configuration files
    └── llm_config_template.json           # LLM API config template
```

## Research Questions

### RQ1: Overall Accuracy
**How accurate are detection tools at identifying malicious NPM packages?**

Evaluates precision, recall, F1-score, and accuracy of all 13 tool variants. Analyzes false positives and false negatives to understand each tool's strengths and limitations.

### RQ2: Behavioral Detection & Evasion Resistance
**How effective are detection tools against different malicious behaviors and evasion techniques?**

Maps detection rates across 11 malicious behavior categories (e.g., Command Execution, Data Exfiltration, C2 Communication) and 14 evasion techniques (e.g., String Obfuscation, Encoding Obfuscation, Hook Abuse). Generates heatmaps and co-occurrence analysis to reveal detection blind spots.

### RQ3: Temporal Robustness
**How do detection rates change as attack techniques evolve over time?**

Tracks detection performance across time periods (2011--2025) to assess tool robustness against evolving threats. Reveals that ML-based tools suffer significant degradation (e.g., SAP-DT drops 48.87% from 2021 to 2023), while behavioral monitoring tools maintain >97% stability.

### RQ4: Tool Complementarity
**Can combining multiple tools improve detection coverage?**

Evaluates 156 pairwise tool combinations using union (OR) and intersection (AND) strategies. Identifies optimal combinations for different deployment goals (coverage vs. precision).

## Detection Tools Evaluated

| Tool | Category | Approach |
|------|----------|----------|
| **GENIE** | Static Analysis | CodeQL taint-tracking queries |
| **GuardDog** | Static Analysis | Semgrep rule-based pattern matching |
| **OSSGadget** | Static Analysis | Pattern-based backdoor detection |
| **Socket.AI** | LLM-based | GPT-4 semantic code analysis |
| **SAP (DT/RF/XGB)** | ML-based | Feature extraction + Decision Tree / Random Forest / XGBoost |
| **Packj (Static/Trace)** | Hybrid | Static behavior analysis + strace-based dynamic monitoring |
| **MalPacDetector** | ML-based | MLP, Naive Bayes, SVM ensemble |
| **Cerebro** | ML-based | Graph neural network on package dependencies |

## Malicious Behavior Taxonomy

| Category | Description |
|----------|-------------|
| Command Execution | Executing system commands or spawning child processes |
| Data Exfiltration | Sending collected data to external servers |
| Data Collection | Gathering sensitive system/user information |
| C2 Communication | Establishing command-and-control channels |
| Malicious Download | Downloading and executing remote payloads |
| Persistence | Maintaining access across reboots or sessions |
| Credential Theft | Stealing passwords, tokens, or API keys |
| Dynamic Code Execution | Using eval/Function to execute runtime-generated code |
| File Manipulation | Unauthorized file read/write/delete operations |
| Reverse Shell | Opening remote shell access to the system |
| Web Injection | Injecting malicious scripts into web content |

## Setup

### Requirements

- Python 3.8+
- Dependencies: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`

### Configuration

1. Copy the config template:
   ```bash
   cp Configs/llm_config_template.json Configs/llm_config.json
   ```
2. Fill in your API keys (Azure OpenAI / OpenAI / Ollama) in `llm_config.json`.

## Usage

### Data Pipeline

```bash
# Download and extract packages
python Core/Data/collection/package_download.py
python Core/Data/collection/unzip_npm_packages.py

# Collect package timestamps
python Core/Data/timecollect/collect_timestamps.py
```

### Run Detection Tools

```bash
# Execute all detection tools on the dataset
python Core/ToolDetection/tool_detect.py

# Generate detection result summaries
python Core/ToolDetection/generate_detection_results.py
```

### Behavior Analysis

```bash
# Extract and classify malicious code snippets
python Core/Analysis/code_snipptes/extract_snippets.py

# Build behavior taxonomy
python Core/Analysis/behavior/behavior_taxonomy_experiment.py
```

### Experiments

```bash
# RQ1: Overall accuracy evaluation
python Experiment/RQ1/accuracy_npm.py

# RQ2: Behavior detection heatmaps and evasion analysis
python Experiment/RQ2/code/detection_rate_heatmap.py
python Experiment/RQ2/code/evasion_detection_heatmap.py
python Experiment/RQ2/code/evasion_combination_arc.py

# RQ3: Temporal trend analysis
python Experiment/RQ3/code/detection_rate_over_time.py

# RQ4: Tool complementarity analysis
python Experiment/RQ4/code/multi_tool_fusion.py
```

## License

MIT License
