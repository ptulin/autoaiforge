# Model Comparison Benchmarker

## Overview

The Model Comparison Benchmarker is a Python tool designed to benchmark and compare the performance of Google Gemma 4 and other open-source AI models across multiple datasets. It provides detailed metrics such as latency, accuracy, and resource utilization, enabling developers to select the best model for their specific use cases.

## Features

- Evaluate multiple AI models on multiple datasets.
- Measure performance metrics such as latency, accuracy, and memory usage.
- Export benchmarking results in JSON or CSV format.

## Installation

Install the required dependencies using pip:

```bash
pip install torch transformers pandas matplotlib
```

## Usage

Run the tool from the command line:

```bash
python model_comparison_benchmarker.py --models <model1> <model2> --datasets <dataset1.csv> <dataset2.csv> --batch-size <batch_size> --output-format <json|csv> --output-file <output_file>
```

### Arguments

- `--models`: List of model names to benchmark (e.g., `bert-base-uncased`).
- `--datasets`: List of dataset file paths (CSV format with `text` and `label` columns).
- `--batch-size`: Batch size for evaluation (default: 16).
- `--output-format`: Output format for benchmarking results (`json` or `csv`, default: `json`).
- `--output-file`: Output file path (default: `benchmark_results.json`).

## Example

```bash
python model_comparison_benchmarker.py --models bert-base-uncased roberta-base \
    --datasets dataset1.csv dataset2.csv \
    --batch-size 16 \
    --output-format json \
    --output-file results.json
```

## Testing

To run the tests, install `pytest` and execute the test file:

```bash
pip install pytest
pytest test_model_comparison_benchmarker.py
```

## License

This project is licensed under the MIT License.