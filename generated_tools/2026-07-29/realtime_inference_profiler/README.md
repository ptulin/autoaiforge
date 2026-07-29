# Real-Time Inference Profiler

## Overview

The Real-Time Inference Profiler is a Python tool designed to simulate and profile AI models under real-time conditions. It generates load scenarios (e.g., steady or bursty request rates) and measures performance metrics such as latency and throughput. This tool provides insights into how models behave under different scalability conditions.

## Features

- Simulate steady and bursty workloads.
- Measure performance metrics like latency and throughput.
- Supports multiple concurrent workers.
- Outputs results in JSON or CSV format.

## Installation

Install the required dependencies:

```bash
pip install numpy pandas pytest
```

## Usage

### Command-Line Interface

Run the profiler from the command line:

```bash
python realtime_inference_profiler.py --workload steady --rate 10 --duration 10 --workers 2 --output-format json
```

### Programmatic Usage

You can also use the profiler programmatically:

```python
from realtime_inference_profiler import profile

def my_model():
    # Simulate model inference
    time.sleep(0.01)

metrics = profile(my_model, workload='steady', rate=10, duration=10, workers=2, output_format='json')
print(metrics)
```

## Testing

Run the tests using pytest:

```bash
pytest test_realtime_inference_profiler.py
```

## License

This project is licensed under the MIT License.