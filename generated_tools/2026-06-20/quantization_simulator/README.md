# Quantization Simulator

## Overview
Quantization Simulator is a Python library designed to simulate the effects of various quantization techniques on large language models before applying them. This tool allows developers to experiment with different precision levels (e.g., 16-bit, 8-bit, 4-bit) and observe their impact on memory usage, inference speed, and accuracy degradation.

## Features
- Simulate quantization at 16-bit, 8-bit, and 4-bit precision levels.
- Measure memory usage of the quantized model.
- Evaluate inference speed (with CUDA support).
- Assess accuracy degradation using evaluation data.

## Requirements
- Python 3.7+
- PyTorch
- pytest (for testing)

## Installation
Install the required dependencies using pip:

```bash
pip install torch pytest
```

## Usage
### CLI
Run the quantization simulator using the command line:

```bash
python quantization_simulator.py <model_path> --quantization_levels 16 8 4
```

- `<model_path>`: Path to the PyTorch model file.
- `--quantization_levels`: List of quantization levels to simulate (default: `[16, 8, 4]`).

### Example
```bash
python quantization_simulator.py my_model.pth --quantization_levels 16 8
```

### Programmatic Usage
You can also use the `simulate_quantization` function directly in your Python code:

```python
import torch
from quantization_simulator import simulate_quantization

model = torch.nn.Linear(10, 2)
results = simulate_quantization(model, quantization_levels=[16, 8])
print(results)
```

## Testing
Run the tests using pytest:

```bash
pytest test_quantization_simulator.py
```

## License
This project is licensed under the MIT License.