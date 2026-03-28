# AI Model Comparator

## Overview

AI Model Comparator is a Python tool for benchmarking and comparing the performance of open-source AI models across tasks. It allows developers to run evaluation datasets through multiple models and generate side-by-side comparisons of metrics like accuracy, latency, and perplexity.

## Features

- Evaluate AI models on tasks such as summarization and text classification.
- Generate performance metrics including average latency and number of samples processed.
- Export results in CSV or JSON format.

## Installation

Install the required dependencies using pip:

```bash
pip install transformers numpy pandas
```

## Usage

Run the tool from the command line:

```bash
python ai_model_comparator.py --models model1 model2 --task summarization --dataset dataset.json --output csv
```

### Arguments

- `--models`: List of model names or paths.
- `--task`: Task type (`summarization` or `text-classification`).
- `--dataset`: Path to the evaluation dataset in JSON format.
- `--output`: Output format (`csv` or `json`).

## Testing

Run the tests using pytest:

```bash
pytest test_ai_model_comparator.py
```

## License

This project is licensed under the MIT License.