# Kernel Fusion Profiler

## Overview
The Kernel Fusion Profiler is a Python tool designed to profile LLM inference workloads and identify potential kernel fusion opportunities on GPUs. By analyzing kernel execution timelines, developers can optimize memory-bound or compute-bound operations by fusing consecutive kernel launches.

## Features
- Profiles GPU kernel execution using PyTorch's profiler.
- Analyzes profiling data to suggest kernel fusion opportunities.
- Visualizes kernel execution times in a bar plot.

## Installation
Install the required dependencies using pip:

```bash
pip install torch pandas seaborn matplotlib
```

## Usage
Run the tool from the command line:

```bash
python kernel_fusion_profiler.py --script <path_to_python_script>
```

### Arguments
- `--script`: Path to the Python script to profile.

## Output
- A CSV-like table of profiling results printed to the console.
- Suggestions for kernel fusion opportunities.
- A bar plot saved as `profiling_results.png`.

## Testing
To run the tests, install `pytest` and run:

```bash
pytest test_kernel_fusion_profiler.py
```

## License
This project is licensed under the MIT License.