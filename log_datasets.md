# Log for datasets

## Datasets

### IU-XRAY (Indiana University Chest X-ray Collection)

- paper: none
- Mentioned in [R2Gen-Repo](https://github.com/cuhksz-nlp/R2Gen#datasets), with a link to the [zipped dataset](https://drive.google.com/file/d/1c0BXEuDy8Cmm2jfN0YYGkQxFZd2ZIoLg/view).
- example project based on the dataset: https://rohansoni-jssaten2019.medium.com/indiana-university-chest-x-rays-automated-report-generation-38f928e6bfc2
- image(s): usually frontal and lateral
- report structure: 
    - "id", 
    - "report" (unstructured), 
    - "image_path", 
    - "split" (test or train)


### MIMIC-CXR 2.0.0

- paper: https://physionet.org/content/mimic-cxr/2.0.0/
- info: https://mimic.mit.edu/docs/iv/modules/cxr/
- repo (sample projects): https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv-cxr/notebooks
- structure: 
    - subject_id (patient)
    - study_id (report)
    - dicom_id (image(s))
- size: 227,835 imaging studies for 64,588 patients
- images: usually 2 images per patient: frontal and lateral view
- A records file, cxr-record-list.csv.gz, provides a mapping between the image (dicom_id), the study (study_id), and the patient (subject_id). Another records file, cxr-study-list.csv.gz, provides a mapping between the studies (study_id) and patients (subject_id).
- report type: semi-structured (but "findings" and "impressions" present)

- Also mentioned in [R2Gen-Repo](https://github.com/cuhksz-nlp/R2Gen#datasets), with a link to the [dataset](https://drive.google.com/file/d/1DS6NYirOXQf8qYieSVMvqNwuOlgAbM_E/view?usp=sharing).
- However, here one needs to demand access. I (NB) have approval now but still need to check how to make it available, as it is 4.5 TB.

### MS-CXR

- paper: https://arxiv.org/pdf/2204.09817.pdf
- info: Making the Most of Text Semantics to Improve Biomedical Vision-Language Processing
- task: phrase grounding? <-- well-balanced phrase grounding benchmark dataset, locally-aligned
- goal: reproducible evaluation of joint latent semantics learnt by biomedical image-text models
- structure:
    - Categories: List of conditions/pathologies
    - Images: Metadata of the original chest X-ray images. The images need to be separately downloaded from MIMIC-CXR / MIMIC-CXR-JPG projects.
    - Annotations: Each entry represents a bounding box with an associated sentence describing a condition/pathology. Images may have multiple associated annotations.
- size: 1162 image–sentence pairs of bounding boxes and corresponding phrases
- (!) complements the existing MIMIC-CXR v.2 dataset and comprises: 
    - Reviewed and edited bounding boxes and phrases (1026 pairs of bounding box/sentence);
    - Manual bounding box labels from scratch (136 pairs of bounding box/sentence)
- (!) How does it extend MIMIC? Duplicates? --> (HH) the paper claims it merely complements MIMIC, but it increasingly seems that MS-CXR is in fact a subset of MIMIC images. 
    (a) "The images need to be separately downloaded from MIMIC-CXR / MIMIC-CXR-JPG projects". <-- !
    (b) the authors parse original MIMIC reports and extract text descriptions from a subset of MIMIC

- Available on [Physionet](https://physionet.org/content/ms-cxr/0.1/). To access it, you need to register on Physionet and then request access to the dataset.

### VinDr-CXR

[Dataset website](https://vindr.ai/datasets/cxr).
The dataset is available on [Kaggle](https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/data).https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/.
The size of the the dataset is 206 GB, but it is freely available.
In this [notebook](https://www.kaggle.com/code/theolange/ai-vinbigdata-visualisation), the author shows how to load and explore the dataset.

**Task**: Bounding box detection and labelling (14 classes).
⚠️ No report generation.

#### Format: **DICOM**

Images are in DICOM format.
There is a Python library to read DICOM files: [pydicom](https://pydicom.github.io/).

Labels are bounding boxes and class labels in a CSV file.

### PadChest

Dataset website: [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/).
A subset of the dataset is available on [Kaggle](https://www.kaggle.com/datasets/raddar/padchest-chest-xrays-sample).
The data consists of 160'000 X-ray images with accompanying reports in Spanish.

❓ I am unsure whether multiple images from different angles are connected to one report. (NB)

The reports are mapped to the Unified Medical Language System (UMLS) (172 different radiographic findings), but only 27% by human annotators, the rest was done by a machine learning model.

The full dataset is 1.02 TB, but two small samples (167 MB, 1.2 GB) are availabe.

## Log Datasets Magma

Ablation study:  CC12M (Conceptual 12M) - Image Captioning

Training: 
- LAION (Schuhmann et al., 2021)
- Wikipedia Image-Text (Srinivasan et al., 2021)
- CC3M (Changpinyo et al.,2021b)
- Visual Genome (Krishna et al., 2016)
- Localized Narratives (Pont-Tuset et al., 2020)
- VQA (Antol et al., 2015)
- GQA (Hudson andManning, 2019)
- OKVQA (Marino et al., 2019),
- VizWiz (Gurari et al., 2018)
- Hateful Memes (Kiela
et al., 2020)
- CoCo Captions (Chen et al., 2015).

--> 25 million image-text pairs to train our final mode

## Log

### 2023-04-10

NB: Farhad mentioned in person and in emails five different datasets, they are listed above.
