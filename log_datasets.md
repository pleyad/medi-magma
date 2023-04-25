# Log for datasets

## Datasets

### IU-XRAY

Mentioned in [R2Gen-Repo](https://github.com/cuhksz-nlp/R2Gen#datasets), with a link to the [zipped dataset](https://drive.google.com/file/d/1c0BXEuDy8Cmm2jfN0YYGkQxFZd2ZIoLg/view).
I downloaded it (NB).

### MIMIC-CXR

Also mentioned in [R2Gen-Repo](https://github.com/cuhksz-nlp/R2Gen#datasets), with a link to the [dataset](https://drive.google.com/file/d/1DS6NYirOXQf8qYieSVMvqNwuOlgAbM_E/view?usp=sharing).
However, here you need to demand access.
It is also avaible on physionet.
I (NB) have approval now but still need to check how to make it available, as it is 4.5 TB.

### MS-CXR

Available on [Physionet](https://physionet.org/content/ms-cxr/0.1/).
To access it, you need to register on Physionet and then request access to the dataset.

The overview mentions how this dataset extends MIMIC-CXR.

- [ ] How does it extend it? Do we need to worry about duplicates?

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