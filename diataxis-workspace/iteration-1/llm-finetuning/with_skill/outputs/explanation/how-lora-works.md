# How LoRA Works

LoRA (Low-Rank Adaptation) is the technique that makes fine-tuning large language models feasible on consumer hardware. Understanding what it does -- conceptually, not mathematically -- helps you make better decisions about configuration and troubleshooting.

## The Problem: Full Fine-Tuning Is Impractical

In traditional fine-tuning, you update all the model's parameters. For a 7B-parameter model in fp16, this requires:

- ~14 GB for the model weights
- ~14 GB for the gradients (one gradient per weight)
- ~28 GB for the optimizer states (Adam stores two state values per weight)

That is roughly 56 GB of VRAM just for a 7B model, which exceeds what any single consumer GPU provides. And this calculation ignores the memory needed for activations during the forward pass.

Full fine-tuning is also not necessary. Research has shown that the weight changes during fine-tuning tend to be low-rank -- meaning they can be captured by much smaller matrices. LoRA exploits this observation.

## The Core Idea: Small Corrections to Frozen Weights

Imagine you have a large matrix W in the model (say, 4096 x 4096 in a Llama attention layer). In full fine-tuning, you would update W directly: W_new = W + delta_W, where delta_W is the change learned during training.

LoRA instead decomposes delta_W into two much smaller matrices: A (4096 x 16) and B (16 x 4096). The product A * B is a 4096 x 4096 matrix -- the same shape as the original -- but it is constructed from only 2 * 4096 * 16 = 131,072 parameters instead of 4096 * 4096 = 16,777,216 parameters. That is a 128x reduction.

During training, the original weight matrix W is frozen (not updated). Only A and B are trained. During inference, the output is computed as: output = input * W + input * A * B. The second term is the LoRA "correction" to the frozen weights.

## What "Rank" Means

The number 16 in the example above is the rank (the `r` parameter in LoraConfig). It controls the expressiveness of the correction:

- **Rank 4-8**: Very small correction. Suitable for simple tasks or when you want minimal deviation from the base model.
- **Rank 16**: The most common default. Sufficient for most instruction-tuning tasks.
- **Rank 32-64**: Higher capacity. Useful when the task requires more substantial behavioral changes, or when you have a large, diverse dataset.

Higher rank means more trainable parameters, more memory usage, and more risk of overfitting with small datasets. The relationship is linear: doubling the rank roughly doubles the number of trainable parameters.

## Alpha and the Scaling Factor

The `lora_alpha` parameter controls how strongly the LoRA correction influences the output. The effective scaling is `alpha / r`. With the common setting of `r=16, alpha=32`, the scaling factor is 2.0 -- meaning the LoRA correction is amplified by a factor of 2 relative to its raw magnitude.

The reason for this separation (rather than just training the matrices to the right magnitude) is practical: it allows you to adjust the correction strength without retraining. Some practitioners tune alpha after training to find the best balance between base model behavior and fine-tuned behavior.

## Why Certain Layers Are Targeted

In a transformer, the attention mechanism has four projection matrices (Q, K, V, O) and the MLP has two or three (gate, up, down). LoRA is typically applied to the attention projections because these are where the model learns "what to attend to" -- the core reasoning mechanism.

Including the MLP layers (gate_proj, up_proj, down_proj) increases the number of trainable parameters and can improve results, especially for tasks that require the model to learn new knowledge rather than just new behavior patterns. The cost is additional memory usage and training time.

Not all layers need LoRA. The embedding layers and the final language model head are sometimes fine-tuned fully (using the `modules_to_save` parameter) because they handle the direct mapping between tokens and vector representations.

## QLoRA: Combining Quantization with LoRA

QLoRA adds one more idea: the frozen base model weights are stored in 4-bit precision. Since these weights are never updated during training, the precision loss from quantization does not compound over training steps. The LoRA adapter weights A and B are stored and computed in higher precision (typically bfloat16).

This combination is why a 7B model can be fine-tuned on an 8 GB GPU:

- Frozen base model in 4-bit: ~3.5 GB
- LoRA adapter parameters: ~80 MB
- Optimizer states for LoRA only: ~160 MB
- Activations and overhead: ~3-4 GB (varies with batch size and sequence length)

The total comes to roughly 7-8 GB, which fits on hardware that would need 56+ GB for full fine-tuning.

## The Tradeoff

LoRA produces results that are slightly worse than full fine-tuning. Published comparisons show that the difference is small -- typically 1-3% on benchmarks -- and for many practical tasks the difference is not noticeable. The massive reduction in hardware requirements makes this a worthwhile tradeoff for nearly all local fine-tuning scenarios.

The most common failure mode with LoRA is not the technique itself but the configuration: rank too low for a complex task, wrong target modules for the model architecture, or learning rate too high causing instability. These are addressable through hyperparameter tuning.

For the parameter specifications, see the [Training Hyperparameters Reference](../reference/training-hyperparameters.md). For practical configuration steps, see the [Configure QLoRA Training Tutorial](../tutorials/configure-qlora-training.md). For adjustments, see [How to Tune Hyperparameters](../howto/tune-hyperparameters.md).
