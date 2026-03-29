# Environment Requirements Reference

## Minimum Hardware

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| GPU | NVIDIA with 8 GB VRAM (RTX 3060, 3070) | NVIDIA with 24 GB VRAM (RTX 3090, 4090) |
| System RAM | 16 GB | 32 GB |
| Disk | 50 GB free | 100 GB free (model caches) |
| CPU | 4 cores | 8+ cores |

## VRAM Requirements by Model Size (QLoRA Training)

| Model Parameters | VRAM (model load, 4-bit) | VRAM (training, batch=4) | VRAM (training, batch=1) |
|-----------------|--------------------------|--------------------------|--------------------------|
| 3B | ~2 GB | ~5 GB | ~4 GB |
| 7-8B | ~5 GB | ~10 GB | ~7 GB |
| 13B | ~8 GB | ~16 GB | ~11 GB |
| 34B | ~20 GB | ~36 GB | ~26 GB |
| 70B | ~38 GB | ~65 GB | ~48 GB |

All values assume gradient checkpointing enabled and 8-bit optimizer.

## Python and CUDA Compatibility

| Python | PyTorch | CUDA Toolkit | NVIDIA Driver |
|--------|---------|-------------|---------------|
| 3.10 | 2.2+ | 11.8, 12.1 | 525+ |
| 3.11 | 2.2+ | 11.8, 12.1, 12.4 | 525+ |
| 3.12 | 2.4+ | 12.1, 12.4 | 525+ |

## Library Version Matrix

| Library | Minimum Version | Tested Version | Notes |
|---------|----------------|----------------|-------|
| torch | 2.2.0 | 2.5.1 | Must match CUDA toolkit version |
| transformers | 4.44.0 | 4.47.1 | Required for Llama 3.1 support |
| datasets | 2.18.0 | 3.2.0 | |
| peft | 0.12.0 | 0.14.0 | Required for recent LoRA features |
| bitsandbytes | 0.43.0 | 0.45.0 | Must match CUDA version |
| trl | 0.9.0 | 0.13.0 | SFTTrainer API changes at 0.10 |
| accelerate | 0.33.0 | 1.2.0 | |
| tokenizers | 0.19.0 | 0.21.0 | |
| unsloth | 2024.8 | 2025.3 | Optional; requires specific torch version |

## Environment Variables

| Variable | Purpose | Example Value |
|----------|---------|---------------|
| `CUDA_VISIBLE_DEVICES` | Restrict which GPUs are used | `0` (first GPU only) |
| `HF_HOME` | Hugging Face cache directory | `~/.cache/huggingface` |
| `HF_TOKEN` | Authentication for gated models (e.g., Llama) | `hf_xxxxxxxxxxxx` |
| `TRANSFORMERS_CACHE` | Model cache location (deprecated, use HF_HOME) | `~/.cache/huggingface/hub` |
| `PYTORCH_CUDA_ALLOC_CONF` | CUDA memory allocator config | `expandable_segments:True` |
| `TOKENIZERS_PARALLELISM` | Disable tokenizer parallelism warnings | `false` |

## Accessing Gated Models

Some models (Llama 3.x) require accepting a license agreement:

1. Create a Hugging Face account at https://huggingface.co
2. Navigate to the model page (e.g., `meta-llama/Meta-Llama-3.1-8B`)
3. Accept the license agreement
4. Generate an access token at https://huggingface.co/settings/tokens
5. Set the token: `huggingface-cli login` or set `HF_TOKEN` environment variable

For a guide on using this environment, see the [Environment Setup Tutorial](../tutorials/environment-setup.md).
