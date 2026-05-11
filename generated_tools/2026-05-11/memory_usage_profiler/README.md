# Memory Usage Profiler

## Description
Memory Usage Profiler is a Python library designed to help developers profile memory consumption patterns of generative AI models during inference. By tracking memory usage over time and for specific model calls, this tool enables developers to identify potential memory bottlenecks, optimize infrastructure, and understand resource requirements for deploying their models.

## Features
- Profiles real-time memory usage during function execution.
- Generates detailed memory usage reports over time.
- Creates a time-series graph of memory usage trends.

## Installation
To install the required dependencies, run:
```bash
pip install psutil==5.9.5 matplotlib==3.8.0
```

## Usage
### Example
```python
from memory_usage_profiler import profile_memory

@profile_memory
def generate_text(model, input_text):
    # Simulate model inference
    result = model.generate(input_text)
    return result

# Example function usage
def example_function():
    data = []
    for i in range(1000000):
        data.append(i)
    return sum(data)

profiled_example = profile_memory(example_function)
profiled_example()
```

### CLI Usage
To run the example function with memory profiling:
```bash
python memory_usage_profiler.py --example
```

This will print memory usage over time to the console and generate a PNG graph of memory usage trends.

## Testing
To run the tests, install `pytest` and execute:
```bash
pytest test_memory_usage_profiler.py
```

## License
This project is licensed under the MIT License.