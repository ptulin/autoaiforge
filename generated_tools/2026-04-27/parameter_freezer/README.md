# Parameter Freezer

## Overview

`parameter_freezer` is a Python tool designed to selectively freeze specific layers or modules of a pre-trained language model during fine-tuning. This helps reduce computational costs and avoid overfitting while focusing on training specific parts of the model.

## Installation

Install the required dependencies:

```bash
pip install torch transformers pyyaml
```

## Usage

### Command Line Interface

```bash
python parameter_freezer.py --model <model_checkpoint> --config <config_file> [--output <output_path>]
```

- `--model`: Path or name of the pre-trained model checkpoint.
- `--config`: Path to the YAML configuration file specifying layers to freeze.
- `--output`: (Optional) Path to save the modified model.

### Example YAML Configuration

```yaml
freeze_layers:
  - layer1
  - layer2
```

### Example

```bash
python parameter_freezer.py --model bert-base-uncased --config freeze_config.yaml --output frozen_model
```

## Testing

Run tests using `pytest`:

```bash
pytest test_parameter_freezer.py
```

## License

MIT License
