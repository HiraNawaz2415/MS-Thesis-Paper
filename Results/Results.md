# Results summary

Caption-assisted multi-label classification of radiological imaging characteristics on ROCOv2 (18 UMLS CUI labels: imaging modality, anatomical region, radiographic projection, acquisition plane). These are summary values taken from the revised manuscript. The manuscript is the authoritative source; see it for definitions, confidence intervals and caveats. The labels describe imaging characteristics, not diagnoses, so the results do not measure diagnostic accuracy.

Large output files (model checkpoints, per-sample prediction files) are not stored in this repository. ROCOv2 images, captions and `license_information.csv` are not redistributed; obtain them from the official ROCOv2 release (Zenodo DOI 10.5281/zenodo.10821435, as cited in the ROCOv2 paper) and follow its licence terms.

## Detailed Results Files
[View Results](https://drive.google.com/drive/folders/1EwAkVvA5bbOpY8oE6eOqxTRNSXZGUaxK?usp=sharing)

## Data partitions

| Partition | Images | Use |
|---|---|---|
| Train | 59,666 | model training |
| Validation | 9,819 | model development and checkpoint selection |
| Calibration | 4,935 | conformal thresholds (random half of the official Test set, seed 42) |
| Test-final | 4,935 | final evaluation (other random half of the official Test set) |

Excluded before this split: 292 Train, 84 Validation and 57 Test records with none of the 18 CUIs, and one Validation record with an empty caption. Labels are built from the combined ROCOv2 concept files (manual and automatic concepts), so some positives, mainly for anatomical regions, are caption-derived.

## Predictive performance (Test-final, threshold 0.5)

| Model | Macro-F1 | Notes |
|---|---|---|
| Proposed multimodal VLM (image + caption) | 0.8311 | Micro-F1 0.9285, Hamming loss 0.0126, subset accuracy 0.8634, macro ROC-AUC 0.9954 (stored predictions of the original run) |
| Same model, float32 recomputation | 0.8308 | differs from the stored predictions in 2 of 88,830 label decisions |
| Multi-seed mean (VLM) | 0.8370 ± 0.0052 | Micro-F1 0.9307 ± 0.0020 |
| Multi-seed mean (DenseNet121, image only) | 0.7212 ± 0.0047 | Micro-F1 0.8611 ± 0.0057 |
| Caption-only TF-IDF + logistic regression | 0.7075 | trained on Train only |
| Caption-only frozen BiomedCLIP text encoder | 0.6416 | trained on Train only |

Caption masking (trained VLM, inference only): intact caption 0.8308; strict label terms deleted 0.7639; empty caption 0.6983. The losses are concentrated in anatomical labels (Pelvis, Abdomen, Chest). The reported performance is therefore that of a caption-assisted setting.

## Conformal prediction (Test-final, nominal coverage 90%, full-precision thresholds)

| Quantity | Value |
|---|---|
| Mean per-label marginal coverage | 0.9026 (95% CI 0.8990–0.9061) |
| Positive-class coverage | 0.7224 |
| Negative-class coverage | 0.9199 |
| All 18 labels covered for an image | 0.4101 |
| Empty prediction sets | 9.58% |
| Mean set size | 0.9042 |

This is empirical coverage on one random split, not a certified guarantee for new articles or deployment. The earlier float16-based coverage value (0.9106) is superseded.

## Composite Trust Score (500 Test-final images, 9,000 label predictions, 101 errors)

| Signal | Error-detection AUROC |
|---|---|
| Raw model confidence | 0.9744 |
| Counterfactual component only | 0.9671 |
| Composite Trust Score (0.5 / 0.5) | 0.9670 |
| Conformal component only | 0.9053 |

The composite score did not improve on raw confidence. The min–max normalisation is taken over this sample, so the score is used only to rank predictions within it; no calibration-fixed normalisation was implemented. The earlier float16-based value (0.9545) is superseded.

## Partition overlap

Using the article IDs in ROCOv2's `license_information.csv`: no article occurs in Train and any other partition; 4,477 of 44,766 distinct articles occur in more than one partition (Validation–Calibration 2,646, Validation–Test-final 2,554, Calibration–Test-final 917). 3,102 of 4,935 Test-final images (62.9%) come from articles that also contribute Validation images, and 1,122 (22.7%) from articles that also contribute Calibration images. On Test-final images whose article has no Validation image (1,833), Micro-F1 is 0.9326 and Macro-F1 0.8215. Patient-level independence is not established. The analysis is reproduced by `scripts/article_overlap_analysis.py`.
