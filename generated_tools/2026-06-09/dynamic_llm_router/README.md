# Dynamic LLM Router

## Overview

The Dynamic LLM Router is a Python tool designed to route incoming requests to different large language models (LLMs) based on resource availability and input size. This enables efficient utilization of compute resources, making it ideal for scenarios where multiple models or devices are available and load balancing is critical.

## Features

- Dynamically checks the availability of compute resources (CPU and GPU).
- Routes requests to the most suitable model and device based on resource availability.
- Supports multiple LLMs and devices.

## Requirements

- Python 3.7+
- `transformers`
- `torch`
- `psutil`
- `pytest` (for testing)

## Installation

Install the required dependencies using pip:

```bash
pip install transformers torch psutil pytest
```

## Usage

Run the tool from the command line:

```bash
python dynamic_llm_router.py --input "Your input text here" --models "gpt2,EleutherAI/gpt-neo-125M" --devices "cuda,cpu"
```

### Arguments

- `--input`: The input text to be processed by the LLM.
- `--models`: A comma-separated list of model names (e.g., `gpt2,EleutherAI/gpt-neo-125M`).
- `--devices`: A comma-separated list of devices to use (e.g., `cuda,cpu`).

### Example

```bash
python dynamic_llm_router.py --input "What is the capital of France?" --models "gpt2" --devices "cpu"
```

## Testing

Run the test suite using pytest:

```bash
pytest test_dynamic_llm_router.py
```

The test suite includes:

1. Testing device availability detection.
2. Testing successful routing of a request to an available model and device.
3. Testing behavior when no devices are available.
4. Testing behavior when model loading fails.

## License

This project is licensed under the MIT License.