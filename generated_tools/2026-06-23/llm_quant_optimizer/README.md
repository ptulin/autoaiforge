# LLM Quantization Optimizer

## Overview

The LLM Quantization Optimizer is a Python tool designed to optimize locally hosted large language models (LLMs) by applying quantization techniques such as 8-bit or 4-bit quantization. This optimization reduces memory usage and improves inference speed while maintaining acceptable accuracy. The tool also benchmarks the quantized models and generates a report with performance metrics.

## Features

- Supports 8-bit and 4-bit quantization methods.
- Benchmarks the quantized model's inference time.
- Saves a detailed report in JSON format.

## Requirements

- Python 3.7+
- `torch`
- `transformers`

Install the required dependencies using pip:

```bash
pip install torch transformers
```

## Usage

Run the tool using the command line:

```bash
python llm_quant_optimizer.py --model <path_to_model> --quantization <8bit|4bit> [--output <output_path>]
```

### Arguments

- `--model`: Path to the locally stored LLM model.
- `--quantization`: Quantization method to apply (`8bit` or `4bit`).
- `--output`: (Optional) Path to save the quantization report. Default is `quantization_report.json`.

### Example

```bash
python llm_quant_optimizer.py --model ./my_model --quantization 8bit --output ./output_report.json
```

## Testing

To run the tests, install `pytest` and execute the following command:

```bash
pytest test_llm_quant_optimizer.py
```

The tests include:

1. Verifying behavior when the model path is invalid.
2. Ensuring an error is raised for invalid quantization methods.
3. Testing successful quantization with mocked model and tokenizer.
4. Benchmarking the model with mocked inference time.
5. Verifying the report is saved correctly.

## Notes

- This tool assumes the model is locally stored and accessible at the specified path.
- The tool does not support downloading models from the internet.
- Ensure the model is compatible with the `transformers` library.