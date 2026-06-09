# LLM Quantization Evaluator

## Overview
The `llm_quantization_eval` tool evaluates the performance of quantized versions of large language models (LLMs), comparing them against full-precision models in terms of speed, memory usage, and accuracy. This helps developers understand the trade-offs of model quantization for their specific workloads.

## Features
- Quantize models using INT8 or FP16 precision.
- Evaluate model accuracy on a given dataset.
- Benchmark model performance in terms of inference time and memory usage.

## Requirements
- Python 3.8+
- Required Python packages:
  - `torch`
  - `transformers`
  - `datasets`
  - `pytest` (for testing)

Install the required packages using:
```bash
pip install torch transformers datasets pytest
```

## Usage
Run the tool from the command line:
```bash
python llm_quantization_eval.py --model <model_name> --quantization <INT8|FP16> --dataset <dataset_name> --device <cpu|cuda>
```

### Example
```bash
python llm_quantization_eval.py --model gpt2 --quantization INT8 --dataset squad --device cpu
```

## Testing
To run the tests, use:
```bash
pytest test_llm_quantization_eval.py
```

The tests include:
- Verifying the quantization methods.
- Testing the evaluation of model accuracy with mocked data.
- Testing the benchmarking of model performance with mocked data.
