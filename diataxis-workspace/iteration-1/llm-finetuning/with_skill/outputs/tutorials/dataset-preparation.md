# Preparing a Dataset for Fine-Tuning

In this tutorial, we will take a public dataset from Hugging Face Hub, convert it into instruction-tuning format, tokenize it, and produce a training-ready dataset object. Along the way, we will inspect the data at every step so you can see exactly what transformations are happening.

## Prerequisites

- Completed the [Environment Setup Tutorial](environment-setup.md)
- A working Python environment with transformers, datasets, and tokenizers installed

## Step 1: Load a Dataset from Hugging Face Hub

We will use the Alpaca dataset, a well-known instruction-tuning dataset:

```python
from datasets import load_dataset

dataset = load_dataset("tatsu-lab/alpaca", split="train")
print(f"Number of examples: {len(dataset)}")
print(f"Columns: {dataset.column_names}")
print(dataset[0])
```

You should see output like:

```
Number of examples: 52002
Columns: ['instruction', 'input', 'output', 'text']
{'instruction': 'Give three tips for staying healthy.',
 'input': '',
 'output': '1. Eat a balanced diet...',
 'text': 'Below is an instruction...'}
```

Notice the dataset has `instruction`, `input`, `output`, and `text` fields. We will use the first three to build our prompt template.

## Step 2: Understand the Alpaca Format

Each example has three fields that matter:

- **instruction**: The task description
- **input**: Optional additional context (often empty)
- **output**: The expected model response

Let's look at an example with input:

```python
with_input = [ex for ex in dataset if ex['input'] != '']
print(with_input[0])
```

You should see an example where `input` provides context that the instruction refers to.

## Step 3: Create a Prompt Template

We need a function that converts each example into a single formatted string. The model learns to generate the text after `### Response:`:

```python
def format_alpaca(example):
    if example["input"]:
        text = (
            f"### Instruction:\n{example['instruction']}\n\n"
            f"### Input:\n{example['input']}\n\n"
            f"### Response:\n{example['output']}"
        )
    else:
        text = (
            f"### Instruction:\n{example['instruction']}\n\n"
            f"### Response:\n{example['output']}"
        )
    return {"formatted_text": text}
```

Apply it to the dataset:

```python
dataset = dataset.map(format_alpaca)
print(dataset[0]["formatted_text"])
```

You should see a cleanly formatted prompt with the instruction and response sections clearly separated.

## Step 4: Split into Train and Validation Sets

```python
split = dataset.train_test_split(test_size=0.05, seed=42)
train_data = split["train"]
val_data = split["test"]

print(f"Training examples: {len(train_data)}")
print(f"Validation examples: {len(val_data)}")
```

You should see:

```
Training examples: 49401
Validation examples: 2601
```

## Step 5: Tokenize and Inspect Token Lengths

Load a tokenizer for the model we will fine-tune (we will use this same model later):

```python
from transformers import AutoTokenizer

model_name = "meta-llama/Meta-Llama-3.1-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
```

Now tokenize and check lengths:

```python
def count_tokens(example):
    tokens = tokenizer(example["formatted_text"])
    return {"token_count": len(tokens["input_ids"])}

train_data = train_data.map(count_tokens)

import statistics
lengths = train_data["token_count"]
print(f"Min tokens: {min(lengths)}")
print(f"Max tokens: {max(lengths)}")
print(f"Median tokens: {statistics.median(lengths):.0f}")
print(f"95th percentile: {sorted(lengths)[int(0.95 * len(lengths))]}")
```

You should see something like:

```
Min tokens: 20
Max tokens: 1847
Median tokens: 82
95th percentile: 312
```

This tells us most examples are short. We will set a `max_seq_length` of 512, which covers over 95% of examples without wasting memory on padding.

## Step 6: Verify the Final Dataset

```python
print(f"Training set: {len(train_data)} examples")
print(f"Validation set: {len(val_data)} examples")
print(f"Columns: {train_data.column_names}")
print("\nSample formatted text (first 200 chars):")
print(train_data[0]["formatted_text"][:200])
```

You should see the dataset with the `formatted_text` column ready for the SFTTrainer.

## What You Accomplished

You now have:

- A loaded and inspected instruction-tuning dataset
- A prompt template function that formats examples consistently
- Train/validation splits
- Token length statistics to guide `max_seq_length` selection
- A dataset object ready to pass to the training configuration step

## Next Steps

- [Configure QLoRA Training Tutorial](configure-qlora-training.md) -- set up the training run
- [How to Prepare a Custom Dataset](../howto/prepare-custom-dataset.md) -- use your own data
- [Dataset Formats Reference](../reference/dataset-formats.md) -- Alpaca, ChatML, ShareGPT specs
- [Why Data Format Matters](../explanation/why-data-format-matters.md) -- why these templates work

## Exercises

Work through the [Dataset Formatting Exercise](../exercises/dataset-formatting.py) to practice converting different data formats.
