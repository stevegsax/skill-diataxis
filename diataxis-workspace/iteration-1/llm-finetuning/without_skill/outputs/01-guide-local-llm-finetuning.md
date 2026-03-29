# Fine-Tuning LLMs on Your Local Computer

This guide walks you through fine-tuning a large language model on consumer hardware using QLoRA and Unsloth. It covers hardware assessment, dataset preparation, model selection, training, evaluation, and deployment.

## Prerequisites

- Python 3.11+
- An NVIDIA GPU with at least 8 GB VRAM (e.g., RTX 3060 12GB, RTX 4060 Ti 16GB, RTX 4070 Ti 12GB)
- CUDA 12.x installed
- Basic familiarity with Python and the command line

If you have an Apple Silicon Mac, you can fine-tune smaller models (1-3B) using MLX. This guide focuses on the NVIDIA/CUDA path, which is the most mature ecosystem.

## 1. Understand What Fine-Tuning Is

Fine-tuning takes a pre-trained base model and further trains it on your specific data. This teaches the model to follow a particular style, answer domain-specific questions, or perform a specialized task -- without training from scratch.

**Full fine-tuning** updates every parameter in the model. For a 7B model, this requires roughly 112 GB of VRAM (16 bytes per parameter with Adam optimizer states). This is impractical on consumer hardware.

**LoRA (Low-Rank Adaptation)** freezes the base model and injects small trainable matrices into attention layers. Only these adapters are trained, reducing trainable parameters by 90%+ and VRAM by 5-6x.

**QLoRA** goes further: the frozen base model is loaded in 4-bit quantized precision, while the LoRA adapters train in higher precision (bfloat16). This pushes a 7B fine-tune down to 8-12 GB VRAM.

## 2. Hardware Requirements

| Model Size | Method | Minimum VRAM | Recommended GPU |
|------------|--------|-------------|-----------------|
| 1-3B | QLoRA | 4-6 GB | RTX 3060 (12GB) |
| 7-8B | QLoRA | 8-12 GB | RTX 4070 Ti (12GB) |
| 13B | QLoRA | 12-16 GB | RTX 4060 Ti (16GB) |
| 30-70B | QLoRA | 16-24 GB | RTX 4090 (24GB) |

Beyond VRAM, you need:

- **RAM**: At least 32 GB system RAM (64 GB preferred for larger models)
- **Storage**: 50-100 GB free for model weights, datasets, and checkpoints
- **CPU**: A modern multi-core CPU (the GPU does the heavy lifting, but data loading uses CPU)

### Check Your Hardware

```bash
# Check NVIDIA GPU and VRAM
nvidia-smi

# Check system RAM
free -h  # Linux
sysctl hw.memsize  # macOS
```

## 3. Environment Setup

```bash
# Create a virtual environment
python -m venv llm-finetune
source llm-finetune/bin/activate

# Install Unsloth (handles PyTorch, transformers, etc.)
pip install unsloth

# Verify CUDA is available
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}'); print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB')"
```

Unsloth is a drop-in optimization layer on top of Hugging Face Transformers and TRL. It provides 2x faster training and 60% less memory usage compared to vanilla implementations, with no changes to your training code.

## 4. Dataset Preparation

Your dataset is the single most important factor in fine-tuning quality. Poor data produces a poor model regardless of hyperparameters.

### Dataset Formats

There are two standard formats:

**Alpaca format** -- for single-turn instruction following:

```json
[
  {
    "instruction": "Summarize the following legal clause.",
    "input": "The party of the first part shall indemnify...",
    "output": "This clause requires Party A to cover Party B's legal costs..."
  },
  {
    "instruction": "What is the capital of France?",
    "input": "",
    "output": "The capital of France is Paris."
  }
]
```

**ShareGPT format** -- for multi-turn conversations:

```json
[
  {
    "conversations": [
      {"from": "human", "value": "What causes rain?"},
      {"from": "gpt", "value": "Rain forms when water vapor in the atmosphere condenses..."},
      {"from": "human", "value": "How does that differ from snow?"},
      {"from": "gpt", "value": "Snow forms when the temperature is below freezing..."}
    ]
  }
]
```

### Dataset Size Guidelines

- **50-200 examples**: Enough for style/format changes (e.g., "always respond in bullet points")
- **500-2,000 examples**: Good for teaching domain knowledge or task-specific behavior
- **5,000-50,000 examples**: Comprehensive fine-tuning for complex tasks
- **Quality over quantity**: 500 high-quality examples often outperform 5,000 noisy ones

### Dataset Quality Checklist

- Every example demonstrates the exact behavior you want
- Responses are accurate, well-formatted, and complete
- No contradictions between examples
- Diverse inputs covering edge cases
- Consistent formatting across all examples

### Creating Your Dataset

For most projects, you will create a dataset manually or semi-automatically:

1. **Manual curation**: Write or collect example input/output pairs
2. **Synthetic generation**: Use a larger model (e.g., Claude, GPT-4) to generate training data from your specifications
3. **Public datasets**: Start with an existing dataset from Hugging Face Hub and filter/modify it

## 5. Model Selection

Choose your base model based on your hardware and task:

| Model | Parameters | Min VRAM (QLoRA) | Strengths |
|-------|-----------|-------------------|-----------|
| Llama 3.2 3B | 3B | 4-6 GB | Fast, good for simple tasks |
| Llama 3.1 8B | 8B | 8-10 GB | Strong general performance |
| Mistral 7B v0.3 | 7B | 8-10 GB | Strong reasoning |
| Qwen 2.5 7B | 7B | 8-10 GB | Multilingual strength |
| Gemma 2 9B | 9B | 10-12 GB | Good instruction following |
| Llama 3.1 70B | 70B | 20-24 GB | Near frontier quality |

**Rule of thumb**: Start with the largest model that fits comfortably in your VRAM. An 8B model fine-tuned on good data will outperform a 70B model fine-tuned on bad data.

## 6. Training with Unsloth

Here is a complete training script:

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# --- Model Setup ---
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B-bnb-4bit",  # 4-bit quantized
    max_seq_length=2048,
    load_in_4bit=True,
)

# --- Add LoRA Adapters ---
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                          # LoRA rank (higher = more capacity, more VRAM)
    lora_alpha=16,                 # Scaling factor (usually equal to r)
    lora_dropout=0,                # Unsloth optimizes for 0 dropout
    target_modules=[               # Apply to all linear layers
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    use_gradient_checkpointing="unsloth",  # Saves 60% VRAM
)

# --- Load Dataset ---
dataset = load_dataset("json", data_files="my_dataset.json", split="train")

# Format into chat template
def format_example(example):
    messages = [
        {"role": "user", "content": example["instruction"]},
        {"role": "assistant", "content": example["output"]},
    ]
    text = tokenizer.apply_chat_template(messages, tokenize=False)
    return {"text": text}

dataset = dataset.map(format_example)

# --- Training ---
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,   # Effective batch size = 2 * 4 = 8
        warmup_steps=10,
        num_train_epochs=3,
        learning_rate=2e-4,              # Standard starting point for QLoRA
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        output_dir="./checkpoints",
        save_strategy="epoch",
        optim="adamw_8bit",             # 8-bit optimizer saves VRAM
        seed=42,
    ),
)

trainer.train()
```

### Key Hyperparameters Explained

- **`r` (LoRA rank)**: Controls adapter capacity. Start with 16. Increase to 32 or 64 for complex tasks. Higher values use more VRAM.
- **`learning_rate`**: Start at 2e-4 for QLoRA. Reduce to 1e-4 if training loss is unstable.
- **`num_train_epochs`**: 1-3 for small datasets (<1000 examples). 1 epoch for large datasets.
- **`per_device_train_batch_size`**: Start at 2, reduce to 1 if you hit OOM errors.
- **`gradient_accumulation_steps`**: Simulates a larger batch size without extra VRAM. Effective batch = batch_size * accumulation_steps.

## 7. Monitoring Training

Watch these signals during training:

- **Training loss**: Should decrease steadily. If it plateaus early, increase learning rate or LoRA rank.
- **Training loss spikes**: Reduce learning rate.
- **Validation loss increasing while training loss decreases**: Overfitting. Stop training, reduce epochs, or add more data.

```python
# Add evaluation during training
from datasets import load_dataset

# Split your dataset
dataset = dataset.train_test_split(test_size=0.1, seed=42)

trainer = SFTTrainer(
    # ... same as above ...
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    args=TrainingArguments(
        # ... same as above ...
        eval_strategy="steps",
        eval_steps=50,
    ),
)
```

## 8. Evaluation

### Automated Metrics

- **Perplexity**: Measures how confident the model is in its predictions. Lower is better. Useful for comparing before/after fine-tuning.
- **Training/validation loss**: The primary signal during training.

### Manual Evaluation (Most Important)

Automated metrics tell you *something* but not *everything*. Always test your fine-tuned model manually:

1. **Prepare 20-50 test prompts** that cover your use case, including edge cases
2. **Compare outputs** from the base model vs. your fine-tuned model
3. **Check for regressions**: Does the model still handle general tasks well?
4. **Look for hallucinations**: Does it make up facts in your domain?

### LLM-as-Judge

Use a stronger model to evaluate your fine-tuned model's outputs:

```python
# Pseudocode for LLM-as-judge evaluation
test_prompts = load_test_prompts()
base_outputs = [base_model.generate(p) for p in test_prompts]
finetuned_outputs = [finetuned_model.generate(p) for p in test_prompts]

for prompt, base_out, ft_out in zip(test_prompts, base_outputs, finetuned_outputs):
    judge_prompt = f"""Rate these two responses to the prompt on a 1-5 scale.
    Prompt: {prompt}
    Response A: {base_out}
    Response B: {ft_out}
    Which is better and why?"""
    judgment = strong_model.generate(judge_prompt)
```

## 9. Export and Deploy

After training, merge the LoRA adapters into the base model and export for inference:

```python
# Save LoRA adapters
model.save_pretrained("./finetuned-lora")
tokenizer.save_pretrained("./finetuned-lora")

# Export to GGUF for llama.cpp / Ollama
model.save_pretrained_gguf(
    "./finetuned-gguf",
    tokenizer,
    quantization_method="q4_k_m",  # Good balance of quality and size
)
```

### Run with Ollama

```bash
# Create a Modelfile
cat > Modelfile << 'EOF'
FROM ./finetuned-gguf/unsloth.Q4_K_M.gguf
TEMPLATE """{{ .Prompt }}"""
PARAMETER temperature 0.7
PARAMETER top_p 0.9
EOF

# Import into Ollama
ollama create my-finetuned-model -f Modelfile

# Run it
ollama run my-finetuned-model "Your prompt here"
```

## 10. Troubleshooting

| Problem | Solution |
|---------|----------|
| CUDA out of memory | Reduce batch size to 1, reduce max_seq_length, reduce LoRA rank |
| Training loss not decreasing | Increase learning rate, check dataset formatting |
| Model outputs gibberish | Check chat template formatting, ensure dataset is clean |
| Model overfits (memorizes training data) | Reduce epochs, add more diverse data, reduce LoRA rank |
| Slow training | Enable gradient checkpointing, use Unsloth optimizations |

## Next Steps

- Work through the companion exercise notebook (`02-exercises.py`) to practice each step hands-on
- Experiment with different LoRA ranks and learning rates
- Try mixing 5-10% general instruction data to preserve broad capabilities
- Explore RLHF/DPO for preference-based fine-tuning after mastering SFT

## Sources

- [Fine-Tune Local LLMs 2026 -- SitePoint](https://www.sitepoint.com/fine-tune-local-llms-2026/)
- [Fine-tuning LLMs Guide -- Unsloth Documentation](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide)
- [LoRA Hyperparameters Guide -- Unsloth Documentation](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- [Datasets Guide -- Unsloth Documentation](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide)
- [Master LoRA and QLoRA -- Let's Data Science](https://letsdatascience.com/blog/fine-tuning-llms-with-lora-and-qlora-complete-guide)
- [LoRA and QLoRA Fine-Tuning 2026 Guide -- Meta Intelligence](https://www.meta-intelligence.tech/en/insight-lora-finetuning)
- [Fine-tune Llama 3.1 with Unsloth -- Hugging Face](https://huggingface.co/blog/mlabonne/sft-llama3)
- [LLM Fine-Tuning GPU Guide -- RunPod](https://www.runpod.io/blog/llm-fine-tuning-gpu-guide)
- [How Much VRAM for Fine-Tuning -- Modal](https://modal.com/blog/how-much-vram-need-fine-tuning)
- [LLM Evaluation Metrics -- AIMultiple](https://research.aimultiple.com/large-language-model-evaluation/)
- [How to Prepare a Dataset for Instruction Tuning -- Weights & Biases](https://wandb.ai/capecape/alpaca_ft/reports/How-to-Fine-Tune-an-LLM-Part-1-Preparing-a-Dataset-for-Instruction-Tuning--Vmlldzo1NTcxNzE2)
