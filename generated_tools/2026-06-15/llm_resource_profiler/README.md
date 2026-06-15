# LLM Resource Profiler

## Description
LLM Resource Profiler is a Python module and CLI tool designed to profile resource usage (RAM, VRAM, CPU, etc.) during inference with locally deployed large language models (LLMs). It helps developers identify performance bottlenecks and optimize hardware usage.

## Features
- Tracks real-time resource consumption during model inference.
- Generates detailed performance reports with charts.
- Supports multiple hardware setups (CPU vs GPU).

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python llm_resource_profiler.py --model model.bin --device gpu --duration 60 --output report.png
```

### Arguments
- `--model`: Path to the model file.
- `--device`: Device type (`cpu` or `gpu`).
- `--duration`: Profiling duration in seconds.
- `--output`: Path to save the resource usage report (default: `report.png`).

## Example
```bash
python llm_resource_profiler.py --model model.bin --device cpu --duration 30 --output cpu_report.png
```

## License
MIT License