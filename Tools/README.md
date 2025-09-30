# NPM Analysis Tools

This document provides detailed information about the tools used for NPM package analysis, including their execution logic, usage instructions, and output locations.

## Dataset Structure

The dataset includes **6,547 malicious packages** and **7,024 benign packages**, organized in the following directory structure:

```
Dataset/
├── zip_benign/       # Compressed benign packages
│   ├── [package_name]/
│   │   └── [version]/
│   │       └── [package.tgz]
├── zip_malware/      # Compressed malicious packages
│   ├── [package_name]/
│   │   └── [version]/
│   │       └── [package.tgz]
├── unzip_benign/     # Extracted benign packages
│   ├── [package_name]/
│   │   └── [version]/
│   │       └── [extracted files]
└── unzip_malware/    # Extracted malicious packages
    ├── [package_name]/
    │   └── [version]/
    │       └── [extracted files]
```

**Important Notes:**
- Each compressed package in the `zip_*` directories has a corresponding extracted version in the `unzip_*` directories
- The `malware` and `benign` labels represent the ground truth classification of the packages
- Some analysis tools operate on compressed packages while others require extracted files

## Output Structure

All tool outputs are stored in the following directory structure:

```
Codes/tool_detect/tool_output/
├── [tool_name]/
│   ├── benign/
│   │   └── [package_name]/
│   │       └── [version]/
│   │           └── [output_file]
│   └── malware/
│       └── [package_name]/
│           └── [version]/
│               └── [output_file]
```

### Example Paths:

- Genie tool output:
  ```
  Codes/tool_detect/tool_output/genie/benign/@0xelod##smart-order-router/3.25.4-theta/@0xelod##smart-order-router-3.25.4-theta.csv
  ```

- GuardDog tool output:
  ```
  Codes/tool_detect/tool_output/guarddog/malware/@0x000000000000000##util/0.1.0/result.txt
  ```

## Tools Documentation

### GENIE

**Description:**
GENIE (Generic Inspection Engine) is a CodeQL-based static analysis tool that detects potentially malicious patterns in JavaScript/TypeScript code. It performs static code analysis (without executing the code) to identify suspicious behavior, categorized as a Static-Based tool.

**Execution Logic:**
1. Copies package source code to a temporary directory
2. Creates a CodeQL database for code analysis
3. Runs predefined malware detection queries
4. Optionally runs obfuscation detection queries
5. Generates CSV reports with findings

**Usage:**
```bash
cd Tools/GENIE
python batch_analysis.py
```

**Configuration:**
The tool can be configured by editing the parameters at the top of the `batch_analysis.py` file:
```python
# Process count for parallel execution
PROCESS_COUNT = 24
# Analysis mode: "INDIVIDUAL" (each query separately) or "BATCH" (all queries at once)
SCAN_MODE = "BATCH"
# Enable/disable obfuscation detection
USE_OBFUSCATOR_QUERIES = True
```

**Input:**
- Operates on extracted package directories from `Dataset/unzip_benign/` or `Dataset/unzip_malware/`

**Output:**
- Location: `Codes/tool_detect/tool_output/genie/[benign|malware]/[package_name]/[version]/[package_name]-[version].csv`
- Format: CSV file containing detected malicious patterns and obfuscation techniques

### Guarddog

**Description:**
GuardDog is a rule-based security tool that uses Semgrep to perform static analysis on package code and metadata to detect potentially malicious patterns. It is categorized as a Static-Based tool.

**Execution Logic:**
1. Parses and analyzes the package source code
2. Applies predefined Semgrep rules to detect suspicious patterns
3. Examines package metadata for security concerns
4. Generates a report of identified security issues

**Usage (from code):**
```bash
guarddog npm scan [package_path]
```

**Input:**
- Operates on compressed package files (zip) from `Dataset/zip_benign/` or `Dataset/zip_malware/`

**Output:**
- Location: `Codes/tool_detect/tool_output/guarddog/[benign|malware]/[package_name]/[version]/result.txt`
- Format: Text file containing detected suspicious code patterns or "benign" if no issues found

### OSSGadget

**Description:**
OSSGadget is a collection of tools for analyzing open source software packages, with oss-detect-backdoor focusing on identifying potential backdoors.

**Execution Logic:**
1. Analyzes the extracted package files
2. Searches for suspicious code patterns
3. Identifies potential backdoors or malicious code

**Usage (from code):**
```bash
Tools/OSSGadget/oss-detect-backdoor [unzip_dir_path]
```

**Input:**
- Operates on extracted package directories from `Dataset/unzip_benign/` or `Dataset/unzip_malware/`

**Output:**
- Location: `Codes/tool_detect/tool_output/ossgadget/[benign|malware]/[package_name]/[version]/result.txt`
- Format: Text file containing detection results or "benign" if no issues found

### MalPacDetector

**Description:**
MalPacDetector is a machine learning-based malware detection tool that uses three different classification models (MLP, Naive Bayes, SVM) to identify malicious NPM packages. It extracts features from package source code and metadata to train and predict malware classification.

**Detection Principle:**
1. Feature extraction from package files and metadata
2. Uses three ML models: Multi-Layer Perceptron (MLP), Naive Bayes (NB), and Support Vector Machine (SVM)
3. Each model provides independent predictions for ensemble-based detection
4. Generates feature vectors and model predictions for comprehensive analysis

**Usage:**
```bash
cd Tools/MalPacDetector
python custom_detector.py
```

**Input:**
- Operates on extracted package directories from `Dataset/unzip_benign/` or `Dataset/unzip_malware/`

**Output:**
- Location: `Codes/tool_detect/tool_output/MalPacDetector/[benign|malware]/[package_name]/[version]/`
- Format: Contains extracted features and prediction results from all three models (MLP, NB, SVM)

### SAP (Static Analysis for Packages)

**Description:**
SAP is a static analysis tool that extracts comprehensive features from NPM packages and uses machine learning models (Decision Tree, Random Forest, XGBoost) for malware detection. It focuses on code structure, dependencies, and metadata analysis.

**Detection Principle:**
1. Feature extraction using `npm_feature_extractor.py` to analyze package structure, dependencies, and code patterns
2. Three-model ensemble: Decision Tree (DT), Random Forest (RF), and XGBoost (XGB)
3. Static analysis of JavaScript code, package.json metadata, and file structure
4. Generates feature vectors for machine learning classification

**Usage:**
```bash
# Feature extraction
cd Tools/sap/scripts/feature_extraction
python npm_feature_extractor.py

# Prediction using trained models
cd Tools/sap/scripts
python sap_prediction.py
```

**Input:**
- Operates on extracted package directories from `Dataset/unzip_benign/` or `Dataset/unzip_malware/`

**Output:**
- Feature files: `Tools/sap/scripts/feature_extraction/benign_npm_feature_extracted.csv` and `malware_npm_feature_extracted.csv`
- Detection results: `Tools/sap/scripts/sap_detection_results.csv`

### SecurityAI (LLM-based Analysis)

**Description:**
SecurityAI leverages Large Language Models (specifically GPT-4 variants) to detect malicious behavior in NPM packages through code analysis. It implements a multi-step analysis process with different temperature parameters for comprehensive malware detection.

**Detection Principle:**
1. Uses two GPT-4 model variants: gpt-4.1-mini (stronger) and gpt-4.1-nano (standard)
2. Multi-step analysis with varying temperature parameters (1.0, 0.75, 0.5) for different analysis phases
3. Generates multiple analysis reports per package (3-5 reports depending on model)
4. Analyzes JavaScript code for malicious patterns, obfuscation, and suspicious behavior
5. Provides detailed reasoning and malicious behavior scoring

**Usage:**
```bash
cd Tools/SecurityAI
python run_dataset_analysis.py
# or for multiprocess analysis
python run_multiprocess.py
```

**Configuration:**
- API key and model settings in `Tools/SecurityAI/config.py`
- Supports both single-process and multi-process analysis modes

**Input:**
- Operates on extracted package directories from `Dataset/unzip_benign/` or `Dataset/unzip_malware/`
- Analyzes JavaScript files up to 175KB in size, maximum 20 JS files per package

**Output:**
- Location: `Codes/tool_detect/tool_output/socketai/[benign|malware]/[package_name]/[version]/`
- Format: Individual LLM analysis results for each file plus summary reports

### Packj

**Description:**
Packj is a comprehensive security analysis tool that provides both static and dynamic analysis capabilities for NPM packages. It combines code analysis, metadata examination, and runtime behavior monitoring to detect malicious activities in packages.

**Detection Principle:**
1. **Static Analysis Mode**: Analyzes package source code, dependencies, and metadata without execution
2. **Dynamic Analysis Mode**: Executes package code in a controlled environment to monitor runtime behavior
3. Examines package.json metadata, file permissions, and dependency chains
4. Detects suspicious API calls, network communications, and file system operations
5. Provides risk scoring based on multiple security indicators

**Usage:**
```bash
cd Tools/packj
# The tool supports both static and dynamic analysis modes
# Specific usage depends on the analysis configuration
```

**Input:**
- Operates on extracted package directories from `Dataset/unzip_benign/` or `Dataset/unzip_malware/`

**Output:**
- Location: `Codes/tool_detect/tool_output/packj/result_trace/[benign|malware]/[package_name]/[version]/`
- Format: Analysis results containing both static and dynamic findings with risk assessments

## Running Multiple Tools

The analysis framework supports running multiple detection tools through the main detection script:

```bash
cd Codes/tool_detect
python tool_detect.py
```

This will execute GuardDog and OSSGadget tools on all packages in the dataset using multiprocess parallel execution.

## Tool Categories

The tools can be categorized by their detection approaches:

**Static Analysis Tools:**
- GENIE: CodeQL-based static analysis
- GuardDog: Rule-based static analysis using Semgrep
- OSSGadget: Static code pattern analysis
- MalPacDetector: ML-based static feature analysis
- SAP: Static code and metadata analysis

**Dynamic Analysis Tools:**
- Packj: Combined static and dynamic analysis with runtime monitoring

**AI-based Analysis Tools:**
- SecurityAI: Large Language Model-based code analysis

## Timeout Handling

Tools are configured with a timeout limit (default: 300 seconds) to prevent hanging on problematic packages. If a tool execution exceeds this limit:

1. The process is terminated
2. "TIMEOUT" is written to the output file
3. The package information is logged in a timeout log file for later reference