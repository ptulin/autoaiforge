# LLM Batch Inference Tester

## Description

`LLM Batch Inference Tester` is a Python library and CLI tool designed to benchmark the inference speeds of large language models (LLMs) across different batch sizes and hardware configurations. This tool helps AI developers evaluate the trade-offs between throughput and latency when running models locally.

## Features

- Customizable benchmarking for batch sizes
- Supports multiple LLM frameworks (via PyTorch)
- Generates detailed performance metrics
- Produces visual graphs for batch size vs latency/throughput

## Installation

Install the required dependencies:

```bash
pip install torch==2.0.1 numpy==1.24.4 matplotlib==3.7.2
```

## Usage

### CLI Example

```bash
python llm_batch_tester.py --model path/to/model --min_batch 1 --max_batch 16 --input_shape 3 224 224 --device cpu
```

### Parameters

- `--model`: Path to the PyTorch model file.
- `--min_batch`: Minimum batch size for benchmarking.
- `--max_batch`: Maximum batch size for benchmarking.
- `--input_shape`: Input shape for the model (excluding batch size).
- `--device`: Device to run the benchmark on (`cpu` or `cuda`).
- `--output`: Output file for the plot (default: `benchmark_results.png`).

## Example Output

```plaintext
Batch Size: 1, Latency: 0.0050s, Throughput: 200.00 samples/s
Batch Size: 2, Latency: 0.0070s, Throughput: 285.71 samples/s
...
Results plotted and saved to benchmark_results.png
```

## Development

### Running Tests

Install `pytest` and run the tests:

```bash
pip install pytest
pytest test_llm_batch_tester.py
```

## License

MIT License