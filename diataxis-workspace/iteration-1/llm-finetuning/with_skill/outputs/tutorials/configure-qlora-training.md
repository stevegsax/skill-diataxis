# Configuring QLoRA Training

In this tutorial, we will configure a complete QLoRA fine-tuning setup: loading a quantized base model, attaching LoRA adapters, setting training hyperparameters, and assembling an SFTTrainer. By the end, you will have a fully configured trainer object ready to run.

## Prerequisites

- Completed the [Environment Setup Tutorial](environment-setup.md)
- Completed the [Dataset Preparation Tutorial](dataset-preparation.md)
- At least 10 GB of free VRAM

## Step 1: Load the Base Model with 4-bit Quantization

We load the model in 4-bit precision using bitsandbytes. This reduces VRAM usage from ~16 GB (fp16) to ~5 GB for an 8B parameter model:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_name = "meta-llama/Meta-Llama-3.1-8B"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.pad_token_id
```

You should see the model download (if not cached) and load onto your GPU. Check memory usage:

```python
print(f"Model loaded. GPU memory used: {torch.cuda.memory_allocated() / 1e9:.1f} GB")
```

You should see approximately 5-6 GB used for an 8B model in 4-bit.

## Step 2: Create the LoRA Configuration

Now we attach LoRA adapters to the model. These are the small trainable matrices that will be updated during fine-tuning:

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

You should see:

```
trainable params: 83,886,080 || all params: 8,114,212,864 || trainable%: 1.0337
```

Notice that only about 1% of the parameters are trainable. This is the power of LoRA -- we get fine-tuning with a fraction of the memory cost. For more on why this works, see [How LoRA Works](../explanation/how-lora-works.md).

## Step 3: Set Training Arguments

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    weight_decay=0.01,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    eval_strategy="steps",
    eval_steps=100,
    bf16=True,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
    max_grad_norm=0.3,
    report_to="none",
)
```

Let's understand the key settings:

- **per_device_train_batch_size=4** with **gradient_accumulation_steps=4** gives an effective batch size of 16
- **learning_rate=2e-4** is a common starting point for QLoRA
- **paged_adamw_8bit** uses 8-bit optimizer states to save more memory
- **gradient_checkpointing=True** trades compute for memory

See the [Training Hyperparameters Reference](../reference/training-hyperparameters.md) for the full list of parameters and their valid ranges.

## Step 4: Create the SFTTrainer

Now we connect everything together. Assuming you have `train_data` and `val_data` from the dataset preparation tutorial:

```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    eval_dataset=val_data,
    processing_class=tokenizer,
    max_seq_length=512,
)
```

## Step 5: Verify the Configuration

Before training, let's make sure everything looks right:

```python
print(f"Training examples: {len(trainer.train_dataset)}")
print(f"Validation examples: {len(trainer.eval_dataset)}")
print(f"Effective batch size: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps}")
print(f"Steps per epoch: {len(trainer.train_dataset) // (training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps)}")
print(f"Total training steps: {trainer.state.max_steps if hasattr(trainer, 'state') else 'will be computed at train time'}")
print(f"GPU memory: {torch.cuda.memory_allocated() / 1e9:.1f} GB allocated")
```

You should see the training configuration summary with reasonable numbers.

## What You Accomplished

You now have a fully configured QLoRA training setup:

- A base model loaded in 4-bit quantization (~5 GB VRAM)
- LoRA adapters attached to attention and MLP layers (~1% trainable parameters)
- Training arguments tuned for local GPU training
- An SFTTrainer ready to call `.train()`

## Next Steps

- [Run Training Tutorial](run-training.md) -- start the training run
- [How to Tune Hyperparameters](../howto/tune-hyperparameters.md) -- adjust settings for your hardware
- [Training Hyperparameters Reference](../reference/training-hyperparameters.md) -- all parameters documented
- [How LoRA Works](../explanation/how-lora-works.md) -- why this approach is effective

## Exercises

Work through the [Training Configuration Exercise](../exercises/training-config.py) to experiment with different LoRA configurations.
