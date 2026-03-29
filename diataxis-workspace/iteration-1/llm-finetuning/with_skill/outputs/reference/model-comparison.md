# Model Comparison Reference

## Model Families for Local Fine-Tuning

| Family | Parameters | VRAM (fp16) | VRAM (4-bit) | License | MMLU | HumanEval | Notes |
|--------|-----------|-------------|-------------|---------|------|-----------|-------|
| Llama 3.1 | 8B | 16 GB | 5 GB | Llama Community | 73.0 | 72.6 | Strong general-purpose default |
| Llama 3.1 | 70B | 140 GB | 38 GB | Llama Community | 86.0 | 80.5 | Requires 48+ GB VRAM for QLoRA |
| Mistral | 7B | 14 GB | 5 GB | Apache 2.0 | 62.5 | 30.5 | Permissive license; v0.3 |
| Mistral Nemo | 12B | 24 GB | 7 GB | Apache 2.0 | 68.0 | 40.2 | Good mid-range option |
| Gemma 2 | 2B | 4 GB | 1.5 GB | Apache 2.0 | 51.3 | 19.5 | Fits on any modern GPU |
| Gemma 2 | 9B | 18 GB | 5 GB | Apache 2.0 | 71.3 | 54.9 | Strong for its size |
| Gemma 2 | 27B | 54 GB | 15 GB | Apache 2.0 | 75.2 | 57.3 | Requires 24+ GB for QLoRA |
| Qwen 2.5 | 7B | 14 GB | 5 GB | Apache 2.0 | 74.2 | 75.6 | Strong multilingual + code |
| Qwen 2.5 | 14B | 28 GB | 8 GB | Apache 2.0 | 79.9 | 80.5 | Excellent quality per parameter |
| Qwen 2.5 | 72B | 144 GB | 40 GB | Qwen License | 86.1 | 86.6 | Requires 48+ GB VRAM |
| Phi-3 Mini | 3.8B | 8 GB | 2.5 GB | MIT | 69.7 | 59.1 | Very strong for its size |
| Phi-3 Small | 7B | 14 GB | 5 GB | MIT | 75.7 | 61.0 | MIT license |
| Phi-3 Medium | 14B | 28 GB | 8 GB | MIT | 78.0 | 62.2 | MIT license |

Benchmark scores are approximate and sourced from model cards and public evaluations. Scores vary by evaluation methodology.

## License Summary

| License | Commercial Use | Redistribution | Conditions |
|---------|---------------|----------------|------------|
| Apache 2.0 | Yes | Yes | Attribution required |
| MIT | Yes | Yes | Attribution required |
| Llama Community | Yes | Yes | Users with 700M+ monthly active users need Meta agreement |
| Qwen License | Conditional | Yes | Commercial use requires agreement for certain sizes |

## Model Hub IDs

| Model | Hugging Face Hub ID |
|-------|-------------------|
| Llama 3.1 8B | `meta-llama/Meta-Llama-3.1-8B` |
| Llama 3.1 8B Instruct | `meta-llama/Meta-Llama-3.1-8B-Instruct` |
| Llama 3.1 70B | `meta-llama/Meta-Llama-3.1-70B` |
| Mistral 7B v0.3 | `mistralai/Mistral-7B-v0.3` |
| Mistral Nemo 12B | `mistralai/Mistral-Nemo-Base-2407` |
| Gemma 2 2B | `google/gemma-2-2b` |
| Gemma 2 9B | `google/gemma-2-9b` |
| Qwen 2.5 7B | `Qwen/Qwen2.5-7B` |
| Qwen 2.5 14B | `Qwen/Qwen2.5-14B` |
| Phi-3 Mini | `microsoft/Phi-3-mini-4k-instruct` |
| Phi-3 Small | `microsoft/Phi-3-small-8k-instruct` |

## Choosing Between Base and Instruct Variants

| Variant | Use When |
|---------|----------|
| Base (e.g., `Meta-Llama-3.1-8B`) | Fine-tuning for instruction following from scratch; custom prompt formats |
| Instruct (e.g., `Meta-Llama-3.1-8B-Instruct`) | Further fine-tuning an already instruction-tuned model; domain adaptation |

Base models are the standard starting point for supervised fine-tuning. Instruct variants are useful when you want to preserve general instruction-following ability while adding domain-specific knowledge.

For guidance on selecting a model, see [How to Choose a Base Model](../howto/choose-base-model.md). For background on model sizing, see [Understanding Model Sizes](../explanation/understanding-model-sizes.md).
