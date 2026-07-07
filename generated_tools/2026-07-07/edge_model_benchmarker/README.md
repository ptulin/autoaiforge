# Edge Model Benchmarker

## Description
The Edge Model Benchmarker is a CLI tool designed to evaluate the performance of small AI models on edge devices under constrained resources. It enables developers to simulate real-world edge scenarios, such as limited CPU cores, memory constraints, and unreliable network conditions, and generates detailed performance reports for analysis.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/edge_model_benchmarker.git
    cd edge_model_benchmarker
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool using the following command:

```bash
python edge_model_benchmarker.py --model model.pth --dataset test_data.csv --cpu_cores 2 --simulate_latency 100 --output results.json
```

### Arguments:
- `--model`: Path to the PyTorch model file.
- `--dataset`: Path to the test dataset (CSV format).
- `--cpu_cores`: Number of CPU cores to use for benchmarking.
- `--memory_limit`: Limit on memory usage (number of samples).
- `--simulate_latency`: Simulated network latency in milliseconds.
- `--output`: Path to save the benchmark results (JSON format).

## Features
- Benchmark AI model performance under constrained resources.
- Simulate network latency for edge environments.
- Generate detailed performance reports including latency and throughput.

## Example

```bash
python edge_model_benchmarker.py --model model.pth --dataset test_data.csv --cpu_cores 4 --simulate_latency 200 --output benchmark_results.json
```

## License
MIT License
