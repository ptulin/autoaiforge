# LLM Input Optimizer

## Overview

LLM Input Optimizer is a Python tool designed to help developers optimize their input prompts for large language models (LLMs) such as GPT-4 or Claude-v1. The tool analyzes input prompts for clarity, length, and structure, providing suggestions to maximize model performance and minimize token usage.

## Features

- **Token Count Analysis**: Calculates the number of tokens in a prompt.
- **Cost Estimation**: Estimates the cost of processing a prompt based on token count and model pricing.
- **Optimization Suggestions**: Provides actionable suggestions to improve prompt clarity and efficiency.

## Installation

This tool does not require any external dependencies beyond Python's standard library.

## Usage

### Command Line Interface

Run the tool from the command line:

```bash
python llm_input_optimizer.py --input "Your prompt here" --model gpt-4
```

You can also pass a JSON array of prompts:

```bash
python llm_input_optimizer.py --input '["Prompt 1", "Prompt 2"]' --model gpt-4
```

### Library Usage

Import the library and use its functions in your Python code:

```python
from llm_input_optimizer import optimize_prompt

results = optimize_prompt("Your prompt here", "gpt-4")
print(results)
```

## Testing

Run tests using `pytest`:

```bash
pytest test_llm_input_optimizer.py
```

## License

This project is licensed under the MIT License.