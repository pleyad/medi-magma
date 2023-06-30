from magma import Magma
from magma.datasets import (
    ImgCptDataset,
)
from magma.utils import (
    cycle,
)
from magma.image_input import ImageInput

import os
import subprocess
import csv
from tqdm import tqdm

CONFIG_PATH = 'configs/MAGMA_medi_biomedlm_mimic_x-iu.yml'
CHECKPOINT_PATH = 'checkpoints/medimagma_mimic_iu'
MODEL_PATH = 'model/medimagma_mimic_iu'
PREDICTION_PATH = 'predictions/medimagma_mimic_iu'
TEST_DATA_PATH = '/srv/scratch1/nbodenmann/prepared_mimic-cxr/test_with_study_id'
WEIGHT_EXTRACTION = os.path.join(CHECKPOINT_PATH, 'zero_to_fp32.py')
GPU = 'cuda:5'

if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH, exist_ok=True)
if not os.path.exists(PREDICTION_PATH):
    os.makedirs(PREDICTION_PATH, exist_ok=True)


current_model_tag = None

for root, dirs, files in os.walk(CHECKPOINT_PATH):
    for folder in dirs:
        if folder.startswith('global_step'):
            folder_path = os.path.join(root, folder)
            current_model_tag = folder
            print(f'Starting prediction for {current_model_tag}\n----------------------')
       
            model_name = f'{current_model_tag}_model.bin'
            model_path = os.path.join(MODEL_PATH, model_name)
            
            # Extract fp32 weights from zero stage 3 output (checkpoint per rank)
            # Use zero_to_fp32.py in the same directory as all step folders
            
            if not os.path.exists(model_path):
                print("Extracting fp32 weights...")
                command = ['python3', WEIGHT_EXTRACTION, CHECKPOINT_PATH, model_path, current_model_tag]
                
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                # Wait for the process to finish and capture the output
                output, error = process.communicate()

                # Print the output and error
                print(output)
                print(error)
            
            model = Magma.from_checkpoint(
                config_path = CONFIG_PATH,
                checkpoint_path = model_path,
                device = GPU
            )

            tokenizer, config, transforms = model.tokenizer, model.config, model.transforms
            test_data = ImgCptDataset(TEST_DATA_PATH, tokenizer, transforms, config.prompt)
            print(f"Loaded test dataset with {len(test_data)} samples")
            
            prediction_csv = os.path.join(PREDICTION_PATH, f'predictions_{current_model_tag}.csv')
            gold_csv = os.path.join(PREDICTION_PATH, f'gold_{current_model_tag}.csv')
            
            if os.path.exists(prediction_csv) and os.path.exists(gold_csv):
                os.remove(prediction_csv)
                os.remove(gold_csv)

            with open(gold_csv, 'a') as gold, open(prediction_csv, 'a') as pred:
                gold_writer = csv.writer(gold, delimiter=";")
                pred_writer = csv.writer(pred, delimiter=";")
                header = ['id', 'mimic_study_id', 'report', 'img_path']
                gold_writer.writerow(header)
                pred_writer.writerow(header)
                id = 0
                for id in tqdm(range(len(test_data)), desc=f"Prection {current_model_tag}"):
                    # Gold Data
                    study_id = test_data.data[id]['metadata']['study_id']
                    report_gold = test_data.data[id]['caption']
                    img_path = test_data.data[id]['image_path']
                    gold_row = [id, study_id, report_gold, img_path]
                    gold_writer.writerow(gold_row)
                    inputs = [
                        ImageInput(os.path.join(test_data.data_dir, img_path)),
                        test_data.prompt]
                    embeddings = model.preprocess_inputs(inputs)
                    try:
                        output = model.generate(
                            embeddings = embeddings,
                            max_steps = 100,
                            temperature = 0.7,
                            top_k = 0,
                            single_gpu = True,
                            progress_bar = False,
                        ) 
                        report_pred = output[0]
                    except RuntimeError as e:
                        print(e)
                        report_pred = "ERROR"
                    pred_row = [id, study_id, report_pred, img_path]
                    pred_writer.writerow(pred_row)
                    
                    # Directly write to file, don't store in buffer
                    gold.flush()
                    pred.flush()

                    id +=1

            os.remove(model_path)
            del model
