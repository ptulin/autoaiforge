# Edge Inference Profiler

## Overview

`edge_inference_profiler` is a Python CLI tool designed to profile inference times and memory usage of small AI models on different edge devices. It helps developers identify bottlenecks in the model and adjust optimizations to enhance edge performance.

## Features

- Measure inference latency (in milliseconds).
- Measure memory usage (in MB) for CUDA-enabled devices.
- Generate a performance graph for visualization.

## Installation

Install the required dependencies using pip:

```bash
pip install torch matplotlib pytest
```

## Usage

Run the tool from the command line:

```bash
python edge_inference_profiler.py --model <model_path> --input_shape <input_shape> --output_graph <output_graph>
```

### Arguments

- `--model`: Path to the PyTorch model file (e.g., `model.pth`).
- `--input_shape`: Input tensor shape as comma-separated values (e.g., `1,3,224,224`).
- `--output_graph`: Path to save the performance graph (e.g., `performance.png`).

### Example

```bash
python edge_inference_profiler.py --model model.pth --input_shape 1,3,224,224 --output_graph performance.png
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_edge_inference_profiler.py
```

## Notes

- Memory usage profiling is only available on CUDA-enabled devices. If CUDA is not available, memory usage will be reported as `0 MB`.
