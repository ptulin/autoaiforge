# Quantization Benchmark Tool

## Description
The Quantization Benchmark Tool is a command-line interface (CLI) utility designed to help developers evaluate the performance impact of various quantization techniques on pre-trained language models. It benchmarks memory usage, inference speed, and model accuracy for methods like GGUF, GPTQ, and AWQ, enabling informed decisions for resource-constrained environments.

## Features
- **Multiple Quantization Methods**: Supports GGUF, GPTQ, and AWQ.
- **Performance Metrics**: Benchmarks memory usage, inference speed, and accuracy.
- **Custom Datasets**: Allows evaluation on user-provided datasets.
- **Flexible Output**: Generates summary reports in JSON or CSV format.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool with the following command:

```bash
python quantization_benchmark.py --model model.pth --methods GGUF GPTQ --dataset eval_data.json --output json
```

### Arguments
- `--model`: Path to the pre-trained model.
- `--methods`: List of quantization methods to test (e.g., GGUF, GPTQ, AWQ).
- `--dataset`: (Optional) Path to the evaluation dataset in JSON format.
- `--output`: Output format for the summary report (`json` or `csv`).

## Example

```bash
python quantization_benchmark.py --model model.pth --methods GGUF GPTQ --dataset eval_data.json --output csv
```

## Limitations
- The quantization methods (GGUF, GPTQ, AWQ) are placeholders and need to be implemented.
- Accuracy computation is currently a dummy implementation and should be replaced with a proper evaluation metric.

## License
This project is licensed under the MIT License.