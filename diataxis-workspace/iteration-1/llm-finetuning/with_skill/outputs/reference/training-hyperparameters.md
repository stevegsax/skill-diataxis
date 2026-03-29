# Training Hyperparameters Reference

## LoraConfig Parameters

| Parameter | Type | Default | Description | Typical Range |
|-----------|------|---------|-------------|---------------|
| `r` | int | 8 | LoRA rank (dimension of the low-rank matrices) | 4-64 |
| `lora_alpha` | int | 8 | Scaling factor for LoRA weights | Usually 2*r |
| `lora_dropout` | float | 0.0 | Dropout probability for LoRA layers | 0.0-0.1 |
| `target_modules` | list[str] | None | Which model modules to apply LoRA to | See architecture table below |
| `bias` | str | "none" | Whether to train bias parameters ("none", "all", "lora_only") | "none" |
| `task_type` | str | None | Task type ("CAUSAL_LM", "SEQ_2_SEQ_LM", etc.) | "CAUSAL_LM" for decoder models |
| `modules_to_save` | list[str] | None | Additional modules to train fully (not LoRA) | embed_tokens, lm_head |

## BitsAndBytesConfig Parameters (4-bit Quantization)

| Parameter | Type | Default | Description | Recommended |
|-----------|------|---------|-------------|-------------|
| `load_in_4bit` | bool | False | Enable 4-bit quantization | True for QLoRA |
| `bnb_4bit_quant_type` | str | "fp4" | Quantization data type | "nf4" (normalized float 4) |
| `bnb_4bit_compute_dtype` | torch.dtype | torch.float32 | Compute dtype for 4-bit operations | torch.bfloat16 |
| `bnb_4bit_use_double_quant` | bool | False | Quantize the quantization constants | True (saves ~0.4 GB per 1B params) |

## BitsAndBytesConfig Parameters (8-bit Quantization)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `load_in_8bit` | bool | False | Enable 8-bit quantization |
| `llm_int8_threshold` | float | 6.0 | Outlier detection threshold |
| `llm_int8_has_fp16_weight` | bool | False | Keep fp16 copy for mixed precision |

## TrainingArguments Parameters (Fine-Tuning Relevant)

| Parameter | Type | Default | Description | Typical Range |
|-----------|------|---------|-------------|---------------|
| `output_dir` | str | required | Directory for checkpoints and logs | "./results" |
| `num_train_epochs` | float | 3.0 | Number of training epochs | 1-5 for fine-tuning |
| `per_device_train_batch_size` | int | 8 | Batch size per GPU | 1-8 (VRAM dependent) |
| `per_device_eval_batch_size` | int | 8 | Eval batch size per GPU | Same or larger than train |
| `gradient_accumulation_steps` | int | 1 | Steps before optimizer update | 1-16 |
| `learning_rate` | float | 5e-5 | Peak learning rate | 1e-5 to 3e-4 for QLoRA |
| `weight_decay` | float | 0.0 | L2 regularization | 0.0-0.1 |
| `warmup_ratio` | float | 0.0 | Fraction of steps for LR warmup | 0.03-0.1 |
| `warmup_steps` | int | 0 | Absolute warmup steps (overrides ratio) | 10-100 |
| `lr_scheduler_type` | str | "linear" | Learning rate schedule | "cosine", "linear" |
| `logging_steps` | int | 500 | Log every N steps | 10-50 |
| `save_strategy` | str | "steps" | When to save checkpoints | "steps", "epoch" |
| `save_steps` | int | 500 | Save every N steps | 100-500 |
| `eval_strategy` | str | "no" | When to evaluate | "steps", "epoch" |
| `eval_steps` | int | None | Evaluate every N steps | 50-200 |
| `bf16` | bool | False | Use bfloat16 precision | True (if GPU supports) |
| `fp16` | bool | False | Use float16 precision | True (if bf16 unavailable) |
| `optim` | str | "adamw_torch" | Optimizer | "paged_adamw_8bit" |
| `gradient_checkpointing` | bool | False | Trade compute for memory | True for large models |
| `max_grad_norm` | float | 1.0 | Gradient clipping norm | 0.3-1.0 |
| `report_to` | str | "all" | Logging integrations | "none", "wandb", "tensorboard" |
| `seed` | int | 42 | Random seed | Any integer |
| `dataloader_num_workers` | int | 0 | Data loading workers | 0-4 |

## SFTTrainer Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | PreTrainedModel | required | The model to fine-tune |
| `args` | TrainingArguments | required | Training configuration |
| `train_dataset` | Dataset | required | Training data |
| `eval_dataset` | Dataset | None | Validation data |
| `processing_class` | PreTrainedTokenizer | None | Tokenizer |
| `max_seq_length` | int | 1024 | Maximum sequence length |
| `packing` | bool | False | Pack multiple examples per sequence |
| `dataset_text_field` | str | None | Column containing formatted text |
| `dataset_kwargs` | dict | None | Additional dataset arguments |

## Effective Batch Size Calculation

```
effective_batch_size = per_device_train_batch_size * gradient_accumulation_steps * num_gpus
```

## Steps Per Epoch Calculation

```
steps_per_epoch = num_training_examples / effective_batch_size
```

## Target Modules by Architecture

| Model Family | Attention Modules | MLP Modules |
|-------------|-------------------|-------------|
| Llama 3.x, Mistral, Gemma | q_proj, k_proj, v_proj, o_proj | gate_proj, up_proj, down_proj |
| Phi-3 | qkv_proj, o_proj | gate_up_proj, down_proj |
| Qwen 2.5 | q_proj, k_proj, v_proj, o_proj | gate_proj, up_proj, down_proj |

For guidance on tuning these parameters, see [How to Tune Hyperparameters](../howto/tune-hyperparameters.md). For background on why LoRA uses these parameters, see [How LoRA Works](../explanation/how-lora-works.md).
