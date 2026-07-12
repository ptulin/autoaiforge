# Distributed Metric Collector

## Overview
The Distributed Metric Collector is a Python library designed to collect and visualize training metrics (e.g., CPU usage, memory usage, custom metrics) across distributed nodes during large-scale AI model training. This helps developers identify bottlenecks and optimize performance.

## Features
- Collect metrics such as CPU usage and memory usage from distributed nodes.
- Support for custom metric hooks.
- Visualization of collected metrics.

## Installation
Install the required dependencies:

```bash
pip install psutil matplotlib
```

## Usage

### Command Line Interface
Run the tool from the command line:

```bash
python distributed_metric_collector.py --nodes node1 node2 --save metrics
```

- `--nodes`: List of node IPs to collect metrics from.
- `--save`: Optional path to save the visualization as images.

### Programmatic Usage

```python
from distributed_metric_collector import Collector

# Define custom metric hook
def custom_hook():
    return {"custom_metric": 99.0}

collector = Collector(nodes=["node1", "node2"], metric_hooks=[custom_hook])
collector.start()

try:
    print("Collecting metrics...")
    time.sleep(10)  # Collect metrics for 10 seconds
finally:
    collector.stop()
    collector.visualize(save_path="metrics")
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_distributed_metric_collector.py
```

## License
MIT License
