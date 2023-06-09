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
[ ] as of 01.06: Learning rate scheduler accessed before defined --> probably reason for weird loss curve
[ ] as of 09.06: RuntimeError: cuDNN error: CUDNN_STATUS_NOT_INITIALIZED
