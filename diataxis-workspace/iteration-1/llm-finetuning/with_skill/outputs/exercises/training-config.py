import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def intro():
    import marimo as mo

    mo.md(
        """
        # Training Configuration Exercise

        This exercise helps you build intuition about how LoRA and training
        hyperparameters affect fine-tuning. You will experiment with different
        configurations and see how they impact trainable parameters, memory usage,
        and training dynamics.
        """
    )
    return (mo,)


@app.cell
def lora_params():
    import marimo as mo

    rank_slider = mo.ui.slider(start=2, stop=128, step=2, value=16, label="LoRA rank (r)")
    alpha_slider = mo.ui.slider(
        start=2, stop=256, step=2, value=32, label="LoRA alpha"
    )
    dropout_slider = mo.ui.slider(
        start=0.0, stop=0.3, step=0.01, value=0.05, label="LoRA dropout"
    )

    target_modules = mo.ui.multiselect(
        options=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        value=["q_proj", "k_proj", "v_proj", "o_proj"],
        label="Target modules",
    )

    mo.md(
        f"""
        ## Part 1: LoRA Configuration

        Adjust the LoRA parameters below to see how they affect the number of
        trainable parameters.

        {rank_slider}
        {alpha_slider}
        {dropout_slider}
        {target_modules}
        """
    )
    return (rank_slider, alpha_slider, dropout_slider, target_modules)


@app.cell
def lora_analysis(rank_slider, alpha_slider, target_modules):
    import marimo as mo

    rank = rank_slider.value
    alpha = alpha_slider.value
    modules = target_modules.value

    # Approximate sizes for Llama 3.1 8B
    hidden_size = 4096
    intermediate_size = 14336
    num_layers = 32

    module_sizes = {
        "q_proj": hidden_size * hidden_size,
        "k_proj": hidden_size * (hidden_size // 8),  # GQA
        "v_proj": hidden_size * (hidden_size // 8),
        "o_proj": hidden_size * hidden_size,
        "gate_proj": hidden_size * intermediate_size,
        "up_proj": hidden_size * intermediate_size,
        "down_proj": intermediate_size * hidden_size,
    }

    total_base_params = 8_000_000_000  # approximate
    lora_params_per_layer = sum(
        2 * rank * (module_sizes.get(m, 0) ** 0.5)  # rough: 2 * r * (in + out)
        for m in modules
    )

    # More accurate calculation
    lora_params_total = 0
    for m in modules:
        if m in ("q_proj", "o_proj"):
            lora_params_total += 2 * rank * hidden_size * num_layers
        elif m in ("k_proj", "v_proj"):
            lora_params_total += (rank * hidden_size + rank * (hidden_size // 8)) * num_layers
        elif m in ("gate_proj", "up_proj"):
            lora_params_total += (rank * hidden_size + rank * intermediate_size) * num_layers
        elif m == "down_proj":
            lora_params_total += (rank * intermediate_size + rank * hidden_size) * num_layers

    trainable_pct = (lora_params_total / total_base_params) * 100
    scaling_factor = alpha / rank
    lora_memory_mb = lora_params_total * 2 / 1e6  # bf16 = 2 bytes

    mo.md(
        f"""
        ### LoRA Configuration Analysis (Llama 3.1 8B)

        | Metric | Value |
        |--------|-------|
        | LoRA rank | {rank} |
        | LoRA alpha | {alpha} |
        | Effective scaling (alpha/r) | {scaling_factor:.1f} |
        | Target modules | {', '.join(modules) if modules else 'none selected'} |
        | Trainable parameters | {lora_params_total:,} |
        | Trainable % of total | {trainable_pct:.2f}% |
        | LoRA adapter memory (bf16) | {lora_memory_mb:.1f} MB |

        **Observations**:
        - {"The scaling factor is 2.0, which is the standard default." if scaling_factor == 2.0 else f"The scaling factor is {scaling_factor:.1f}. The standard default is 2.0 (alpha = 2 * r)."}
        - {"Only attention modules are targeted. Adding MLP modules increases capacity but also memory." if len(modules) <= 4 else "Both attention and MLP modules are targeted. This increases capacity but uses more memory."}
        - {"Rank is at the standard default of 16." if rank == 16 else f"Rank {rank} {'is lower than the default (16) — suitable for simple tasks.' if rank < 16 else 'is higher than the default (16) — more capacity but higher overfitting risk.'}"}
        """
    )
    return (lora_params_total,)


@app.cell
def training_args_explorer():
    import marimo as mo

    batch_size = mo.ui.slider(start=1, stop=8, step=1, value=4, label="Batch size")
    grad_accum = mo.ui.slider(
        start=1, stop=32, step=1, value=4, label="Gradient accumulation steps"
    )
    lr_slider = mo.ui.slider(
        start=1, stop=30, step=1, value=20, label="Learning rate (x10^-5)"
    )
    epochs_slider = mo.ui.slider(start=1, stop=10, step=1, value=1, label="Epochs")
    seq_len = mo.ui.dropdown(
        options={"256": "256", "512": "512", "1024": "1024", "2048": "2048"},
        value="512",
        label="Max sequence length",
    )

    mo.md(
        f"""
        ## Part 2: Training Arguments

        Experiment with training arguments to understand their impact on
        training dynamics and memory usage.

        {batch_size}
        {grad_accum}
        {lr_slider}
        {epochs_slider}
        {seq_len}
        """
    )
    return (batch_size, grad_accum, lr_slider, epochs_slider, seq_len)


@app.cell
def training_analysis(batch_size, grad_accum, lr_slider, epochs_slider, seq_len):
    import marimo as mo

    bs = batch_size.value
    ga = grad_accum.value
    lr = lr_slider.value * 1e-5
    epochs = epochs_slider.value
    max_seq = int(seq_len.value)

    effective_bs = bs * ga
    num_examples = 50000  # typical Alpaca-sized dataset
    steps_per_epoch = num_examples // effective_bs
    total_steps = steps_per_epoch * epochs
    warmup_steps = int(total_steps * 0.03)

    # VRAM estimation (very rough, for Llama 3.1 8B with QLoRA)
    model_vram = 5.0  # 4-bit 8B model
    activation_vram = bs * max_seq * 4096 * 2 / 1e9  # rough
    optimizer_vram = 0.3  # 8-bit optimizer on LoRA params
    total_vram = model_vram + activation_vram + optimizer_vram

    # Time estimation (rough: ~1 step per second on RTX 3090)
    time_hours = total_steps / 3600

    mo.md(
        f"""
        ### Training Plan Analysis

        | Metric | Value |
        |--------|-------|
        | Per-device batch size | {bs} |
        | Gradient accumulation | {ga} |
        | **Effective batch size** | **{effective_bs}** |
        | Learning rate | {lr:.1e} |
        | Epochs | {epochs} |
        | Max sequence length | {max_seq} |
        | Steps per epoch | {steps_per_epoch:,} |
        | Total training steps | {total_steps:,} |
        | Warmup steps (3%) | {warmup_steps} |
        | Estimated VRAM | ~{total_vram:.1f} GB |
        | Estimated time (RTX 3090) | ~{time_hours:.1f} hours |

        **Observations**:
        - {"Effective batch size of 16 is a good default." if effective_bs == 16 else f"Effective batch size is {effective_bs}. The standard default is 16."}
        - {"Learning rate 2e-4 is the standard QLoRA default." if abs(lr - 2e-4) < 1e-6 else f"Learning rate {lr:.1e} {'may be too low — training will be slow.' if lr < 1e-4 else 'may be too high — watch for instability.' if lr > 3e-4 else 'is in a reasonable range.'}"}
        - {"Single epoch is often sufficient for instruction tuning." if epochs == 1 else f"{epochs} epochs — watch for overfitting after epoch 1-2."}
        - {"Estimated VRAM fits on an 8 GB GPU." if total_vram < 8 else "Estimated VRAM fits on a 24 GB GPU." if total_vram < 24 else "Estimated VRAM may require 48+ GB. Consider reducing batch size."}
        """
    )
    return ()


@app.cell
def rank_vs_params_chart():
    import marimo as mo

    mo.md(
        """
        ## Part 3: Understanding Rank vs Trainable Parameters

        The table below shows how LoRA rank affects trainable parameters for
        Llama 3.1 8B with all attention + MLP modules targeted.

        | Rank | Trainable Params | % of Total | Adapter Size (MB) |
        |------|-----------------|------------|-------------------|
        | 4 | ~21M | 0.26% | 42 |
        | 8 | ~42M | 0.52% | 84 |
        | 16 | ~84M | 1.03% | 168 |
        | 32 | ~168M | 2.07% | 336 |
        | 64 | ~336M | 4.14% | 672 |
        | 128 | ~672M | 8.28% | 1,344 |

        Key insight: trainable parameters scale linearly with rank. Doubling the
        rank doubles the parameters. For most instruction-tuning tasks, rank 16
        provides sufficient capacity. Rank 64+ is rarely needed and increases
        overfitting risk.
        """
    )
    return ()


@app.cell
def config_quiz():
    import marimo as mo

    q1 = mo.ui.dropdown(
        options={
            "Increase LoRA rank": "wrong1",
            "Reduce batch size and increase gradient accumulation": "correct",
            "Increase learning rate": "wrong2",
            "Use fp32 instead of bf16": "wrong3",
        },
        label="Your answer",
    )

    mo.md(
        f"""
        ## Part 4: Configuration Quiz

        **Question 1**: You are running out of VRAM during training. Which
        adjustment maintains the same effective batch size while reducing memory?

        {q1}
        """
    )
    return (q1,)


@app.cell
def quiz_feedback(q1):
    import marimo as mo

    if q1.value == "correct":
        feedback = "Correct. Reducing per-device batch size reduces the activations held in memory. Increasing gradient accumulation compensates by accumulating gradients over more steps before each optimizer update."
    elif q1.value is None:
        feedback = "Select an answer above."
    else:
        feedback = "Not quite. Reducing batch size and increasing gradient accumulation keeps the effective batch size the same while reducing peak memory usage. The other options either don't help with memory or make it worse."

    mo.md(f"**Feedback**: {feedback}")
    return ()


@app.cell
def summary():
    import marimo as mo

    mo.md(
        """
        ## Summary

        In this exercise you explored:

        - How LoRA rank, alpha, and target modules affect trainable parameters
        - How batch size, gradient accumulation, and sequence length affect memory and training time
        - The relationship between configuration choices and practical constraints

        Next: proceed to the [Configure QLoRA Training Tutorial](../tutorials/configure-qlora-training.md)
        to apply these settings to a real model.
        """
    )
    return ()


if __name__ == "__main__":
    app.run()
