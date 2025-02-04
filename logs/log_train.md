# Training Magma


### Run Training
* check config file `configs/MAGMA_medi_biomedlm`
    * Adjust data path `train_dataset_dir`
    * Adjust checkpoint path (where to save model parameters) `checkpoint_path`
    * Adjust any other parameter as needed (`batch_size`, `train_steps`)

* check with nvidia which GPUs are available
`watch -n1 nvidia-smi`

* add free GPU ideas after `localhost`
```bash
deepspeed --include localhost:5,6,7 train.py --config MAGMA_medi_biomedlm.yml

```

### Debug Training
* use launch.json to use vscode debugger
* adjust path to your setup
* I recommend using one GPU only for debugging, check as well if GPU is even available (s. `localhost: xy` in cofig)
```json
"args": [
                "--include",
                "localhost:7",
                "${workspaceFolder}/medi-magma/train.py",
                "--config",
                "MAGMA_medi_biomedlm.yml"                                                    
            ],
```

### Current issues
[x] as of 01.06: Learning rate scheduler accessed before defined --> probably reason for weird loss curve
[x] as of 09.06: RuntimeError: cuDNN error: CUDNN_STATUS_NOT_INITIALIZED


### First full mimix CXR training - some facts
* 3 GPUs
* Number of training/evaluation samples:
train: 202922
eval: 1654 
* Batch size: 24
* Number of samples the model has seen: 24*2400 = 57600 (28% of all data)
* Number of training steps: 2400
* Training time for training step: 55.69s
* Inference time for one example: 3 minutes
* Total training time: 42h 43 minute 
* Checkpoints saved every 100 training steps
* Eval every 50
* Checkpoint with lowest eval: 1250 but not saved only eval -> 1000 best?

## Full mimic and x-iu data (alternately)
* 6 GPUS
* Number of training/evaluation samples:
train: 210970 samples
eval: 1654 samples
* Batch size: 56
* Number of samples the model has seen: 56*1700 = 95200 (45% of all data)
* Number of training steps: 1700
* Total training time: ~ 100h
* Checkpoints saved every 100 training steps
* Eval every 50
