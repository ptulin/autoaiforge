# LLM Hardware Profiler

## Overview

The LLM Hardware Profiler is a Python tool designed to benchmark the performance of large language models (LLMs) on local hardware. It measures key metrics such as:

- Memory usage
- CPU utilization
- GPU utilization (if available)
- Inference latency

This tool provides developers with insights into potential bottlenecks and helps optimize model selection for specific hardware setups.

## Features

- Supports Hugging Face Transformers models
- Measures memory usage before and after inference
- Calculates inference latency
- Reports CPU and GPU utilization
- Outputs results to the console or a JSON file

## Requirements

- Python 3.7+
- `transformers`
- `torch`
- `psutil`
- `pytest` (for testing)

## Installation

Install the required dependencies:

```bash
pip install transformers torch psutil pytest
```

## Usage

Run the tool from the command line:

```bash
python llm_hardware_profiler.py --model gpt-2 --framework huggingface --batch_size 8 --output results.json
```

### Arguments

- `--model`: Name of the model to benchmark (e.g., `gpt-2`)
- `--framework`: Framework to use (currently only `huggingface` is supported)
- `--batch_size`: Batch size for inference
- `--output`: Optional output file to save the results as JSON

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_hardware_profiler.py
```

The tests mock external dependencies to ensure they run without requiring network access or specific hardware.

## License

This project is licensed under the MIT License.