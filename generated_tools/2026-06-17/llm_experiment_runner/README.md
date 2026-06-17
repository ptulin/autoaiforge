# LLM Experiment Runner

## Overview

The LLM Experiment Runner is a CLI tool for running experiments with open-weight large language models (LLMs). It allows developers to:

- Load pre-trained models
- Run inference on custom datasets
- Measure latency and benchmark performance

This tool is particularly useful for evaluating LLMs for specific tasks or environments.

## Features

- Load pre-trained models using the `transformers` library
- Run inference on text datasets
- Compute performance metrics such as mean, max, and min latency
- Save results and metrics to a JSON file

## Installation

Install the required dependencies:

```bash
pip install torch transformers numpy
```

## Usage

Run the tool from the command line:

```bash
python llm_experiment_runner.py --dataset <path_to_dataset> --model <model_name> [--output <output_file>]
```

### Arguments

- `--dataset`: Path to the text dataset file (required)
- `--model`: Name of the pre-trained model to load (required)
- `--output`: Path to save the results as a JSON file (optional)

### Example

```bash
python llm_experiment_runner.py --dataset data.txt --model gpt2 --output results.json
```

## Testing

Run the test suite using `pytest`:

```bash
pytest test_llm_experiment_runner.py
```

## License

This project is licensed under the MIT License.