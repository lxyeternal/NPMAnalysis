# EMPHunter

EMPHunter (Extended Malicious Packages Hunter) detects malicious npm packages
without labeled malicious examples. It parses the installation scripts of each
package into API sequences, embeds them with FastText-PVDM document embedding
models, clusters the embeddings and ranks the outliers as candidate malware.

The code and the pretrained models are distributed by the authors and are not
duplicated here:

- Code: https://github.com/rwnbiad105/EMPHunter
- Data and pretrained embedding models: https://zenodo.org/records/15470290

## Usage in this benchmark

Clone the repository, download the data archive from Zenodo and place the
`DataShare/` models and base data as described in the upstream README. The
pipeline is configured in `npm/EMPHunter-npm/main.py`: set the unpacked target
package directory to `Dataset/unzip_benign/` or `Dataset/unzip_malware/` of this
repository and give the batch a name, then run

```bash
cd EMPHunter/npm/EMPHunter-npm
python main.py
```

A package is reported as malicious when one of its installation hooks is ranked
as an outlier.

## Output

- Location: `Experiment/Results/EMPHunter/[benign|malware]/[package_name]/[version]/result.txt`
- Format: one text report per package with the analysed installation hooks,
  their EMPHunter package ids, the outlier flag and the ranking score
- Summary: `Experiment/Results/EMPHunter/_eval_summary/`
