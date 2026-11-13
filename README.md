# Caption-Assisted Multi-Label Classification of Radiological Imaging Characteristics

**Conformal Prediction, Latent Decision-Boundary Sensitivity, and an Exploratory Trust Score**

## Overview

This project investigates a multimodal vision-language approach for multi-label classification of radiological imaging characteristics using the ROCOv2 dataset.

The framework combines radiological images and their associated captions using **BiomedCLIP**. It predicts 18 UMLS CUI-based labels describing imaging characteristics, including modality, anatomical region, projection, and plane.

The study additionally investigates split conformal prediction, latent decision-boundary sensitivity, and an exploratory Composite Trust Score.

**Important scope:** The 18 labels describe radiological imaging characteristics, not pathological diagnoses. This project evaluates model behaviour on the specified dataset and does not establish clinical diagnostic accuracy or clinical effectiveness.

## Research Objectives

- Evaluate multimodal image-caption classification using BiomedCLIP.
- Predict 18 radiological imaging-characteristic labels.
- Compare multimodal performance with a DenseNet121 baseline.
- Examine the influence of caption information on model predictions.
- Evaluate prediction-set behaviour using split conformal prediction.
- Investigate latent decision-boundary sensitivity.
- Examine the exploratory Composite Trust Score and its relationship with prediction confidence.
- Assess sensitivity to identified image reuse across dataset partitions.

## Dataset

**ROCOv2**

The dataset contains radiological images with associated captions and labels.

| Dataset component | Number of samples |
|---|---:|
| Training | 59,666 |
| Validation | 9,819 |
| Test | 9,870 |
| Calibration split | 4,935 |
| Final test split | 4,935 |

The final test and calibration splits are treated separately in the evaluation pipeline.

### Classification labels

The model predicts 18 UMLS CUI-based labels representing:

- Imaging modality
- Anatomical region
- Projection
- Imaging plane

Pathology labels are not part of the target classification task.

**Dataset access:** Refer to the official ROCOv2 dataset source and its applicable access and licensing conditions. This repository does not redistribute the original dataset unless explicitly permitted.

## Methodology

The framework consists of the following main stages.

### 1. Dataset preparation

- Load radiological images.
- Load corresponding ground-truth captions.
- Prepare the 18 target labels.
- Use the predefined dataset partitions.

### 2. Dual encoding

The image and text inputs are processed using BiomedCLIP:

- Image encoder: BiomedCLIP ViT-B/16
- Text encoder: BiomedCLIP PubMedBERT
- Image embedding dimension: 512
- Text embedding dimension: 512
- L2-normalised embeddings

### 3. Multimodal fusion and classification

The image and text representations are combined into a 1,024-dimensional multimodal representation.

The prediction head uses the following architecture:

- Input dimension: 1,024
- Hidden layer: 256
- Output dimension: 18
- Activation: ReLU
- Dropout: 0.2
- Output activation: Sigmoid

The model uses a two-stage fine-tuning procedure.

### 4. Multi-label prediction

The model produces 18 independent label probabilities. A threshold of 0.5 is used for binary predictions.

### 5. Split conformal prediction

Split conformal prediction is used to examine prediction-set behaviour.

- Calibration is performed using the designated calibration split.
- Label-wise calibration is applied.
- Prediction sets may contain `{0}`, `{1}`, or be empty.
- A Mondrian sensitivity analysis is also considered.

The exact conformity-score and quantile definitions should be consulted in the manuscript's Methods section.

### 6. Latent decision-boundary sensitivity

DeepFool-based perturbations are investigated in the latent representation space.

Reported configuration:

- Maximum steps: 50
- Overshoot: 0.02
- Perturbation space: latent representation
- No projection into image space
- No decoding into an image or caption

These perturbations are interpreted as latent decision-boundary sensitivity analysis, not clinically validated counterfactual explanations.

### 7. Exploratory Composite Trust Score

The study investigates an exploratory composite score combining conformal-set-derived information and latent distance.

This score is exploratory and is not presented as a clinically validated measure of trustworthiness.

## Experimental Results

The multimodal model achieved the following results on the final test split:

| Metric | BiomedCLIP multimodal model |
|---|---:|
| Macro-F1 | 0.8311 |
| Micro-F1 | 0.9285 |
| Macro ROC-AUC | 0.9954 |
| Hamming Loss | 0.0126 |
| Subset Accuracy | 0.8634 |

### Baseline comparison

| Metric | BiomedCLIP multimodal | DenseNet121 |
|---|---:|---:|
| Macro-F1 | 0.8311 | 0.7170 |
| Micro-F1 | 0.9285 | 0.8578 |
| Macro ROC-AUC | 0.9954 | 0.9697 |

### Conformal prediction findings

The marginal coverage was approximately 0.9026. However, positive-class coverage was lower (0.7224), and coverage varied across labels. Therefore, marginal coverage should not be interpreted as a guarantee of reliable positive-label prediction for every class.

### Trust Score findings

The exploratory Composite Trust Score did not demonstrate improved error detection over raw prediction confidence in the reported evaluation.

These results are reported to support transparent assessment rather than to claim a validated trustworthiness improvement.

## Technologies

- Python
- PyTorch
- BiomedCLIP
- Vision Transformers
- PubMedBERT
- Scikit-learn
- NumPy
- Pandas
- Matplotlib
- Google Colab

## Repository Structure

The repository is intended to organise the research materials as follows. Update this structure to match the files actually released.

```text
project/
├── README.md
├── requirements.txt
├── notebooks/
│   └── model_training_and_evaluation.ipynb
├── src/
│   ├── data_preprocessing/
│   ├── model/
│   ├── training/
│   └── evaluation/
├── configs/
├── results/
├── figures/
└── LICENSE
```

## Reproducibility and Data Availability

This repository is intended to provide the research code, experimental configurations, label information, and analysis materials required to understand and reproduce the reported workflow, subject to dataset access restrictions.

The repository contents and availability will be updated by the authors.

**Repository URL:** To be added.

**Dataset:** ROCOv2. Refer to the original dataset source for access and licensing information.

## Limitations

- The evaluation is based on ROCOv2 and does not constitute external clinical validation.
- The classification targets are imaging characteristics, not pathological diagnoses.
- Ground-truth captions are used as model inputs; caption information can contain target-related information.
- Conformal coverage varies across labels, particularly for rare positive classes.
- Latent perturbations are not decoded or clinically validated.
- The Composite Trust Score did not demonstrate an advantage over raw confidence in the reported error-detection evaluation.
- Dataset image reuse and the absence of patient/article-level identifiers limit claims about sample independence.

## Citation

If you use this work, please cite the associated research publication or manuscript.

**Manuscript title:**

*Caption-Assisted Multi-Label Classification of Radiological Imaging Characteristics: Conformal Prediction, Latent Decision-Boundary Sensitivity and an Exploratory Trust Score.*

Full bibliographic details and the publication DOI will be added when available.

## Contact

**Hira Nawaz**  
MS Computer Science Researcher  
University of Gujrat, Pakistan

For research-related questions, please use the contact information provided in the associated publication or GitHub profile.
"""

output_path = "/mnt/data/README.md"
pypandoc.convert_text(readme, "md", format="md", outputfile=output_path, extra_args=["--standalone"])
print(f"Created: {output_path}")
