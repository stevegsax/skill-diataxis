# How to Prepare a Custom Dataset for Fine-Tuning

This guide shows you how to convert your own data into instruction-tuning format suitable for fine-tuning with SFTTrainer.

## How to Convert a CSV File

1. Load your CSV with pandas:

    ```python
    import pandas as pd
    from datasets import Dataset

    df = pd.read_csv("my_data.csv")
    ```

2. Map your columns to the Alpaca format. Suppose your CSV has `question` and `answer` columns:

    ```python
    def to_alpaca(row):
        return {
            "instruction": row["question"],
            "input": "",
            "output": row["answer"],
        }

    df_formatted = df.apply(to_alpaca, axis=1, result_type="expand")
    dataset = Dataset.from_pandas(df_formatted)
    ```

3. Apply the prompt template:

    ```python
    def format_alpaca(example):
        return {
            "formatted_text": (
                f"### Instruction:\n{example['instruction']}\n\n"
                f"### Response:\n{example['output']}"
            )
        }

    dataset = dataset.map(format_alpaca)
    ```

## How to Convert a JSON File

1. Load JSON where each entry has your data fields:

    ```python
    from datasets import Dataset
    import json

    with open("my_data.json") as f:
        data = json.load(f)

    dataset = Dataset.from_list(data)
    ```

2. Map fields and apply the prompt template as shown above.

## How to Handle Multi-Turn Conversation Data

1. If your data has conversation turns, concatenate them with role markers:

    ```python
    def format_conversation(example):
        turns = example["messages"]  # [{"role": "user", "content": "..."}, ...]
        text_parts = []
        for turn in turns:
            if turn["role"] == "user":
                text_parts.append(f"### Instruction:\n{turn['content']}\n")
            elif turn["role"] == "assistant":
                text_parts.append(f"### Response:\n{turn['content']}\n")
        return {"formatted_text": "\n".join(text_parts)}
    ```

2. Alternatively, use the ChatML format if your model supports it:

    ```python
    def format_chatml(example):
        text_parts = []
        for turn in example["messages"]:
            text_parts.append(f"<|im_start|>{turn['role']}\n{turn['content']}<|im_end|>")
        return {"formatted_text": "\n".join(text_parts)}
    ```

Refer to the [Dataset Formats Reference](../reference/dataset-formats.md) for the full ChatML specification.

## How to Filter and Deduplicate Training Data

1. Remove exact duplicates:

    ```python
    df = df.drop_duplicates(subset=["instruction", "output"])
    ```

2. Remove near-duplicates by normalizing whitespace and casing:

    ```python
    df["norm_instruction"] = df["instruction"].str.lower().str.strip()
    df = df.drop_duplicates(subset=["norm_instruction"])
    df = df.drop(columns=["norm_instruction"])
    ```

3. Filter out very short or very long examples:

    ```python
    df = df[df["output"].str.len() > 10]
    df = df[df["output"].str.len() < 5000]
    ```

## How to Balance Dataset Categories

1. If your data has category labels, check the distribution:

    ```python
    print(df["category"].value_counts())
    ```

2. Undersample overrepresented categories:

    ```python
    target_count = df["category"].value_counts().median()
    balanced = df.groupby("category").apply(
        lambda x: x.sample(n=min(len(x), int(target_count)), random_state=42)
    ).reset_index(drop=True)
    ```

3. Alternatively, oversample underrepresented categories by duplicating rows:

    ```python
    target_count = df["category"].value_counts().max()
    oversampled = df.groupby("category").apply(
        lambda x: x.sample(n=int(target_count), replace=True, random_state=42)
    ).reset_index(drop=True)
    ```

For background on why data balance matters, see [Why Data Format Matters](../explanation/why-data-format-matters.md).
