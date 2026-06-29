# LLM Edge Runner

## Overview

LLM Edge Runner is a Python tool designed to efficiently run large language models (LLMs) on local devices or edge hardware. It optimizes model loading, resource allocation, and execution, while including failover mechanisms to handle resource constraints. When resources are insufficient, the tool gracefully falls back to smaller models or pre-defined responses.

## Features

- Load and run large language models locally or on edge devices.
- Check system resources to determine available memory.
- Automatically fallback to pre-defined responses when resources are insufficient.

## Requirements

- Python 3.8+
- Install the following Python packages:
  - `torch`
  - `transformers`
  - `psutil`

Install the required packages using pip:
```bash
pip install torch transformers psutil
```

## Usage

Run the tool using the command line:
```bash
python llm_edge_runner.py --model <model_name_or_path> --fallback <fallback_json_path> --input <input_text>
```

### Arguments

- `--model`: Path or name of the model to load (e.g., `gpt2`).
- `--fallback`: Path to a JSON file containing fallback responses.
- `--input`: Input text for the model.

### Example

```bash
python llm_edge_runner.py --model gpt2 --fallback fallback.json --input "Hello, how are you?"
```

## Testing

To run the tests, install `pytest`:
```bash
pip install pytest
```

Run the tests:
```bash
pytest test_llm_edge_runner.py
```

The tests include:
- Model loading.
- Resource checking.
- Fallback response loading.
- Model execution.
- Main function behavior under low memory conditions.

All tests are designed to run without network access by mocking external dependencies.