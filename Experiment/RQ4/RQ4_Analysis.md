# RQ4: Tool Complementarity Analysis

## 1. Overview

This analysis examines how different malware detection tools can be combined to achieve better detection performance than individual tools. We evaluate **156 pairwise combinations** using two strategies:

- **Union Strategy**: Flag as malicious if **either** tool detects it (OR logic) → Maximizes recall
- **Intersection Strategy**: Flag as malicious only if **both** tools agree (AND logic) → Maximizes precision

## 2. Top Performing Combinations

### 2.1 Union Strategy - Best Combinations (by F1-Score)

| Rank | Tool 1 | Tool 2 | Accuracy | Precision | Recall | F1 | TP | TN |
|------|--------|--------|----------|-----------|--------|-----|-----|-----|
| 1 | Cerebro | MalPac-SVM | **95.92%** | 97.58% | 92.45% | **94.95%** | 4605 | 6915 |
| 2 | SocketAI | MalPac-SVM | 94.98% | 97.36% | 91.89% | 94.55% | 6016 | 7125 |
| 3 | GuardDog | SocketAI | 94.88% | 94.66% | 94.52% | 94.59% | 6188 | 6939 |
| 4 | SocketAI | MalPac-NB | 94.93% | 97.14% | 91.98% | 94.49% | 6022 | 7111 |
| 5 | SocketAI | MalPac-MLP | 94.37% | 96.49% | 91.43% | 93.89% | 5986 | 7070 |
| 6 | SAP-XGB | MalPac-SVM | 94.22% | 93.65% | 94.18% | 93.91% | 6165 | 6870 |
| 7 | GuardDog | MalPac-SVM | 94.17% | 95.03% | 92.53% | 93.76% | 6058 | 6971 |

### 2.2 Intersection Strategy - Best Combinations (by F1-Score)

| Rank | Tool 1 | Tool 2 | Accuracy | Precision | Recall | F1 | TP | TN |
|------|--------|--------|----------|-----------|--------|-----|-----|-----|
| 1 | GuardDog | Packj-Static | **92.66%** | 95.60% | 88.56% | **91.94%** | 5797 | 7021 |
| 2 | Packj-Static | MalPac-SVM | 92.48% | 98.23% | 85.66% | 91.51% | 5607 | 7187 |
| 3 | GuardDog | Packj-Trace | 91.47% | 96.40% | 85.15% | 90.43% | 5573 | 7080 |
| 4 | Packj-Static | MalPac-NB | 91.68% | 97.85% | 84.27% | 90.55% | 5516 | 7167 |
| 5 | Packj-Static | MalPac-MLP | 91.61% | 97.40% | 84.54% | 90.51% | 5534 | 7140 |
| 6 | GuardDog | MalPac-SVM | 91.53% | 98.14% | 83.69% | 90.34% | 5479 | 7184 |

## 3. Why These Combinations Work

### 3.1 Union Strategy Analysis

**Best: Cerebro + MalPac-SVM (F1=94.95%)**
- **Cerebro** (ML-based): Uses graph neural networks to analyze package dependency and code structure
- **MalPac-SVM** (ML-based): Uses SVM classifier on extracted features
- **Complementarity**: Different ML approaches capture different malicious patterns
- Both are ML-based but use fundamentally different feature representations

**Second: SocketAI + MalPac-SVM (F1=94.55%)**
- **SocketAI** (LLM-based): Semantic understanding of code behavior
- **MalPac-SVM** (ML-based): Statistical pattern recognition
- **Complementarity**: LLM understands intent; ML captures statistical anomalies

**Third: GuardDog + SocketAI (F1=94.59%)**
- **GuardDog** (Static rule-based): Pattern matching for known malicious indicators
- **SocketAI** (LLM-based): Semantic code analysis
- **Complementarity**: Rules catch known patterns; LLM catches novel/obfuscated attacks

### 3.2 Intersection Strategy Analysis

**Best: GuardDog + Packj-Static (F1=91.94%)**
- Both are **static analysis** tools (fast execution)
- **GuardDog**: Rule-based pattern matching
- **Packj-Static**: AST analysis and risky API detection
- **High Precision (95.60%)**: When both agree, confidence is very high
- **Trade-off**: Lower recall (88.56%) due to strict requirement

**Second: Packj-Static + MalPac-SVM (F1=91.51%)**
- **Packj-Static**: Code structure analysis
- **MalPac-SVM**: Feature-based classification
- **Precision: 98.23%** - Extremely low false positive rate
- Best for environments where false alarms are costly

## 4. Performance vs. Speed Trade-offs

### 4.1 Tool Speed Categories

| Category | Tools | Speed | Use Case |
|----------|-------|-------|----------|
| **Fast (Static)** | OSSGadget, GuardDog, GENIE, Packj-Static | ~1-5 sec/package | CI/CD pipelines, real-time scanning |
| **Medium (ML)** | SAP-DT/RF/XGB, Cerebro, MalPacDetector | ~5-30 sec/package | Batch processing, nightly scans |
| **Slow (Dynamic)** | Packj-Trace | ~1-5 min/package | Deep analysis, suspicious packages |
| **API-dependent** | SocketAI | Variable | When accuracy is critical |

### 4.2 Recommended Combinations by Use Case

#### High-Speed Pipeline (CI/CD Integration)
```
Recommendation: GuardDog + Packj-Static (Intersection)
- F1: 91.94%, Precision: 95.60%
- Both tools are static, total time: ~5-10 sec/package
- Low false positives won't block legitimate packages
```

#### Maximum Detection Coverage
```
Recommendation: GuardDog + SocketAI (Union)
- F1: 94.59%, Recall: 94.52%
- Catches both pattern-based and semantic malware
- Accept higher false positive rate for better coverage
```

#### Balanced Performance (Best Overall)
```
Recommendation: Cerebro + MalPac-SVM (Union)
- F1: 94.95%, Accuracy: 95.92%
- Both ML-based, reasonable processing time
- Best balance of precision and recall
```

#### Minimum False Positives (Conservative)
```
Recommendation: GENIE + GuardDog (Intersection)
- Precision: 99.83%, but Recall: 44.55%
- Only flags when very confident
- For manual review workflows
```

## 5. Strategy Comparison

### 5.1 Union vs Intersection Performance

| Metric | Union (Best) | Intersection (Best) | Difference |
|--------|--------------|---------------------|------------|
| F1-Score | 94.95% | 91.94% | +3.01% |
| Accuracy | 95.92% | 92.66% | +3.26% |
| Precision | 97.58% | 95.60% | +1.98% |
| Recall | 92.45% | 88.56% | +3.89% |

**Key Insight**: Union strategies consistently outperform intersection in overall metrics because:
1. Malware detection benefits from **high recall** (missing malware is costly)
2. Union combines detection capabilities additively
3. Intersection's strict requirement causes significant **false negatives**

### 5.2 When to Use Each Strategy

| Strategy | Best For | Avoid When |
|----------|----------|------------|
| **Union** | Security-critical environments, comprehensive scanning, unknown threats | High false positive costs, limited review resources |
| **Intersection** | Automated blocking, CI/CD gates, compliance checks | Missing malware is unacceptable, emerging threats |

## 6. Cross-Category Complementarity

### 6.1 Best Cross-Category Combinations

| Category Combination | Example | Union F1 | Insight |
|---------------------|---------|----------|---------|
| Static + LLM | GuardDog + SocketAI | 94.59% | Rules + Semantics |
| ML + LLM | MalPac-SVM + SocketAI | 94.55% | Statistics + Understanding |
| ML + ML (different) | Cerebro + MalPac-SVM | 94.95% | Different feature spaces |
| Static + Static | GuardDog + Packj-Static | 68.24% (Union), 91.94% (Intersection) | Pattern overlap |

### 6.2 Key Findings

1. **Cross-methodology combinations work best for Union**
   - Different detection approaches catch different malware types
   - LLM + Rule-based achieves excellent coverage

2. **Same-methodology combinations work well for Intersection**
   - Agreement between similar tools indicates high confidence
   - Static + Static achieves best precision

3. **Dynamic analysis (Packj-Trace) considerations**
   - Adds significant time overhead
   - Best reserved for second-stage analysis of flagged packages
   - Union with Packj-Trace: Very high recall but slow

## 7. Practical Deployment Recommendations

### 7.1 Two-Stage Detection Pipeline

```
Stage 1 (Fast Filter):
├── GuardDog + Packj-Static (Intersection)
├── Time: ~5-10 seconds
├── If flagged → Block immediately (high confidence)
└── If clean → Proceed to Stage 2

Stage 2 (Deep Analysis):
├── SocketAI + MalPac-SVM (Union)
├── Time: ~30-60 seconds
├── Catches sophisticated/obfuscated malware
└── Final decision with detailed report
```

### 7.2 Resource-Constrained Environments

```
Single Tool Priority: GuardDog (best standalone static)
Two-Tool Combo: GuardDog + SAP-XGB (Union)
  - F1: 93.44%
  - No API dependencies
  - Fully offline capable
```

### 7.3 Maximum Security Environments

```
Three-Tool Ensemble:
1. GuardDog (Static rules)
2. MalPac-SVM (ML features)
3. SocketAI (LLM semantics)

Decision Logic:
- Block if 2+ tools flag (majority voting)
- Review if 1 tool flags (manual inspection)
- Allow if 0 tools flag
```

## 8. Summary Statistics

| Metric | Best Union | Best Intersection |
|--------|------------|-------------------|
| Highest F1 | Cerebro + MalPac-SVM (94.95%) | GuardDog + Packj-Static (91.94%) |
| Highest Accuracy | Cerebro + MalPac-SVM (95.92%) | GuardDog + Packj-Static (92.66%) |
| Highest Precision | GENIE + SocketAI (99.92%) | GENIE + SAP-DT (100%) |
| Highest Recall | Packj-Static + MalPac-MLP (99.83%) | GuardDog + OSSGadget (82.14%) |
| Fastest High-F1 | GuardDog + Packj-Static (Union: 68.24%) | GuardDog + Packj-Static (91.94%) |

## 9. Conclusions

1. **Tool complementarity significantly improves detection**: Best combinations achieve 20-30% improvement over individual tools.

2. **Union strategy is generally superior**: Higher F1, accuracy, and recall in most cases.

3. **Intersection strategy excels in precision**: Best for automated blocking with minimal false positives.

4. **Cross-methodology combinations are most effective**: Combining static rules, ML, and LLM approaches captures the widest range of malware.

5. **Performance trade-offs are manageable**: Two-stage pipelines can balance speed and accuracy effectively.

6. **Recommended default combination**:
   - **For coverage**: GuardDog + SocketAI (Union) - F1: 94.59%
   - **For precision**: GuardDog + Packj-Static (Intersection) - F1: 91.94%
   - **For balance**: Cerebro + MalPac-SVM (Union) - F1: 94.95%
