# Understanding Model Sizes and Quantization

Choosing a model size for local fine-tuning involves a tension between capability and hardware constraints. This discussion explores why parameter count matters, what quantization actually does, and why the relationship between model size and quality is not as straightforward as it first appears.

## Parameters and Capability

An LLM's parameter count -- 7B, 13B, 70B -- refers to the number of learnable weights in the model. More parameters generally mean the model can represent more complex patterns and store more knowledge. A 70B model has seen the same training data as a 7B model from the same family, but it has more capacity to internalize that data.

However, the relationship between parameter count and capability is not linear. Doubling the parameters does not double the quality. Benchmark scores tend to follow a logarithmic curve: the jump from 3B to 7B is substantial, the jump from 7B to 13B is noticeable, and the jump from 13B to 34B is there but diminishing. Beyond 70B, improvements become incremental for most tasks.

This matters for fine-tuning because you do not need the most capable base model -- you need one that is *capable enough* for your specific task. A 7B model fine-tuned on domain-specific data often outperforms a general-purpose 70B model on that domain. The fine-tuning compensates for the smaller model's lower general capability by focusing its capacity on what you actually care about.

## What Quantization Does

A model parameter is typically stored as a 16-bit floating-point number (fp16), using 2 bytes. A 7B-parameter model therefore requires 14 GB just to hold the weights in memory -- before accounting for optimizer states, activations, and gradients.

Quantization reduces the precision of these numbers. In 4-bit quantization, each weight is represented with just 4 bits (0.5 bytes) instead of 16. This cuts the memory required for a 7B model from 14 GB to about 3.5 GB. The actual VRAM usage is higher (around 5 GB) because some overhead is involved in the dequantization process.

The technique used in QLoRA is called NF4 (Normal Float 4), which is designed specifically for neural network weights. It works on the observation that pre-trained model weights tend to follow a normal distribution. NF4 maps the 16 possible 4-bit values to optimal positions along this distribution, minimizing the quantization error.

## What Quantization Trades Away

Quantization is not free. Reducing a weight from 16 bits to 4 bits loses information. The model's outputs will not be identical to the fp16 version. In practice, the degradation from 4-bit quantization is surprisingly small for inference -- outputs are nearly indistinguishable for most use cases.

For training, the story is more nuanced. In QLoRA, the base model weights are frozen in 4-bit, and only the LoRA adapters (which are in higher precision) are trained. The quantized base model computes forward passes with some precision loss, which means the gradients used to update the LoRA adapters are approximate. Research has shown that this approximation has minimal impact on final quality, but it is not zero.

The practical implication: a model fine-tuned with QLoRA will be very slightly worse than the same model fine-tuned with full fp16 LoRA. On consumer hardware, this tradeoff is almost always worth making because it enables training models that would otherwise not fit in memory at all.

## The Specialist vs Generalist Dynamic

One of the most counterintuitive aspects of fine-tuning is that a small, fine-tuned model can outperform a much larger general model on specific tasks. A 7B model fine-tuned on 5,000 high-quality medical Q&A examples will typically answer medical questions better than a general-purpose 70B model that was not fine-tuned for medicine.

The reason is that fine-tuning concentrates the model's capacity. The base model distributes its parameters across all the knowledge and patterns it learned during pre-training. Fine-tuning adjusts a small subset of parameters (via LoRA) to emphasize the patterns relevant to your task, effectively specializing the model without destroying its general knowledge.

This is why the model selection decision is not simply "pick the biggest model you can run." A smaller model that fine-tunes well on your specific task may be more useful than a larger model that is too general.

## Practical Guidance Without Prescriptions

The right model size depends on your task complexity, your data quality, and your patience for training time. A reasonable approach is to start with a 7-8B model (the Llama 3.1 8B or Qwen 2.5 7B are strong defaults as of early 2026), verify that fine-tuning works end-to-end, and only move to a larger model if the results are insufficient.

For the factual comparison of available models, see the [Model Comparison Reference](../reference/model-comparison.md). For a step-by-step model selection process, see [How to Choose a Base Model](../howto/choose-base-model.md).
