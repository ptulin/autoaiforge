# Context Window Optimizer

## Overview

The Context Window Optimizer is a Python CLI tool designed to optimize the context window for AI agents by dynamically summarizing and compressing prior interactions. It ensures that the agent's context fits within a limited token budget without losing essential information.

## Features

- Estimates the token count of a given text using a specified tokenizer model.
- Summarizes text to fit within a specified token budget.
- Supports input from both text files and raw text strings.
- Default support for the GPT-2 tokenizer.

## Requirements

- Python 3.7+
- `transformers` library
- `nltk` library
- `pytest` for testing

Install the required dependencies using pip:

```bash
pip install transformers nltk pytest
```

## Usage

Run the tool from the command line:

```bash
python context_window_optimizer.py --input <input_text_or_file> --max_tokens <max_token_count> [--model <model_name>]
```

### Arguments

- `--input`: Path to the input text file or raw text.
- `--max_tokens`: Maximum token budget.
- `--model`: (Optional) Model name for tokenization. Default is `gpt2`.

### Example

Summarize a text file to fit within 50 tokens:

```bash
python context_window_optimizer.py --input example.txt --max_tokens 50
```

Summarize raw text to fit within 30 tokens:

```bash
python context_window_optimizer.py --input "This is a long text that needs to be summarized." --max_tokens 30
```

## Testing

Run the test suite using pytest:

```bash
pytest test_context_window_optimizer.py
```

The tests include:

- Estimating token count.
- Summarizing text with different token limits.
- Processing input from both files and raw strings.
- Handling empty input gracefully.
