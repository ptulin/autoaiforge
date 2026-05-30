# LLM Runtime Monitor

## Description
LLM Runtime Monitor is a Python library designed to help developers monitor resource utilization (CPU, memory) and performance metrics while running open-source Large Language Models (LLMs). This tool provides insights into resource usage and helps optimize runtime environments and debug issues during model execution.

## Features
- Track CPU and memory usage in real-time
- Log model-specific performance metrics like inference latency
- Visualize resource utilization with simple charts

## Installation
```bash
pip install psutil==5.9.5 matplotlib==3.7.2
```

## Usage
```python
from llm_runtime_monitor import monitor

def my_model():
    # Simulate some workload
    for _ in range(10000000):
        pass

# Monitor the model execution
monitor(my_model)
```

## Example
```python
from llm_runtime_monitor import monitor

def dummy_model(duration):
    """A dummy model function to simulate workload."""
    import time
    start = time.time()
    while time.time() - start < duration:
        sum(i * i for i in range(10000))

print("Starting LLM Runtime Monitor with a dummy model...")
monitor(dummy_model, 5)
```

## License
MIT License
