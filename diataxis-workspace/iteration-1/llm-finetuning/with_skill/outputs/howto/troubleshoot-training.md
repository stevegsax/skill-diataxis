# How to Troubleshoot Common Training Issues

This guide shows you how to diagnose and fix problems that occur during local LLM fine-tuning.

## How to Fix CUDA Out-of-Memory Errors

**Symptom**: `torch.cuda.OutOfMemoryError: CUDA out of memory`

1. Reduce batch size:

    ```python
    per_device_train_batch_size = 1
    gradient_accumulation_steps = 16  # increase to maintain effective batch size
    ```

2. Enable gradient checkpointing if not already enabled:

    ```python
    gradient_checkpointing = True
    ```

3. Reduce sequence length:

    ```python
    max_seq_length = 256  # down from 512
    ```

4. Use 8-bit optimizer:

    ```python
    optim = "paged_adamw_8bit"
    ```

5. If all else fails, switch to a smaller model.

Clear GPU cache before retrying:

```python
import torch
torch.cuda.empty_cache()
```

## How to Resume Training from a Checkpoint

**Symptom**: Training was interrupted (crash, keyboard interrupt, power loss).

1. Locate the latest checkpoint directory:

    ```python
    import os
    checkpoints = sorted(
        [d for d in os.listdir("./results") if d.startswith("checkpoint-")],
        key=lambda x: int(x.split("-")[1])
    )
    latest = f"./results/{checkpoints[-1]}"
    print(f"Resuming from: {latest}")
    ```

2. Resume training:

    ```python
    trainer.train(resume_from_checkpoint=latest)
    ```

## How to Handle NaN Loss Values

**Symptom**: `{'loss': nan, ...}` in training output.

1. Reduce the learning rate:

    ```python
    learning_rate = 1e-4  # or lower
    ```

2. Increase warmup steps:

    ```python
    warmup_ratio = 0.1  # 10% of total steps
    ```

3. Reduce gradient norm clipping:

    ```python
    max_grad_norm = 0.3  # lower value clips more aggressively
    ```

4. Check your data for empty or malformed examples:

    ```python
    for i, example in enumerate(train_data):
        if not example["formatted_text"].strip():
            print(f"Empty example at index {i}")
    ```

5. If using bf16, try fp16 or fp32:

    ```python
    bf16 = False
    fp16 = True
    ```

## How to Diagnose Slow Training Speed

**Symptom**: Training steps take much longer than expected.

1. Check if GPU is being used:

    ```bash
    nvidia-smi
    ```

    GPU utilization should be 80%+. If it is near 0%, the model may be on CPU.

2. Verify device placement:

    ```python
    print(next(model.parameters()).device)  # should show cuda:0
    ```

3. If using gradient checkpointing, training will be ~30% slower. This is expected.

4. Ensure DataLoader is not the bottleneck. Set:

    ```python
    dataloader_num_workers = 4
    ```

5. If using unsloth and seeing no speedup, verify it patched the model:

    ```python
    # unsloth logs a message at model load time
    # Check for "Unsloth: ..." in the output
    ```

## How to Use Gradient Checkpointing to Reduce Memory

**Symptom**: Training runs out of memory but you cannot reduce batch size further.

1. Enable gradient checkpointing in TrainingArguments:

    ```python
    gradient_checkpointing = True
    ```

2. If using a custom training loop, enable it on the model directly:

    ```python
    model.gradient_checkpointing_enable()
    ```

Gradient checkpointing recomputes intermediate activations during the backward pass instead of storing them. This reduces memory usage by 40-60% at the cost of ~30% slower training.

For background on why these issues occur, see [How LoRA Works](../explanation/how-lora-works.md) and [Understanding Model Sizes](../explanation/understanding-model-sizes.md).
