# ProfMal

ProfMal detects malicious npm packages with a graph-based model that combines
static and dynamic analysis. It builds a code property graph with Joern and a
call graph with Jelly, records dynamic call graphs and sensitive API invocations
with NodeProf on Graal.js, merges them into a behavior graph and classifies the
graph with a heterogeneous graph transformer.

The code and the trained model are distributed by the authors and are not
duplicated here:

- Code: https://github.com/yiheng98/ProfMal
- Customized Joern 4.0.227 used by the tool: linked from the upstream README

## Usage in this benchmark

Clone the repository, install Python 3.11 dependencies, Jelly 0.10.0 and the
customized Joern, and set `joern_path` and `workspace_path` in `config.yaml`.
Each unpacked package under `Dataset/unzip_benign/` or `Dataset/unzip_malware/`
is then analysed with

```bash
cd ProfMal
python main.py --package <package_dir>
```

A package is reported as malicious when the classifier labels its behavior
graph as malicious.

## Output

- Location: `Experiment/Results/ProfMal/[benign|malware]/[package_name]/[version]/`
- Format: `result.txt` with the verdict and run time, `sensitive.dot` with the
  sensitive-API subgraph of the behavior graph, and `work_flow.log` with the
  analysis log
- Summary: `Experiment/Results/ProfMal/[benign|malware]/summary_[benign|malware].csv`
