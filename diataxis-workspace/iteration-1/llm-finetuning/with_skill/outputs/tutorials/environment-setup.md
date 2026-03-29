# Setting Up Your Local Fine-Tuning Environment

In this tutorial, we will set up a complete Python environment for fine-tuning LLMs on your local machine. Along the way, we will install PyTorch with GPU support, the Hugging Face ecosystem, and the parameter-efficient training libraries. By the end, you will have a verified environment ready for training.

## Prerequisites

- An NVIDIA GPU with at least 8 GB VRAM
- NVIDIA drivers installed (version 525+)
- Python 3.10 or later

## Step 1: Create a Virtual Environment

First, create a dedicated virtual environment. Open your terminal and run:

```bash
python3 -m venv llm-finetune
source llm-finetune/bin/activate
```

You should see your prompt change to show `(llm-finetune)` at the beginning. Verify you are using the right Python:

```bash
python --version
```

You should see output like:

```
Python 3.11.9
```

Any version 3.10 or above works.

## Step 2: Upgrade pip

```bash
pip install --upgrade pip
```

You should see:

```
Successfully installed pip-24.x.x
```

## Step 3: Install PyTorch with CUDA Support

Install PyTorch with CUDA 12.1 support:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

This takes a minute or two. Now verify GPU access:

```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}'); print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB')"
```

You should see something like:

```
CUDA available: True
GPU: NVIDIA GeForce RTX 3090
VRAM: 24.3 GB
```

If `CUDA available` shows `False`, check that your NVIDIA drivers are installed and up to date. See the [environment requirements reference](../reference/environment-requirements.md) for the CUDA/driver compatibility matrix.

## Step 4: Install the Hugging Face Ecosystem

Install the core libraries:

```bash
pip install transformers datasets accelerate tokenizers
```

Verify the installation:

```bash
python -c "import transformers; print(f'transformers: {transformers.__version__}')"
```

You should see:

```
transformers: 4.47.x
```

## Step 5: Install PEFT and Quantization Libraries

PEFT provides LoRA and QLoRA support. bitsandbytes enables 4-bit quantization:

```bash
pip install peft bitsandbytes
```

Verify bitsandbytes can see your GPU:

```bash
python -c "import bitsandbytes as bnb; print('bitsandbytes loaded successfully')"
```

You should see:

```
bitsandbytes loaded successfully
```

If you get CUDA-related errors, see the [environment requirements reference](../reference/environment-requirements.md) for version compatibility.

## Step 6: Install TRL (Transformer Reinforcement Learning)

TRL provides the `SFTTrainer` class we will use for supervised fine-tuning:

```bash
pip install trl
```

Verify:

```bash
python -c "from trl import SFTTrainer; print('TRL loaded successfully')"
```

## Step 7: (Optional) Install Unsloth for Faster Training

Unsloth optimizes training to run 2-5x faster with lower memory usage:

```bash
pip install unsloth
```

Verify:

```bash
python -c "import unsloth; print(f'unsloth: {unsloth.__version__}')"
```

This step is optional. Everything in this learning path works without unsloth, but it significantly speeds up training if your hardware is supported.

## Step 8: Verify the Complete Environment

Run a comprehensive check:

```bash
python -c "
import torch
import transformers
import datasets
import peft
import bitsandbytes
import trl

print('All libraries loaded successfully')
print(f'  PyTorch: {torch.__version__}')
print(f'  CUDA: {torch.version.cuda}')
print(f'  GPU: {torch.cuda.get_device_name(0)}')
print(f'  VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB')
print(f'  transformers: {transformers.__version__}')
print(f'  datasets: {datasets.__version__}')
print(f'  peft: {peft.__version__}')
print(f'  trl: {trl.__version__}')
"
```

You should see all libraries listed with their versions and your GPU information.

## What You Accomplished

You now have a working environment with:

- PyTorch with CUDA support
- Hugging Face transformers and datasets
- PEFT for parameter-efficient fine-tuning (LoRA/QLoRA)
- bitsandbytes for 4-bit quantization
- TRL for supervised fine-tuning
- (Optionally) unsloth for training acceleration

## Next Steps

- [Dataset Preparation Tutorial](dataset-preparation.md) -- prepare training data
- [Environment Requirements Reference](../reference/environment-requirements.md) -- version matrix and hardware specs
- [Understanding Model Sizes](../explanation/understanding-model-sizes.md) -- why hardware constraints matter

## Exercises

Work through the [Environment Check Exercise](../exercises/environment-check.py) to interactively verify your setup.
