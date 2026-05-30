# LLM Inference Profiler

## Overview
The LLM Inference Profiler is a Python tool designed to benchmark and profile large language model (LLM) inference. It provides detailed performance statistics such as latency, throughput, and GPU utilization, helping developers identify bottlenecks and optimize model execution.

## Features
- Supports different batch sizes and input lengths.
- Provides average latency, throughput, and GPU memory usage statistics.
- Outputs results to the console or an optional JSON file.

## Installation
Install the required dependencies:

```bash
pip install torch transformers
```

## Usage
Run the profiler using the command line:

```bash
python llm_inference_profiler.py --model <model_name> --batch_size <batch_size> --input_length <input_length> --iterations <iterations> [--output_file <output_file>]
```

### Arguments
- `--model`: Name of the model to benchmark (e.g., `gpt-2`).
- `--batch_size`: Batch size for inference.
- `--input_length`: Input length for each sequence.
- `--iterations`: Number of iterations to run.
- `--output_file`: Optional JSON file to save the report.

## Testing
Run the tests using `pytest`:

```bash
pytest test_llm_inference_profiler.py
```

The tests mock external dependencies to ensure they pass without network access.

## License
MIT License