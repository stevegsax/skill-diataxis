# Dataset Formats Reference

## Alpaca Format

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `instruction` | string | Yes | The task or question for the model |
| `input` | string | No | Additional context for the instruction (empty string if none) |
| `output` | string | Yes | The expected model response |

### Prompt Template

Without input:

```
### Instruction:
{instruction}

### Response:
{output}
```

With input:

```
### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}
```

### Minimal Example

```json
{
    "instruction": "Summarize the following text.",
    "input": "The quick brown fox jumps over the lazy dog.",
    "output": "A fox jumps over a dog."
}
```

## ChatML Format

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `messages` | array | Yes | Array of message objects |
| `messages[].role` | string | Yes | One of: `system`, `user`, `assistant` |
| `messages[].content` | string | Yes | The message text |

### Prompt Template

```
<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{user_message}<|im_end|>
<|im_start|>assistant
{assistant_message}<|im_end|>
```

### Special Tokens

| Token | Purpose |
|-------|---------|
| `<\|im_start\|>` | Start of a message turn |
| `<\|im_end\|>` | End of a message turn |

### Minimal Example

```json
{
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2+2?"},
        {"role": "assistant", "content": "4"}
    ]
}
```

### Compatible Models

ChatML is natively supported by: Qwen, Phi-3, Yi, and models with "chat" or "instruct" variants that specify ChatML in their model card.

## ShareGPT Format

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `conversations` | array | Yes | Array of turn objects |
| `conversations[].from` | string | Yes | One of: `human`, `gpt`, `system` |
| `conversations[].value` | string | Yes | The message text |

### Minimal Example

```json
{
    "conversations": [
        {"from": "human", "value": "Explain photosynthesis."},
        {"from": "gpt", "value": "Photosynthesis is the process by which plants convert sunlight into energy..."}
    ]
}
```

### Notes

- ShareGPT format is commonly used in community datasets
- TRL's SFTTrainer can handle ShareGPT format directly with the `dataset_text_field` parameter or by converting to ChatML

## Hugging Face Datasets Library Key Functions

| Function | Purpose | Key Parameters |
|----------|---------|----------------|
| `load_dataset(path)` | Load from Hub or local files | `path`: Hub ID or file path; `split`: which split |
| `Dataset.from_pandas(df)` | Convert pandas DataFrame | `df`: the DataFrame |
| `Dataset.from_list(data)` | Convert list of dicts | `data`: list of dictionaries |
| `dataset.map(fn)` | Apply transformation | `fn`: function; `batched`: process in batches |
| `dataset.filter(fn)` | Filter examples | `fn`: predicate function |
| `dataset.train_test_split(test_size)` | Split dataset | `test_size`: fraction (0.0-1.0) or count |
| `dataset.select(indices)` | Select by index | `indices`: list or range |
| `dataset.shuffle(seed)` | Randomize order | `seed`: random seed for reproducibility |

## Token Length and Truncation

| Parameter | Location | Description |
|-----------|----------|-------------|
| `max_seq_length` | SFTTrainer | Maximum token length; longer examples are truncated |
| `packing` | SFTTrainer | Pack multiple short examples into one sequence (saves memory) |
| `dataset_text_field` | SFTTrainer | Column name containing the formatted text |

### Recommended `max_seq_length` by Use Case

| Use Case | Typical Length | Recommended `max_seq_length` |
|----------|---------------|------------------------------|
| Short Q&A | 50-200 tokens | 256 |
| Instructions | 100-500 tokens | 512 |
| Long-form writing | 500-2000 tokens | 1024 or 2048 |
| Code generation | 200-1500 tokens | 1024 |

Set `max_seq_length` to cover the 95th percentile of your data's token lengths.

For a hands-on walkthrough, see the [Dataset Preparation Tutorial](../tutorials/dataset-preparation.md). For guidance on using your own data, see [How to Prepare a Custom Dataset](../howto/prepare-custom-dataset.md).
