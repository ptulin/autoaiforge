# LLM Hardware Optimizer

## Description
LLM Hardware Optimizer is a CLI tool designed to analyze local hardware capabilities and generate an optimized configuration file for running large language models efficiently. It considers GPU/CPU specs, available memory, and other hardware details to recommend optimal batch sizes, precision modes (FP16/FP32), and parallelism settings.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd llm_hardware_optimizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the desired output file format:

```bash
python llm_hardware_optimizer.py --output config.yaml
```

Supported output formats:
- YAML (`.yaml` or `.yml`)
- JSON (`.json`)

## Features

- **Automatic Hardware Profiling**: Detects CPU, GPU, and memory specifications.
- **Optimized Configuration Generation**: Recommends batch sizes, precision modes, and parallelism settings based on hardware.
- **Multi-framework Support**: Configurations are suitable for frameworks like PyTorch and TensorFlow.

## Example Output

```yaml
batch_size: 32
precision: FP16
parallelism: none
```

## Testing

Run tests using `pytest`:

```bash
pytest test_llm_hardware_optimizer.py
```

## License

MIT License
