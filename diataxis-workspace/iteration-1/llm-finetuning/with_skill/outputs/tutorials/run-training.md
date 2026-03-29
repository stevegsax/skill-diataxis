# Running Training

In this tutorial, we will start a training run, observe the training logs, monitor GPU usage, save the resulting adapter, and test the fine-tuned model with a sample prompt. This is where you see the results of all the previous setup.

## Prerequisites

- Completed the [Configure QLoRA Training Tutorial](configure-qlora-training.md)
- A configured `trainer` object ready to call `.train()`

For a quick run, we will use a 1000-example subset so training completes in minutes rather than hours.

## Step 1: (Optional) Subset for a Quick Test

If you want results fast (recommended for your first run):

```python
small_train = train_data.select(range(1000))
small_val = val_data.select(range(200))

# Recreate trainer with the subset
from trl import SFTTrainer
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=small_train,
    eval_dataset=small_val,
    processing_class=tokenizer,
    max_seq_length=512,
)
```

With 1000 examples, batch size 4, and gradient accumulation 4, you get about 62 steps per epoch. On an RTX 3090, this takes approximately 5 minutes.

## Step 2: Start Training

```python
trainer.train()
```

You should see output like this:

```
{'loss': 1.8234, 'grad_norm': 0.5421, 'learning_rate': 0.0002, 'epoch': 0.16}
{'loss': 1.4521, 'grad_norm': 0.3812, 'learning_rate': 0.00019, 'epoch': 0.32}
{'loss': 1.2103, 'grad_norm': 0.2934, 'learning_rate': 0.00017, 'epoch': 0.48}
...
```

Notice:

- **loss** decreases over time -- the model is learning
- **grad_norm** stays stable -- training is not diverging
- **learning_rate** decreases following the cosine schedule

If you see `loss: nan`, stop training and see [How to Troubleshoot Training Issues](../howto/troubleshoot-training.md).

## Step 3: Monitor GPU Memory

While training runs, you can check GPU usage from another terminal:

```bash
nvidia-smi
```

Or within Python:

```python
print(f"GPU memory allocated: {torch.cuda.memory_allocated() / 1e9:.1f} GB")
print(f"GPU memory reserved: {torch.cuda.memory_reserved() / 1e9:.1f} GB")
```

With QLoRA on an 8B model, batch size 4, and gradient checkpointing, you should see approximately 8-12 GB of VRAM in use during training.

## Step 4: Save the Adapter

After training completes, save the LoRA adapter weights:

```python
trainer.save_model("./results/final-adapter")
tokenizer.save_pretrained("./results/final-adapter")

print("Adapter saved. Files:")
import os
for f in os.listdir("./results/final-adapter"):
    size = os.path.getsize(f"./results/final-adapter/{f}") / 1e6
    print(f"  {f}: {size:.1f} MB")
```

You should see:

```
Adapter saved. Files:
  adapter_config.json: 0.0 MB
  adapter_model.safetensors: 167.8 MB
  tokenizer.json: 17.5 MB
  ...
```

Notice the adapter is only ~168 MB, not the full 16 GB of the base model. You only save the LoRA weights.

## Step 5: Test the Fine-Tuned Model

Now let's see if fine-tuning worked. Generate a response with the fine-tuned model:

```python
model.eval()

prompt = "### Instruction:\nExplain the difference between a list and a tuple in Python.\n\n### Response:\n"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True,
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

You should see a coherent response that follows the instruction. The response quality will be modest with only 1000 training examples, but it demonstrates that the model has learned the instruction-following pattern.

## Step 6: View the Training Loss Curve

```python
import json

log_history = trainer.state.log_history
train_losses = [(entry["step"], entry["loss"]) for entry in log_history if "loss" in entry]

print("Step | Loss")
print("-----|------")
for step, loss in train_losses:
    bar = "#" * int((2.0 - loss) * 20) if loss < 2.0 else ""
    print(f"{step:5d} | {loss:.4f} {bar}")
```

You should see loss decreasing over steps, which confirms the model is learning from the data.

## What You Accomplished

You have:

- Run a complete fine-tuning training loop
- Monitored training loss and GPU usage
- Saved a LoRA adapter (small file, not the full model)
- Tested the fine-tuned model and seen it respond to instructions

## Next Steps

- [Evaluate Model Tutorial](evaluate-model.md) -- systematic evaluation and model merging
- [How to Troubleshoot Training Issues](../howto/troubleshoot-training.md) -- fix common problems
- [How to Iterate on Results](../howto/iterate-on-results.md) -- improve your model
- [Evaluation Strategies](../explanation/evaluation-strategies.md) -- understanding model quality

## Exercises

Work through the [Run and Evaluate Exercise](../exercises/run-and-evaluate.py) to run training and compare outputs.
