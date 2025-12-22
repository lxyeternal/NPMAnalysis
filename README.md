# NPM Malware Detection Benchmark

An empirical study evaluating NPM malware detection tools.

## Project Structure

```
NPMAnalysis/
├── Core/                          # Core analysis modules
│   ├── Analysis/                  # Behavior and code analysis
│   │   ├── behavior/              # Malicious behavior classification
│   │   └── code_snipptes/         # Code pattern analysis
│   ├── Data/                      # Data collection and processing
│   │   ├── collection/            # Dataset collection scripts
│   │   ├── cleaning/              # Data cleaning scripts
│   │   └── timecollect/           # Timestamp data collection
│   └── ToolDetection/             # Detection tool evaluation
│       └── DetectionResults/      # Tool detection outputs
│
├── Experiment/                    # Research experiments
│   ├── RQ2/                       # Detection rate analysis
│   │   ├── code/                  # Analysis scripts
│   │   └── statistic/             # Results and figures
│   ├── RQ3/                       # Temporal trend analysis
│   │   ├── code/                  # Analysis scripts
│   │   └── statistic/             # Results and figures
│   └── RQ4/                       # Tool complementarity analysis
│
└── Dataset/                       # Malware and benign samples
```

## Detection Tools Evaluated

| Tool | Type |
|------|------|
| GENIE | Rule-based |
| GuardDog | Rule-based |
| OSSGadget | Rule-based |
| SocketAI | Rule-based |
| SAP-DT | ML-based |
| SAP-RF | ML-based |
| SAP-XGB | ML-based |
| Packj-Static | Hybrid |
| Packj-Trace | Hybrid |

## Research Questions

- **RQ2**: How effective are detection tools against different malicious behaviors and evasion techniques?
- **RQ3**: How do detection rates change over time?
- **RQ4**: Can combining multiple tools improve detection coverage?

## Requirements

- Python 3.8+
- pandas, numpy, matplotlib, seaborn

## Usage

```bash
# RQ2: Generate detection rate heatmaps
cd Experiment/RQ2/code
python detection_rate_heatmap.py
python evasion_detection_heatmap.py

# RQ3: Generate temporal trend analysis
cd Experiment/RQ3/code
python detection_rate_over_time.py

# RQ4: Tool complementarity analysis
cd Experiment/RQ4
python multi_tool_fusion.py
```

## License

MIT License
