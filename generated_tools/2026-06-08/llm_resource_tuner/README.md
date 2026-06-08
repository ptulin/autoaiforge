# LLM Resource Tuner

LLM Resource Tuner is a Python CLI tool designed to help developers optimize the resource usage of large language models (LLMs). It analyzes model configurations and hardware constraints to provide recommendations for batch sizes, precision settings, and hardware-specific tweaks.

## Features
- Analyze GPU memory and suggest optimal configurations for LLMs.
- Provide recommendations for batch size and precision settings.
- Save recommendations to a YAML file for easy reference.

## Installation

Install the required dependencies:

```bash
pip install transformers pyyaml
```

## Usage

Run the CLI tool with the following options:

```bash
python llm_resource_tuner.py --model <model_name> --gpu_memory <gpu_memory> [--output <output_file>]
```

### Arguments
- `--model`: Name of the model to analyze (e.g., `gpt-3`).
- `--gpu_memory`: Available GPU memory (e.g., `8GB`).
- `--output`: (Optional) Path to save the recommendations as a YAML file.

### Example

```bash
python llm_resource_tuner.py --model gpt-3 --gpu_memory 8GB --output recommendations.yaml
```

## Testing

To run the tests, install `pytest` and execute:

```bash
pip install pytest
pytest test_llm_resource_tuner.py
```

## License

This project is licensed under the MIT License.