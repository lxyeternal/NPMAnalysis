# IntelGuard

IntelGuard is a knowledge-driven malicious package detector. It builds a
knowledge base of expert reasoning from public security reports and uses that
knowledge to guide an LLM when judging unknown packages.

The code lives in its own repository and is not duplicated here:

https://github.com/lxyeternal/IntelGuard

## Knowledge base used in this benchmark

`KnowledgeBase/` holds the knowledge base used for the npm experiments in this
repository. Reports whose packages appear in the benchmark dataset were removed
before building it, so the detector never retrieves knowledge about a package it
is being evaluated on.

| File | Content |
|---|---|
| `knowledge_base.json` | 4,209 reports, 7,297 malicious code snippets |
| `snippet_code_embeddings.npy` | code embeddings of the snippets (text-embedding-3-large, 3072-d) |
| `snippet_behavior_embeddings.npy` | behavior embeddings of the snippets |
| `clusters.json` | code-level and behavior-level HDBSCAN clusters |
| `behavior_cluster_centroids.npy` | centroids of the behavior clusters |
| `removed_kb_ids.json` | ids of the 211 reports removed because of dataset overlap |

## Usage

Clone IntelGuard, fill in `Configs/llm_config.json`, and point the detector at
this knowledge base:

```bash
git clone https://github.com/lxyeternal/IntelGuard.git
cd IntelGuard
python Codes/Detect/run_npm_dataset.py \
    --dataset-root <NPMAnalysis>/Dataset \
    --output-root <NPMAnalysis>/Experiment/Results/IntelGuard \
    --kb-path <NPMAnalysis>/Tools/IntelGuard/KnowledgeBase \
    --limit 0
```

A single package can be checked with
`python Codes/Detect/package_detector.py <package_dir> -m npm --kb-path <NPMAnalysis>/Tools/IntelGuard/KnowledgeBase`.
The environment variable `INTELGUARD_KB_PATH` can be set instead of `--kb-path`.

## Output

- Location: `Experiment/Results/IntelGuard/[benign|malware]/[package_name]/[version]/result.json`
- Format: one JSON report per package listing every code slice with its
  trigger, sensitive APIs, retrieved knowledge and the LLM verdict; the package
  is malicious if any slice is judged malicious.
