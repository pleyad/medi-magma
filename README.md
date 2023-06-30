# MAGMA goes Medi: Multimodal Augmentation through Adapter-based Fine-tuning for Radiology Report Generation

### Data processing
The scripts used for data preprocessing are:
* `DATA_combined_prepare.py`
* `DATA_iuxray_pepare.py` 
* `DATA_mimix_prepare.py`

### Training
The training of the two training experiment are were done with the following:
*`train.py`
Configs for 1. Training: `configs/MAGMA_medi_biomedlm_mimic.yml`
Configs for 2. Training: `configs/MAGMA_medi_biomedlm_mimic.ym`

### Inference
Script used:
* `medimagma_inference.py`

### Evaluation
Scripts used:
* `preprocess_predictions.py`
* `all_timesteps_evaluate.py`

### Plots
All materials and code can be found in the `plots/` folder.
