# Local LLM Launcher

## Description

Local LLM Launcher is a Python CLI tool designed to simplify the process of launching large language models on local devices. It provides a unified interface for configuring model paths, memory allocation, and hardware acceleration.

## Features

- Load large language models locally.
- Configure device settings (CPU/GPU).
- Parse configuration files for model settings.

## Installation

Install the required dependencies using pip:

```bash
pip install transformers torch rich
```

## Usage

Run the tool using the following command:

```bash
python local_llm_launcher.py --model <model_name> --device <cpu|gpu> --config <path_to_config.json>
```

### Arguments

- `--model`: Name of the model to load (e.g., `gpt-j`, `llama-13b`).
- `--device`: Device to run the model on (`cpu` or `gpu`). Defaults to `cpu`.
- `--config`: Path to the configuration JSON file.

## Example

```bash
python local_llm_launcher.py --model gpt-j --device gpu --config config.json
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_local_llm_launcher.py
```

## License

MIT License
