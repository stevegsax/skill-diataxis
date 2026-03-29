# How to Tune Hyperparameters for Local Fine-Tuning

This guide shows you how to adjust training hyperparameters based on your hardware and training behavior.

## How to Adjust Batch Size for Your VRAM

1. Start with `per_device_train_batch_size=4` and `gradient_accumulation_steps=4` (effective batch size 16).

2. If you get a CUDA out-of-memory error, halve the batch size:

    ```python
    per_device_train_batch_size = 2  # halved
    gradient_accumulation_steps = 8  # doubled to keep effective batch size at 16
    ```

3. If it still fails, go to batch size 1:

    ```python
    per_device_train_batch_size = 1
    gradient_accumulation_steps = 16
    ```

4. If batch size 1 still fails, enable gradient checkpointing (if not already enabled):

    ```python
    gradient_checkpointing = True
    ```

5. If it still fails, reduce `max_seq_length` (e.g., from 512 to 256).

The VRAM formula (approximate):

```
VRAM = model_size_4bit + (batch_size * seq_length * hidden_dim * 2 bytes) + optimizer_states
```

See the [Training Hyperparameters Reference](../reference/training-hyperparameters.md) for all parameter details.

## How to Set Learning Rate and Scheduler

1. Start with `learning_rate=2e-4` for QLoRA. This is the value from the QLoRA paper and works for most scenarios.

2. If loss spikes or becomes NaN, reduce the learning rate:

    ```python
    learning_rate = 1e-4  # or 5e-5 for more stability
    ```

3. Use a cosine scheduler with warmup:

    ```python
    lr_scheduler_type = "cosine"
    warmup_ratio = 0.03  # 3% of total steps
    ```

4. If training for multiple epochs, consider a linear scheduler to avoid the cosine's rapid initial decay:

    ```python
    lr_scheduler_type = "linear"
    ```

## How to Choose LoRA Rank and Alpha

1. **Rank (`r`)**: Controls the capacity of the LoRA adapters.

    - `r=8`: lightweight, good for simple tasks or small datasets
    - `r=16`: balanced default, works for most fine-tuning
    - `r=32` or `r=64`: higher capacity, useful for complex tasks or large datasets

2. **Alpha (`lora_alpha`)**: Scaling factor. A common heuristic is `alpha = 2 * r`:

    ```python
    r = 16
    lora_alpha = 32
    ```

3. **Dropout (`lora_dropout`)**: Regularization to prevent overfitting:

    - `0.0`: no dropout (use with large datasets)
    - `0.05`: light regularization (default)
    - `0.1`: more regularization (use with small datasets)

## How to Configure Target Modules for Different Architectures

1. The default targets are attention projection layers. For most models:

    ```python
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]
    ```

2. For better results, also include MLP layers:

    ```python
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"]
    ```

3. To find the correct module names for a given model:

    ```python
    for name, _ in model.named_modules():
        if "proj" in name or "dense" in name:
            print(name)
    ```

4. Architecture-specific names:

    | Model Family | Attention Modules | MLP Modules |
    |-------------|-------------------|-------------|
    | Llama, Mistral | q_proj, k_proj, v_proj, o_proj | gate_proj, up_proj, down_proj |
    | Phi-3 | qkv_proj, o_proj | gate_up_proj, down_proj |
    | Gemma | q_proj, k_proj, v_proj, o_proj | gate_proj, up_proj, down_proj |
    | Qwen | c_attn, c_proj | w1, w2, c_fc |

For background on why these modules are targeted, see [How LoRA Works](../explanation/how-lora-works.md).
