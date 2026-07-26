# Micro LLM Splitter

## Overview

The Micro LLM Splitter is a Python tool designed to split large language models into smaller, manageable sub-models that can fit within the memory constraints of microcontrollers. It partitions weights intelligently and adds logic for distributed inference across microcontroller clusters.

## Features

- Splits large language models into smaller sub-models based on a specified memory limit.
- Saves the sub-models to disk for easy deployment.
- Supports models from the Hugging Face Transformers library.

## Installation

Install the required dependencies:

```bash
pip install transformers numpy
```

## Usage

Run the tool from the command line:

```bash
python micro_llm_splitter.py --model_name <model_name> --max_memory <max_memory_in_MB> --output_dir <output_directory>
```

### Arguments

- `--model_name`: The name of the Hugging Face model to split.
- `--max_memory`: Maximum memory (in MB) allowed for each sub-model.
- `--output_dir`: Directory to save the sub-models.

### Example

```bash
python micro_llm_splitter.py --model_name bert-base-uncased --max_memory 500 --output_dir ./sub_models
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_micro_llm_splitter.py
```

## License

This project is licensed under the MIT License.