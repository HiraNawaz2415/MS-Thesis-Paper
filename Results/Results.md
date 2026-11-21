## Results

# README — ready-to-copy replacements

Apply to `README.md` in https://github.com/HiraNawaz2415/MS-Thesis-Paper. Sections are named as they appear in the current README. Wording uses only facts verified in the project files and the ROCOv2 paper. Delete any line that refers to a file you do not upload.

---
## Replace the whole "Dataset" subsection text about labels (keep the sample-count table)

The 18 labels are the UMLS CUIs of the manually curated ROCOv2 concept vocabulary (6 imaging modalities, 8 anatomical regions, 2 radiographic projections, 2 acquisition planes). The original reason for adopting this vocabulary is not documented in the project files. Targets were built from the combined ROCOv2 concept files (`train_concepts.csv`, `valid_concepts.csv`, `test_concepts.csv`), which contain manually created and automatically extracted concepts; some positives, mainly for anatomical regions, therefore come from automatically extracted, caption-derived concepts. Records with none of the 18 CUIs (292 Train, 84 Validation, 57 Test) and one Validation record with an empty caption were excluded, leaving 59,666 / 9,819 / 9,870 images. The Test set was split in half with seed 42 into a Calibration set (4,935) and a Test-final set (4,935).

## Replace "Repository Structure"

```
Notebooks/            Notebooks 01-14 and the multi-seed aggregation (Colab)
Results/              Results.md and a Google Drive link file
split_ids/            image IDs of Train, Validation, Calibration and Test-final (one ID per line)   [only if uploaded]
config/               label_mapping.json, dataset_config.json                                          [only if uploaded]
scripts/              article_overlap_analysis.py                                                      [only if uploaded]
README.md
```

## Replace "Limitations" bullet on identifiers

ROCOv2 provides no patient or study identifiers, so patient-level independence of the partitions cannot be assessed. ROCOv2's `license_information.csv` gives the PubMed Central article ID of each image: no article is shared between Train and the other partitions, but 62.9% of Test-final images (3,102 of 4,935) come from articles that also contribute Validation images, and 22.7% (1,122) from articles that also contribute Calibration images. Test-final is therefore not independent of the Validation and Calibration partitions at article level.

## Replace the "Reproducibility and Data Availability" text

This repository contains the notebooks and result summaries of the study [and the image identifiers of each partition, the label mapping, the dataset configuration and the script for the article-overlap analysis]. It does not redistribute ROCOv2 images, captions or `license_information.csv`; obtain them from the official ROCOv2 release (Zenodo DOI 10.5281/zenodo.10821435, as cited in the ROCOv2 paper) and follow its licensing terms. Repository URL: https://github.com/HiraNawaz2415/MS-Thesis-Paper

To rerun the article-overlap analysis, place `license_information.csv`, the prepared CSV files of Notebook 02, `test_final_logits_fp32.csv` and `qhat_fp32.json` in one folder and run:

```
python scripts/article_overlap_analysis.py --data-dir <folder> --logits <folder>/test_final_logits_fp32.csv --qhat <folder>/qhat_fp32.json
```

## Replace the Trust Score sentence in "Experimental Results"

The Composite Trust Score did not improve error detection over raw model confidence (AUROC 0.9670 vs 0.9744, full-precision conformal thresholds; the earlier float16 value of 0.9545 is superseded). Conformal marginal coverage at nominal 90% was 0.9026 (the earlier float16 value of 0.9106 is superseded), with positive-class coverage 0.7224.

## Delete

- "Repository URL: To be added."
- "The repository contents and availability will be updated by the authors."
- The Python snippet at the end of the README (a pandoc call writing `/mnt/data/README.md`).
- `Results/Result_link_of_Google_Drive.txt` if the Drive link is not meant to be public (the reviewer could not open it).

## Not included on purpose

No licence text. A licence needs the authors' and institution's decision.

The complete experimental results, graphs, and evaluation
tables are available below:

[📊 View Complete Results on Google (https://drive.google.com/drive/folders/1EwAkVvA5bbOpY8oE6eOqxTRNSXZGUaxK
