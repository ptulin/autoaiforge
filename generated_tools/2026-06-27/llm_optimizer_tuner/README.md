# LLM Optimizer Tuner

## Overview

`llm_optimizer_tuner` is a Python tool designed to help developers benchmark and tune routing configurations for multiple LLMs. It simulates various task workloads and provides analytics to refine routing strategies.

## Features

- Simulate workloads for different LLM routing configurations.
- Generate performance metrics including latency and cost.
- Export performance metrics to a CSV report.

## Installation

Install the required dependencies using pip:

```bash
pip install pyyaml numpy pandas matplotlib
```

## Usage

Run the tool from the command line:

```bash
python llm_optimizer_tuner.py <config_file> <tasks_file> [--output <output_file>]
```

### Arguments

- `<config_file>`: Path to the routing configuration file (YAML format).
- `<tasks_file>`: Path to the sample tasks file (JSON format).
- `[--output <output_file>]`: (Optional) Path to save the performance metrics report. Default is `report.csv`.

### Example

```bash
python llm_optimizer_tuner.py config.yaml tasks.json --output metrics_report.csv
```

## Configuration File Format

The configuration file should be in YAML format and define routing configurations for different task types. Example:

```yaml
classification:
  model: model_a
translation:
  model: model_b
```

## Tasks File Format

The tasks file should be a JSON array of task objects. Each task object should have the following structure:

```json
[
  {"name": "task1", "type": "classification"},
  {"name": "task2", "type": "translation"}
]
```

## Testing

Run the tests using pytest:

```bash
pytest test_llm_optimizer_tuner.py
```

## License

This project is licensed under the MIT License.