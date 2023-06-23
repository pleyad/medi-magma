from dataclasses import dataclass, asdict
import yaml
from pprint import pprint
from .utils import is_main
import os
from pathlib import Path
import uuid


def load_config(path, config_dir=Path("configs")):
    if not path.endswith(".yml"):
        path += ".yml"
    if not os.path.exists(path):
        path = config_dir / path
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    return config


@dataclass
class MultimodalConfig:

    # Training:
    # ------------------------------------------------------------

    batch_size: int
    train_steps: int
    optimizer_name: str = "AdamW"
    lr: float = 8.0e-4
    image_enc_lr: float = None
    min_lr: float = 0.0
    lr_decay_iters: int = None
    gradient_accumulation_steps: int = 1
    image_size: int = 256
    eval_every: int = 250
    eval_steps: int = 25
    zero_stage: int = 2
    gradient_clipping: float = 1.0
    warmup_num_steps: int = 100
    weight_decay: float = 0.00
    run_blind: bool = False
    fine_tune: bool = False
    load_optimizer: bool = True
    prompt: str = ''

    # Checkpointing:
    # ------------------------------------------------------------
    save_every: int = 2500
    save: str = None
    load: str = None

    # Data:
    # ------------------------------------------------------------
    train_dataset_name: str = "conceptual_captions"
    eval_dataset_name: str = None
    train_dataset_dir: str = "/data/coco_data"
    eval_dataset_dir: str = None
    eval_dataset_pct: float = 0.1

    # Model architecture:
    # ------------------------------------------------------------
    encoder_name: str = "clip"
    tokenizer_name: str = "gpt2"
    lm_name: str = "EleutherAI/gpt-j-6B"
    image_seq_len: int = 2
    pretrained_img_encoder: bool = False
    seq_len: int = None

    # Layer Freezing settings:
    # ------------------------------------------------------------
    freeze_lm: bool = True
    freeze_img_encoder: bool = True

    image_embed_dropout_prob: float = 0.0
    use_image_embed_layernorm: bool = False

    # Adapter settings:
    # ------------------------------------------------------------
    adapter_config: dict = None

    # Classification Finetuning settings:
    # ------------------------------------------------------------
    class_dict: dict = None  # {num_classes: .., ckpt_path: .., classifier_type:, .., interface_type: .., interface_position: .., freeze_model: ..}

    # Logging settings:
    # ------------------------------------------------------------
    name: str = None  # name, just used for wandb logging
    log_every: int = 1
    wandb_project: str = "magma"

    def print(self):
        if is_main():
            print("-" * 100)
            pprint(self.__dict__, indent=4)
            print("-" * 100)

    def __post_init__(self):
        self.is_classifier = self.class_dict is not None
        if self.adapter_config is None:
            self.adapter_config = {}

        # Deepspeed Settings:
        # ------------------------------------------------------------
        if self.lr_decay_iters is None:
            self.lr_scheduler = "WarmupLR"
            self.scheduler_dict = {
                "type": self.lr_scheduler,
                "params": {
                    "warmup_min_lr": self.min_lr,
                    "warmup_max_lr": self.lr,
                    "warmup_num_steps": self.warmup_num_steps,
                },
            }
        else:
            self.lr_scheduler = "WarmupDecayLR"
            self.scheduler_dict = {
                "type": self.lr_scheduler,
                "params": {
                    "total_num_steps": self.lr_decay_iters,
                    "warmup_min_lr": self.min_lr,
                    "warmup_max_lr": self.lr,
                    "warmup_num_steps": self.warmup_num_steps,
                },
            }
        self.deepspeed_config_params = {
            "train_batch_size": self.batch_size,
            "gradient_accumulation_steps": self.gradient_accumulation_steps,
            "gradient_clipping": self.gradient_clipping,
            "bf16": {"enabled": True, "loss_scale_window": 250},
            "scheduler": self.scheduler_dict,
            "zero_optimization": {
                "stage": self.zero_stage,
                "load_from_fp32_weights": False,
                 "offload_optimizer": {
                    "device": "cpu",
                    "pin_memory": True
                },
                "offload_param": {
                    "device": "cpu",
                    "pin_memory": True
                },
                "overlap_comm": True,
                "contiguous_gradients": True,
                "sub_group_size": 1e9,
                "reduce_bucket_size": "auto",
                "stage3_prefetch_bucket_size": "auto",
                "stage3_param_persistence_threshold": "auto",
                "stage3_max_live_parameters": 1e9,
                "stage3_max_reuse_distance": 1e9,
                "stage3_gather_16bit_weights_on_model_save": True
            },
            "zero_force_ds_cpu_optimizer": False,
        }
        

        if self.name is None:
            self.name = str(uuid.uuid4())[:8]

    @classmethod
    def from_yml(cls, path):
        return cls(**load_config(path))

    def to_dict(self):
        return asdict(self)
