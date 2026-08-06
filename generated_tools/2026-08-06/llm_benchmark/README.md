# LLM Benchmark
This tool provides a comprehensive benchmarking suite for Large Language Models (LLMs) to evaluate their performance and efficiency.

## Installation
To install the required packages, run the following command:
```bash
pip install transformers torch psutil
```

## Usage
To use the benchmarking tool, run the following command:
```bash
python llm_benchmark.py --model_path <model_path> --metric <metric>
```
Replace `<model_path>` with the path to the model you want to benchmark, and `<metric>` with the metric you want to measure (inference_time, memory_usage, or energy_consumption).

## Metrics
The tool supports the following metrics:
* inference_time: measures the time it takes for the model to make a prediction
* memory_usage: measures the amount of memory used by the model
* energy_consumption: measures the energy consumed by the model (currently a placeholder function)