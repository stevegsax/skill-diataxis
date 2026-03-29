# Evaluating Your Fine-Tuned Model

In this tutorial, we will load a fine-tuned adapter, run inference, compare the fine-tuned model against the base model on the same prompts, compute a basic quality metric, and merge the LoRA weights into the base model for deployment. By the end, you will have a merged model saved to disk and a clear picture of what fine-tuning accomplished.

## Prerequisites

- Completed the [Run Training Tutorial](run-training.md)
- A saved adapter at `./results/final-adapter/`

## Step 1: Load the Base Model and Adapter

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

model_name = "meta-llama/Meta-Llama-3.1-8B"

# Load base model in 4-bit (same config as training)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load the fine-tuned adapter on top
finetuned_model = PeftModel.from_pretrained(base_model, "./results/final-adapter")
finetuned_model.eval()

print("Base model with adapter loaded successfully")
```

## Step 2: Define Test Prompts

Create a set of prompts that test the instruction-following capability:

```python
test_prompts = [
    "Explain what a hash table is in simple terms.",
    "Write a Python function that reverses a string.",
    "List three benefits of version control systems.",
    "What is the difference between TCP and UDP?",
    "Summarize what machine learning is in two sentences.",
]

def format_prompt(instruction):
    return f"### Instruction:\n{instruction}\n\n### Response:\n"
```

## Step 3: Compare Base vs Fine-Tuned Outputs

First, generate with the fine-tuned model:

```python
def generate_response(model, prompt, max_tokens=256):
    inputs = tokenizer(format_prompt(prompt), return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
        )
    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract just the response part
    if "### Response:" in full_text:
        return full_text.split("### Response:")[-1].strip()
    return full_text

print("=" * 60)
print("FINE-TUNED MODEL OUTPUTS")
print("=" * 60)

finetuned_responses = []
for prompt in test_prompts:
    response = generate_response(finetuned_model, prompt)
    finetuned_responses.append(response)
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response[:300]}")
    print("-" * 40)
```

Now generate with the base model (without the adapter) for comparison:

```python
# Disable the adapter to get base model behavior
finetuned_model.disable_adapter_layers()

print("=" * 60)
print("BASE MODEL OUTPUTS (no fine-tuning)")
print("=" * 60)

base_responses = []
for prompt in test_prompts:
    response = generate_response(finetuned_model, prompt)
    base_responses.append(response)
    print(f"\nPrompt: {prompt}")
    print(f"Response: {response[:300]}")
    print("-" * 40)

# Re-enable the adapter
finetuned_model.enable_adapter_layers()
```

You should see a clear difference. The base model may continue the prompt as if completing text, while the fine-tuned model follows the instruction and provides a direct answer.

## Step 4: Compute a Simple Quality Score

A manual scoring rubric for instruction following:

```python
def score_response(prompt, response):
    """Simple heuristic quality score (0-3)."""
    score = 0
    # Does it actually answer the question?
    if len(response) > 20:
        score += 1
    # Is it reasonably concise (not rambling)?
    if len(response) < 1000:
        score += 1
    # Does it not repeat the instruction back?
    if prompt.lower() not in response.lower():
        score += 1
    return score

print("\nQuality Comparison:")
print(f"{'Prompt':<45} | Base | Fine-tuned")
print("-" * 70)
for i, prompt in enumerate(test_prompts):
    base_score = score_response(prompt, base_responses[i])
    ft_score = score_response(prompt, finetuned_responses[i])
    print(f"{prompt[:43]:<45} | {base_score}/3  | {ft_score}/3")
```

This is a rough heuristic. For more rigorous evaluation, see [Evaluation Strategies](../explanation/evaluation-strategies.md).

## Step 5: Merge LoRA Weights into the Base Model

For deployment, you can merge the LoRA weights into the base model so you no longer need the separate adapter:

```python
from peft import AutoPeftModelForCausalLM

# Load in float16 for merging (cannot merge quantized model directly)
merge_model = AutoPeftModelForCausalLM.from_pretrained(
    "./results/final-adapter",
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True,
)

merged_model = merge_model.merge_and_unload()
merged_model.save_pretrained("./results/merged-model")
tokenizer.save_pretrained("./results/merged-model")

print("Merged model saved to ./results/merged-model")
```

The merged model is a standard Hugging Face model that can be loaded without PEFT.

## What You Accomplished

You have:

- Loaded a fine-tuned adapter on a base model
- Compared base vs fine-tuned model outputs on the same prompts
- Seen the concrete effect of instruction fine-tuning
- Computed basic quality scores
- Merged LoRA weights into a standalone model for deployment

## Next Steps

- [How to Iterate on Results](../howto/iterate-on-results.md) -- improve your fine-tuned model
- [Evaluation Strategies](../explanation/evaluation-strategies.md) -- deeper discussion of evaluation methods
- [How to Choose a Base Model](../howto/choose-base-model.md) -- try different base models

## Exercises

Work through the [Model Evaluation Exercise](../exercises/model-evaluation.py) to practice evaluation techniques.
