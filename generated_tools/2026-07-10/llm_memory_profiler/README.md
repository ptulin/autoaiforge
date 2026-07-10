# LLM Memory Profiler

## Description
LLM Memory Profiler is a Python library designed to profile the memory usage of locally hosted large language models (LLMs) during inference tasks. It provides insights into peak memory usage, memory allocation per layer, and device-specific memory consumption, helping developers optimize memory-intensive workloads.

## Features
- Layer-wise breakdown of memory usage during inference
- Supports both PyTorch and TensorFlow models
- Detailed logging of memory allocation over time

## Installation

```bash
pip install torch==2.0.1 tensorflow==2.13.0 psutil==5.9.5
```

## Usage

### Example Usage

```python
from llm_memory_profiler import profile_memory
import torch

# Load your PyTorch model
model = torch.load("path_to_model.pth")
input_data = torch.randn(1, 3, 224, 224)

# Profile memory
metrics = profile_memory(model, input_data)
print(metrics)
```

### CLI Usage

```bash
python llm_memory_profiler.py --model_path path_to_model.pth --framework torch --log_file memory_log.txt
```

## Output
The tool logs memory usage metrics to the console or a specified log file. Metrics include:
- Initial memory usage
- Peak memory usage
- Inference time

## License
MIT License