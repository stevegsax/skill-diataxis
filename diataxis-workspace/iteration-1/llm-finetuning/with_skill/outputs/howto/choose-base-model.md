# How to Choose a Base Model for Local Fine-Tuning

This guide shows you how to select the right base model given your hardware, task, and licensing requirements.

## Step 1: Determine Your VRAM Budget

Check your available VRAM:

```bash
nvidia-smi --query-gpu=memory.total --format=csv,noheader
```

Apply this rule of thumb for QLoRA training (4-bit base model + LoRA adapters + optimizer states + activations):

| GPU VRAM | Maximum Model Size (QLoRA) |
|----------|---------------------------|
| 8 GB     | 7-8B parameters           |
| 12 GB    | 7-8B parameters (comfortable) |
| 16 GB    | 13B parameters            |
| 24 GB    | 13B parameters (comfortable), 34B (tight) |
| 48 GB    | 70B parameters            |

If your VRAM is at the boundary, reduce batch size to 1 and enable gradient checkpointing. See [How to Tune Hyperparameters](tune-hyperparameters.md).

## Step 2: Check Licensing

Before investing time in fine-tuning, verify the model license permits your use case:

1. Go to the model page on Hugging Face Hub
2. Check the "License" field in the model card
3. Key license types:

    - **Apache 2.0** (Mistral, Gemma): permissive, commercial use allowed
    - **Llama Community License** (Llama 3.x): commercial use allowed with conditions (700M+ monthly active users need a separate agreement)
    - **Research only**: no commercial use

See the [Model Comparison Reference](../reference/model-comparison.md) for a complete license table.

## Step 3: Match Model Family to Your Task

- **General instruction following**: Llama 3.1 8B or Mistral 7B are strong defaults
- **Code generation**: Start with a code-specialized variant (e.g., CodeLlama, DeepSeek Coder)
- **Multilingual tasks**: Qwen 2.5 has strong multilingual support
- **Small/fast models**: Phi-3 Mini (3.8B) or Gemma 2 2B for constrained hardware
- **Maximum quality at a given size**: Compare recent benchmark scores in the [Model Comparison Reference](../reference/model-comparison.md)

## Step 4: Decide on Quantization Level

For QLoRA fine-tuning, the base model is loaded in 4-bit. This is the standard approach and what the tutorials in this learning path use.

If you have ample VRAM and want potentially better results:

- Load in 8-bit (`load_in_8bit=True`) -- uses ~2x the VRAM of 4-bit
- Load in fp16 (no quantization) and use standard LoRA -- uses ~4x the VRAM of 4-bit

For most local fine-tuning scenarios, 4-bit (QLoRA) is the right choice.

For background on quantization tradeoffs, see [Understanding Model Sizes](../explanation/understanding-model-sizes.md).

## Step 5: Verify the Model Loads

Before committing to a training run, verify the model loads on your hardware:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

model = AutoModelForCausalLM.from_pretrained(
    "your-chosen-model",
    quantization_config=BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16),
    device_map="auto",
)
print(f"Loaded. VRAM used: {torch.cuda.memory_allocated() / 1e9:.1f} GB")
```

If this fails with an out-of-memory error, select a smaller model.
