# LLM Training Optimizer

## Description
The LLM Training Optimizer is a CLI tool designed to generate optimized training configurations for open-source large language models (LLMs). By leveraging hardware specifications and dataset size, this tool helps developers fine-tune models efficiently, maximizing hardware utilization and training performance.

## Features
- Autodetect hardware specifications (RAM and CPU cores).
- Generate YAML configuration files for training.
- Supports multiple open-source LLM frameworks.
- Suggests batch size, number of workers, and precision settings based on hardware.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python llm_training_optimizer.py --model gpt-j --dataset_size 10GB
```

### Example with Hardware File
```bash
python llm_training_optimizer.py --model llama --dataset_size 500MB --hardware_specs hardware.yaml
```

### Output
The tool generates a YAML configuration file (default: `config.yaml`) containing optimized training settings.

## Requirements
- Python 3.7+
- psutil==5.9.5
- PyYAML==6.0

## License
MIT License