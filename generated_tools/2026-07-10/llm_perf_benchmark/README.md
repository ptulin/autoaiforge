# LLM Performance Benchmark

## Description
`LLM Performance Benchmark` is a command-line tool designed to benchmark the inference performance of locally hosted large language models (LLMs). It provides detailed metrics such as latency and throughput, helping AI developers optimize their model configurations and identify hardware bottlenecks. The tool also supports generating visual charts for performance analysis.

## Features
- Benchmark LLM inference on CPU and GPU hardware.
- Configurable batch sizes and input lengths to simulate real workloads.
- Outputs average latency, throughput, and detailed latency metrics.
- Optionally generates visual charts for latency analysis.

## Installation

```bash
pip install torch==2.0.1 numpy==1.24.3 matplotlib==3.7.1
```

## Usage

### Command-line Arguments
- `--model_path`: Path to the model file (required).
- `--hardware`: Hardware type (`cpu` or `cuda`, required).
- `--batch_size`: Batch size for inference (required).
- `--input_length`: Input length for inference (required).
- `--plot`: Path to save the latency plot (optional).

### Example

```bash
python llm_perf_benchmark.py --model_path model.pt --hardware cuda --batch_size 16 --input_length 128 --plot latency_plot.png
```

## Output
- **Console Output**: Displays average latency and throughput.
- **Optional Plot**: Saves a latency chart to the specified file.

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_perf_benchmark.py
```