# RQ2: Malicious Behavior Detection and Evasion Technique Analysis

## Overview

This document provides a comprehensive analysis of malicious behavior detection capabilities across different security tools, evasion technique effectiveness, and attack vector distribution in malicious NPM packages.

**Dataset Statistics:**
- Total package versions analyzed: 7,785
- Malicious package versions: 5,642
- Benign package versions: 1,927
- Unique malicious code patterns: 2,956

---

## RQ2.1: How Effective Are Detection Tools at Identifying Different Malicious Behaviors?

### 2.1.1 Malicious Behavior Categories

We classified malicious behaviors into 15 categories based on their attack objectives:

| Category | Description |
|----------|-------------|
| **Persistence Mechanisms** | Techniques to maintain access after initial compromise |
| **Command Execution** | Remote command execution and shell access |
| **System Reconnaissance** | System information gathering and enumeration |
| **Data Exfiltration** | Stealing and transmitting sensitive data |
| **Network Communication** | Malicious network connections and C2 communication |
| **Obfuscation Techniques** | Code obfuscation to evade detection |
| **File Operations** | Malicious file read/write/delete operations |
| **Malicious Payload Delivery** | Downloading and executing additional malware |
| **Browser Manipulation** | Browser credential theft and session hijacking |
| **Credential Theft** | Stealing user credentials and tokens |
| **Proxy Manipulation** | Network proxy configuration tampering |
| **Anti-Analysis** | Techniques to evade analysis and debugging |
| **Prototype Pollution** | JavaScript prototype chain attacks |
| **DDoS Capabilities** | Distributed denial of service functionality |
| **Privilege Escalation** | Gaining elevated system privileges |

### 2.1.2 Detection Performance by Tool and Behavior Category

The following table shows the detection rate (%) for each tool across behavior categories:

| Category | PackJ Static | PackJ Trace | OSSGadget | GuardDog | Socket.AI | SAP-XGB | SAP-RF | SAP-DT | GENIE |
|----------|--------------|-------------|-----------|----------|-----------|---------|--------|--------|-------|
| **Persistence Mechanisms** | 99.0% | 96.3% | 92.5% | 98.5% | 41.1% | 86.3% | 78.3% | 77.6% | 50.8% |
| **Command Execution** | 98.7% | 95.9% | 92.3% | 94.2% | 46.0% | 84.3% | 73.0% | 72.3% | 52.1% |
| **System Reconnaissance** | 98.8% | 96.3% | 92.3% | 94.8% | 41.1% | 87.3% | 74.7% | 74.4% | 55.2% |
| **Data Exfiltration** | 99.3% | 97.5% | 92.9% | 93.2% | 43.3% | 89.4% | 74.1% | 73.8% | 56.4% |
| **Network Communication** | 99.3% | 97.8% | 92.3% | 92.1% | 40.6% | 92.3% | 74.3% | 74.0% | 57.0% |
| **Obfuscation Techniques** | 96.4% | 91.3% | 92.7% | 71.5% | 63.7% | 69.8% | 41.2% | 39.9% | 30.9% |
| **File Operations** | 95.1% | 87.0% | 89.6% | 65.2% | 51.3% | 67.7% | 46.9% | 46.6% | 14.0% |
| **Malicious Payload Delivery** | 96.7% | 95.0% | 93.7% | 74.6% | 45.7% | 78.2% | 51.4% | 51.4% | 54.3% |
| **Browser Manipulation** | 98.2% | 92.9% | 88.0% | 68.9% | 72.8% | 72.1% | 46.3% | 45.6% | 18.6% |
| **Credential Theft** | 94.1% | 91.8% | 86.9% | 60.3% | 58.6% | 46.6% | 16.6% | 16.2% | 20.7% |
| **Proxy Manipulation** | 99.6% | 99.2% | 89.7% | 80.6% | 33.6% | 60.9% | 57.3% | 57.3% | 56.5% |
| **Anti-Analysis** | 94.4% | 86.0% | 86.4% | 74.6% | 76.3% | 62.1% | 30.5% | 29.9% | 41.8% |
| **Prototype Pollution** | 78.7% | 73.8% | 88.5% | 37.7% | 72.1% | 42.6% | 18.0% | 18.0% | 39.3% |
| **Privilege Escalation** | 95.0% | 94.7% | 80.0% | 30.0% | 45.0% | 40.0% | 25.0% | 25.0% | N/A |
| **DDoS Capabilities** | 100.0% | 100.0% | 88.2% | N/A | 47.1% | 17.6% | N/A | N/A | 5.9% |

**Note:** N/A indicates insufficient data (no malicious reports detected for that category by the tool).

### 2.1.3 Key Findings - Detection Capability

1. **PackJ Static achieves the highest overall detection rates** (94.1%-100%), demonstrating comprehensive static analysis capabilities across all behavior categories.

2. **PackJ Trace performs second-best** (73.8%-100%), with dynamic analysis providing strong coverage for runtime behaviors.

3. **OSSGadget shows consistent performance** (80.0%-93.7%), with pattern-based detection providing reliable detection across most categories.

4. **GuardDog excels at lifecycle hook detection** (98.5% for Persistence Mechanisms) but struggles with credential theft (60.3%) and privilege escalation (30.0%).

5. **Socket.AI shows variable performance** (33.6%-76.3%), with strengths in Anti-Analysis (76.3%) and Browser Manipulation (72.8%) but weaknesses in Network Communication (40.6%) and Persistence (41.1%).

6. **SAP ML models (XGB, RF, DT) show moderate performance** with XGB outperforming RF and DT in most categories. All struggle significantly with Trace Cleanup and rare attack types.

7. **GENIE performs weakest overall** (5.9%-57.0%), likely due to its specialized CodeQL-based approach targeting specific vulnerability patterns.

### 2.1.4 Detection Gaps Analysis

**Tools struggle most with:**
- Credential Theft: Only PackJ Static (94.1%) and PackJ Trace (91.8%) achieve >90%
- Prototype Pollution: Most tools achieve <80% detection rate
- Privilege Escalation: Significant detection gaps across all tools except PackJ variants
- DDoS Capabilities: Limited detection by most rule-based tools

---

## RQ2.2: How Do Evasion Techniques Impact Detection Effectiveness?

### 2.2.1 Evasion Technique Categories

We identified 14 distinct evasion technique categories in malicious NPM packages:

| Category | Count | Percentage | Description |
|----------|-------|------------|-------------|
| **String_Obfuscation** | 541 | 19.64% | Hiding malicious strings through splitting, Unicode, custom decryption |
| **Encoding_Obfuscation** | 374 | 13.58% | Base64, hexadecimal, Base32 encoding to hide payloads |
| **Silent_Error_Handling** | 366 | 13.28% | Suppressing exceptions to hide malicious behavior |
| **Hook_Abuse** | 352 | 12.78% | Abusing NPM lifecycle hooks (preinstall, postinstall, install) |
| **Code_Structure_Obfuscation** | 325 | 11.80% | Control flow flattening, code splitting, variable indirection |
| **Stealth_Execution** | 263 | 9.55% | Dynamic eval, conditional execution, shell operations |
| **Module_Abuse** | 175 | 6.35% | Abusing built-in modules and legitimate APIs |
| **Network_Communication_Hiding** | 144 | 5.23% | Traffic blending, DNS exfiltration, communication spoofing |
| **Environment_Detection** | 117 | 4.25% | Runtime environment detection for adaptive execution |
| **Anti_Analysis** | 54 | 1.96% | Static analysis prevention, debugging detection, tampering |
| **Trace_Cleanup** | 30 | 1.09% | File and trace cleanup to reduce detection |
| **Dependency_Confusion** | 6 | 0.22% | Exploiting dependency resolution vulnerabilities |
| **Typosquatting** | 4 | 0.15% | Similar package names to deceive users |
| **Runtime_Caching** | 4 | 0.15% | Runtime caching techniques |

### 2.2.2 Detection Rate by Evasion Category

The following table shows how each tool performs against specific evasion techniques:

| Evasion Category | PackJ Static | PackJ Trace | OSSGadget | GuardDog | Socket.AI | SAP-XGB | SAP-RF | SAP-DT | GENIE |
|------------------|--------------|-------------|-----------|----------|-----------|---------|--------|--------|-------|
| **Encoding_Obfuscation** | 99.73% | 97.33% | 96.79% | 76.47% | 71.93% | 79.95% | 66.84% | 66.58% | 30.75% |
| **String_Obfuscation** | 94.64% | 82.62% | 86.14% | 63.77% | 84.10% | 61.00% | 31.05% | 30.87% | 62.85% |
| **Hook_Abuse** | 96.31% | 89.49% | 92.90% | 99.15% | 44.03% | 73.58% | 71.31% | 70.45% | 14.77% |
| **Silent_Error_Handling** | 98.09% | 91.80% | 93.17% | 83.88% | 62.57% | 77.05% | 54.92% | 54.37% | 65.30% |
| **Code_Structure_Obfuscation** | 95.08% | 85.85% | 86.15% | 71.69% | 84.00% | 70.77% | 39.38% | 39.38% | 68.92% |
| **Anti_Analysis** | 100.00% | 96.30% | 75.93% | 22.22% | 64.81% | 62.96% | 5.56% | 5.56% | 27.78% |
| **Network_Communication_Hiding** | 99.31% | 97.92% | 97.22% | 96.53% | 52.78% | 90.28% | 78.47% | 77.08% | 65.97% |
| **Stealth_Execution** | 91.25% | 76.81% | 85.55% | 56.65% | 74.90% | 50.95% | 24.33% | 24.33% | 33.08% |
| **Environment_Detection** | 88.03% | 71.79% | 93.16% | 63.25% | 52.99% | 49.57% | 33.33% | 33.33% | 35.04% |
| **Module_Abuse** | 98.29% | 94.29% | 95.43% | 85.71% | 53.71% | 88.57% | 70.29% | 69.14% | 69.14% |
| **Trace_Cleanup** | 60.00% | 63.33% | 86.67% | 100.00% | 80.00% | 13.33% | 10.00% | 10.00% | 3.33% |
| **Dependency_Confusion** | 100.00% | 100.00% | 100.00% | 100.00% | 33.33% | 100.00% | 100.00% | 100.00% | 33.33% |
| **Typosquatting** | 100.00% | 75.00% | 100.00% | 75.00% | 50.00% | 25.00% | 75.00% | 75.00% | 0.00% |
| **Runtime_Caching** | 100.00% | 100.00% | 25.00% | 75.00% | 100.00% | 100.00% | 50.00% | 50.00% | 0.00% |

### 2.2.3 Most Effective Evasion Techniques

**Evasion techniques that significantly reduce detection:**

1. **Anti_Analysis** (against GuardDog): Only 22.22% detection rate, compared to 100% by PackJ Static
   - Techniques include: Anti-debugging, static analysis evasion, code obfuscation

2. **Hook_Abuse** (against GENIE): Only 14.77% detection rate
   - GENIE's CodeQL-based approach misses NPM lifecycle hook exploitation

3. **Stealth_Execution** (against SAP-RF/DT): Only 24.33% detection rate
   - Dynamic eval and conditional execution evade static feature extraction

4. **Trace_Cleanup** (against SAP models): 10.00-13.33% detection rate
   - File cleanup operations evade behavior-based ML models

5. **Environment_Detection** (against SAP-DT): 33.33% detection rate
   - Adaptive execution based on environment detection evades static analysis

### 2.2.4 Evasion Technique Combinations

Malicious packages frequently combine multiple evasion techniques:

| Combination | Count | Percentage |
|-------------|-------|------------|
| Code_Structure_Obfuscation + String_Obfuscation | 106 | 36.81% |
| Encoding_Obfuscation + String_Obfuscation | 48 | 16.67% |
| Stealth_Execution + String_Obfuscation | 25 | 8.68% |
| Encoding_Obfuscation + Hook_Abuse | 19 | 6.60% |
| Encoding_Obfuscation + Network_Communication_Hiding | 13 | 4.51% |
| Hook_Abuse + Stealth_Execution | 13 | 4.51% |
| Silent_Error_Handling + String_Obfuscation | 10 | 3.47% |
| Stealth_Execution + Trace_Cleanup | 10 | 3.47% |
| Environment_Detection + Stealth_Execution | 9 | 3.12% |
| Encoding_Obfuscation + Module_Abuse | 5 | 1.74% |

**Key Finding:** The most common combination is **Code_Structure_Obfuscation + String_Obfuscation** (36.81%), indicating attackers primarily rely on layered obfuscation strategies.

### 2.2.5 Tool Vulnerability Analysis

| Tool | Weakest Against | Detection Rate | Strongest Against | Detection Rate |
|------|-----------------|----------------|-------------------|----------------|
| **PackJ Static** | Trace_Cleanup | 60.00% | Anti_Analysis | 100.00% |
| **PackJ Trace** | Trace_Cleanup | 63.33% | Dependency_Confusion | 100.00% |
| **OSSGadget** | Runtime_Caching | 25.00% | Dependency_Confusion | 100.00% |
| **GuardDog** | Anti_Analysis | 22.22% | Trace_Cleanup | 100.00% |
| **Socket.AI** | Dependency_Confusion | 33.33% | Runtime_Caching | 100.00% |
| **SAP-XGB** | Trace_Cleanup | 13.33% | Dependency_Confusion | 100.00% |
| **SAP-RF** | Anti_Analysis | 5.56% | Dependency_Confusion | 100.00% |
| **SAP-DT** | Anti_Analysis | 5.56% | Dependency_Confusion | 100.00% |
| **GENIE** | Typosquatting/Runtime_Caching | 0.00% | Code_Structure_Obfuscation | 68.92% |

---

## RQ2.3: What Are the Primary Attack Vectors in Malicious NPM Packages?

### 2.3.1 NPM Lifecycle Hook Distribution

Malicious packages heavily abuse NPM lifecycle hooks for automatic code execution during package installation:

| Hook Type | Count | Percentage |
|-----------|-------|------------|
| **preinstall** | 4,536 | 83.97% |
| **postinstall** | 657 | 12.16% |
| **install** | 150 | 2.78% |
| **other** | 59 | 1.09% |
| **Total** | 5,402 | 100.00% |

**Key Finding:** **preinstall** hooks dominate at 83.97%, as they execute before any dependencies are installed, providing immediate code execution opportunity.

### 2.3.2 Why preinstall is Preferred

1. **Immediate Execution**: Runs before dependency resolution, ensuring malicious code executes even if installation fails later
2. **Minimal Footprint**: Less likely to leave traces as package installation may not complete
3. **Evasion Opportunity**: Can check environment and abort before full installation if sandbox detected
4. **Early Access**: Gains access to system before any security tools that might be installed as dependencies

### 2.3.3 Malicious Code File Locations

Based on GuardDog detection patterns, malicious code is distributed across:

| File Location | Approximate Percentage |
|---------------|----------------------|
| **index.js** | ~46.9% |
| **package.json** (scripts section) | ~38.2% |
| **Other .js files** | ~13.1% |
| **Hidden/obfuscated files** | ~1.8% |

**Common patterns:**
- `"preinstall": "node index.js"` - Execute main malicious script
- `"preinstall": "node index.js > /dev/null 2>&1"` - Silent execution
- `"preinstall": "node new.js"` - Secondary script execution

### 2.3.4 Attack Vector Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    NPM Package Structure                     │
├─────────────────────────────────────────────────────────────┤
│  package.json                                               │
│    ├── scripts.preinstall  ────→  83.97% of hooks          │
│    ├── scripts.postinstall ────→  12.16% of hooks          │
│    └── scripts.install     ────→   2.78% of hooks          │
├─────────────────────────────────────────────────────────────┤
│  Malicious Code Entry Points                                 │
│    ├── index.js            ────→  ~46.9% of code locations  │
│    ├── package.json inline ────→  ~38.2% of code locations  │
│    └── Other .js files     ────→  ~14.9% of code locations  │
└─────────────────────────────────────────────────────────────┘
```

### 2.3.5 Common Attack Patterns

**Top 10 Most Frequent Malicious Code Patterns:**

| Rank | Pattern Type | Occurrences | Description |
|------|-------------|-------------|-------------|
| 1 | HTTP Request Data Write | 2,410 | `req.write(postData)` - Data exfiltration |
| 2 | npm-obfuscation | 2,145 | `"preinstall":"node index.js"` - Hook execution |
| 3 | npm-install-script | 1,393 | HTTPS request handlers for C2 |
| 4 | shady-links | 653 | HTTPS request with process.stdout |
| 5 | npm-install-script | 374 | `"preinstall": "node new.js"` |
| 6 | npm-exfiltrate-sensitive-data | 298 | HTTPS request data handlers |
| 7 | shady-links | 284 | `https.get('https://ipinfo.io/json'` |
| 8 | shady-links | 224 | Discord webhook URLs for exfiltration |
| 9 | npm-install-script | 156 | `"preinstall": "node index.js > /dev/null 2>&1"` |
| 10 | shady-links | 149 | Additional preinstall patterns |

---

## Summary and Recommendations

### Detection Tool Comparison

| Tool | Type | Strengths | Weaknesses | Overall Rate |
|------|------|-----------|------------|--------------|
| **PackJ Static** | Static Analysis | Comprehensive coverage, highest detection rates | Trace cleanup detection | ~95-99% |
| **PackJ Trace** | Dynamic Analysis | Runtime behavior detection | Resource intensive | ~85-97% |
| **OSSGadget** | Pattern Matching | Consistent performance, network detection | Runtime caching | ~80-97% |
| **GuardDog** | Semgrep Rules | Excellent hook detection (99.15%) | Anti-analysis (22.22%) | ~60-100% |
| **Socket.AI** | AI/ML Hybrid | Balanced approach | Dependency confusion, hooks | ~35-84% |
| **SAP-XGB** | ML (XGBoost) | Network communication | Trace cleanup, rare attacks | ~50-90% |
| **SAP-RF** | ML (Random Forest) | Dependency confusion | Anti-analysis (5.56%) | ~25-100% |
| **SAP-DT** | ML (Decision Tree) | Dependency confusion | Anti-analysis (5.56%) | ~25-100% |
| **GENIE** | CodeQL | Specific vulnerability patterns | Hook abuse (14.77%) | ~0-69% |

### Recommendations for Detection Improvement

1. **Combine static and dynamic analysis** - PackJ's dual approach achieves highest coverage
2. **Enhance hook abuse detection** - Focus on preinstall hooks (83.97% of attack vectors)
3. **Improve anti-analysis resistance** - Current tools vulnerable to debugging detection
4. **Add trace cleanup detection** - Most tools miss file cleanup operations
5. **Monitor common file locations** - Prioritize index.js and package.json analysis
6. **Detect evasion combinations** - 36.81% use Code_Structure + String obfuscation

### Key Statistics Summary

| Metric | Value |
|--------|-------|
| Total malicious packages | 5,642 |
| Packages using install hooks | 5,402 (95.7%) |
| Most common hook | preinstall (83.97%) |
| Most common evasion | String_Obfuscation (19.64%) |
| Best performing tool | PackJ Static (~95-99%) |
| Most evaded tool | GENIE (~0-69%) |
| Most common evasion combo | Code_Structure + String_Obfuscation (36.81%) |

---

*Generated for NPMAnalysis Research Project - RQ2 Analysis*
