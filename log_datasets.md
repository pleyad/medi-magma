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

29.04: I am currently downloading it to rattle, into `/srv/scratch1/bodenmann/mimic-cxr`.

### MS-CXR

- paper: https://arxiv.org/pdf/2204.09817.pdf
- info: https://physionet.org/content/ms-cxr/0.1/
- **task**: phrase grounding? <-- well-balanced phrase grounding benchmark dataset, locally-aligned
- goal: reproducible evaluation of joint latent semantics learnt by biomedical image-text models
- structure:
    - Categories: List of conditions/pathologies
    - Images: Metadata of the original chest X-ray images. The images need to be separately downloaded from MIMIC-CXR / MIMIC-CXR-JPG projects.
    - Annotations: Each entry represents a bounding box with an associated sentence describing a condition/pathology. Images may have multiple associated annotations.
- size: 1162 image–sentence pairs of bounding boxes and corresponding phrases
- (!) complements the existing MIMIC-CXR v.2 dataset and comprises: 
    - Reviewed and edited bounding boxes and phrases (1026 pairs of bounding box/sentence);
    - Manual bounding box labels from scratch (136 pairs of bounding box/sentence)
- (!) **How does it extend MIMIC? Duplicates?** --> (HH) the paper claims it merely complements MIMIC, but it increasingly seems that MS-CXR is in fact a subset of MIMIC images. 
    (a) "The images need to be separately downloaded from MIMIC-CXR / MIMIC-CXR-JPG projects". <-- !
    (b) the authors parse original MIMIC reports and extract text descriptions from a subset of MIMIC

- Available on [Physionet](https://physionet.org/content/ms-cxr/0.1/). To access it, you need to register on Physionet and then request access to the dataset.

### VinDr-CXR

- paper: https://physionet.org/content/vindr-cxr/1.0.0/
- labels: bounding boxes and class labels in a CSV file:
    - local: 22 critical findings - each localized with a bounding box = “Findings” 
    - global: 6 diagnoses = “Impressions”
- localization: only text → "sequence of unique anatomical locations is always preceded by the token “loc”"
- Image Format: **DICOM**: Python library to read DICOM files: [pydicom](https://pydicom.github.io/).
- **Task**: Bounding box detection and labelling (14 classes)
- ⚠️ No report generation
- goal: developing and evaluating algorithms for detecting and localizing anomalies in CXR scans
- size: The published dataset consists of 18,000 postero-anterior (PA) view CXR scans with both the localization of critical findings and the classification of common thoracic diseases. 
- 15,000 train, 3,000 test → both manually annotated
- has bounding-box annotations but lacks free-text descriptions

- [Dataset website](https://vindr.ai/datasets/cxr).
    The dataset is available on [Kaggle](https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/data).https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/. The size of the the dataset is 206 GB, but it is freely available.
- In this [notebook](https://www.kaggle.com/code/theolange/ai-vinbigdata-visualisation), the author shows how to load and explore the dataset.
- and here are some projects based on the dataset: https://www.kaggle.com/competitions/vinbigdata-chest-xray-abnormalities-detection/overview

### PadChest
- paper: https://www.sciencedirect.com/science/article/abs/pii/S1361841520301614?via%3Dihub
- Dataset website: [PadChest](https://bimcv.cipf.es/bimcv-projects/padchest/).
- subset: A subset of the dataset is available on [Kaggle](https://www.kaggle.com/datasets/raddar/padchest-chest-xrays-sample). The full dataset is 1.02 TB, but two small samples (167 MB, 1.2 GB) are availabe.
- The data consists of 160'000 X-ray images from 67,000 patients with accompanying reports in Spanish.
- labels: 174 different radiographic findings, 19 differential diagnoses and 104 anatomic locations organized as a hierarchical taxonomy and mapped onto standard Unified Medical Language System (UMLS) terminology
- ground truth: manual labeling by trained physicians (27% of the images); 73% by a ML model
- language: Although the excerpts from the report are provided in Spanish, the labels are mapped onto biomedical vocabulary unique identifier (CUIs) codes, thus making the dataset usable regardless of the language

- ❓ I am unsure whether multiple images from different angles are connected to one report. (NB) --> - (HH) Yes, they are, according to the original paper. Look: 
    - "Each study contains **one or more images** corresponding to different position views, mainly P-A and lateral, and is associated with a **single radiography report** describing the results of all position views in a common text."

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
