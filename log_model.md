### GPT-2 config
GPT2Config {
  "_name_or_path": "stanford-crfm/BioMedLM",
  "activation_function": "gelu_new",
  "architectures": [
    "GPT2LMHeadModel"
  ],
  "attn_pdrop": 0.1,
  "bos_token_id": 28895,
  "embd_pdrop": 0.1,
  "eos_token_id": 28895,
  "gradient_checkpointing": false,
  "initializer_range": 0.02,
  "layer_norm_epsilon": 1e-05,
  "model_type": "gpt2",
  "n_ctx": 1024,
  "n_embd": 2560,
  "n_head": 20,
  "n_inner": null,
  "n_layer": 32,
  "n_positions": 1024,
  "pad_token_id": 28895,
  "reorder_and_upcast_attn": false,
  "resid_pdrop": 0.1,
  "scale_attn_by_inverse_layer_idx": true,
  "scale_attn_weights": true,
  "summary_activation": null,
  "summary_first_dropout": 0.1,
  "summary_proj_to_labels": true,
  "summary_type": "cls_index",
  "summary_use_proj": true,
  "task_specific_params": {
    "text-generation": {
      "do_sample": true,
      "max_length": 50
    }
  },
  "torch_dtype": "float32",
  "transformers_version": "4.6.0.dev0",
  "use_cache": false,
  "vocab_size": 28896
}

### BERT Config
DistilBertConfig {
  "_name_or_path": "medicalai/ClinicalBERT",
  "activation": "gelu",
  "architectures": [
    "DistilBertForMaskedLM"
  ],
  "attention_dropout": 0.1,
  "dim": 768,
  "dropout": 0.1,
  "hidden_dim": 3072,
  "initializer_range": 0.02,
  "max_position_embeddings": 512,
  "model_type": "distilbert",
  "n_heads": 12,
  "n_layers": 6,
  "output_past": true,
  "pad_token_id": null,
  "qa_dropout": 0.1,
  "seq_classif_dropout": 0.2,
  "sinusoidal_pos_embds": false,
  "tie_weights_": true,
  "transformers_version": "4.6.0.dev0",
  "vocab_size": 119547
}

Masked Language Model
- has access to token left to right

### GPT-j config
GPTNeoConfig {
  "activation_function": "gelu_new",
  "architectures": [
    "GPTNeoForCausalLM"
  ],
  "attention_dropout": 0,
  "attention_layers": [
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global",
    "global"
  ],
  "attention_types": [
    [
      "global"
    ],
    28
  ],
  "bos_token_id": 50256,
  "embed_dropout": 0,
  "eos_token_id": 50256,
  "full_bf16": false,
  "gradient_checkpointing": true,
  "hidden_size": 4096,
  "initializer_range": 0.02,
  "intermediate_size": null,
  "jax": true,
  "layer_norm_epsilon": 1e-05,
  "max_position_embeddings": 2048,
  "model_device": null,
  "model_dtype": "fp16",
  "model_type": "gpt_neo",
  "num_heads": 16,
  "num_layers": 28,
  "resid_dropout": 0,
  "rotary": true,
  "rotary_dim": 64,
  "summary_activation": null,
  "summary_first_dropout": 0.1,
  "summary_proj_to_labels": true,
  "summary_type": "cls_index",
  "summary_use_proj": true,
  "task_specific_params": {
    "text-generation": {
      "do_sample": true,
      "max_length": 50,
      "temperature": 0.9
    }
  },
  "tokenizer_class": "GPT2Tokenizer",
  "transformers_version": "4.6.0.dev0",
  "use_cache": true,
  "vocab_size": 50400,
  "window_size": 256
}


self.transformer = self.lm.transformer.h


Causal Language Model:
- can only see token to left 