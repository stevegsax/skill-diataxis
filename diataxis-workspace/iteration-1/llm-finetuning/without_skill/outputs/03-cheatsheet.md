# LLM Fine-Tuning Quick Reference

## Setup (One-Time)

```bash
python -m venv llm-finetune && source llm-finetune/bin/activate
pip install unsloth
nvidia-smi  # Verify GPU
```

## Dataset Format (Alpaca)

```json
[{"instruction": "...", "input": "", "output": "..."}]
```

## Minimal Training Script

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Meta-Llama-3.1-8B-bnb-4bit", max_seq_length=2048, load_in_4bit=True)

model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16, lora_dropout=0,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    use_gradient_checkpointing="unsloth")

dataset = load_dataset("json", data_files="data.json", split="train")
dataset = dataset.map(lambda ex: {"text": tokenizer.apply_chat_template(
    [{"role":"user","content":ex["instruction"]},{"role":"assistant","content":ex["output"]}],
    tokenize=False)})

SFTTrainer(model=model, tokenizer=tokenizer, train_dataset=dataset,
    dataset_text_field="text", max_seq_length=2048,
    args=TrainingArguments(per_device_train_batch_size=2, gradient_accumulation_steps=4,
        num_train_epochs=3, learning_rate=2e-4, output_dir="./checkpoints",
        bf16=torch.cuda.is_bf16_supported(), optim="adamw_8bit")).train()

model.save_pretrained_gguf("./output", tokenizer, quantization_method="q4_k_m")
```

## Default Hyperparameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| LoRA rank (r) | 16 | Increase for complex tasks |
| lora_alpha | 16 | Usually same as r |
| learning_rate | 2e-4 | Reduce to 1e-4 if unstable |
| batch_size | 2 | Reduce to 1 if OOM |
| grad_accum_steps | 4 | Effective batch = batch * this |
| epochs | 1-3 | 1 for large datasets |
| max_seq_length | 2048 | Increase if data has long sequences |

## Model Selection by VRAM

| VRAM | Model |
|------|-------|
| 6 GB | Llama 3.2 3B, Phi-3 Mini |
| 10 GB | Llama 3.1 8B, Mistral 7B, Qwen 2.5 7B |
| 16 GB | Gemma 2 9B, Llama 3.1 8B (higher rank) |
| 24 GB | Llama 3.1 70B (QLoRA) |

## Export and Deploy

```bash
# Create Ollama Modelfile
echo 'FROM ./output/unsloth.Q4_K_M.gguf' > Modelfile
ollama create my-model -f Modelfile
ollama run my-model "test prompt"
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| CUDA OOM | batch_size=1, lower r, lower max_seq_length |
| Loss not decreasing | Higher learning_rate, check data format |
| Overfitting | Fewer epochs, more data, lower r |
| Gibberish output | Check chat template, verify data quality |
