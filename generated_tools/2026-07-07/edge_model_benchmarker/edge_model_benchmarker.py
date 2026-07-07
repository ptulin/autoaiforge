import argparse
import json
import time
import numpy as np
import psutil
import torch
from torch.utils.data import DataLoader, TensorDataset

def simulate_network_latency(latency_ms):
    """Simulates network latency by sleeping for the specified duration."""
    time.sleep(latency_ms / 1000.0)

def benchmark_model(model_path, dataset_path, cpu_cores=None, memory_limit=None, simulate_latency=None):
    """Benchmark the performance of a PyTorch model under constrained resources."""
    # Load the model
    try:
        model = torch.load(model_path)
        model.eval()
    except Exception as e:
        return {"error": f"Failed to load model: {e}"}

    # Load the dataset
    try:
        data = np.loadtxt(dataset_path, delimiter=',')
        inputs = torch.tensor(data[:, :-1], dtype=torch.float32)
        targets = torch.tensor(data[:, -1], dtype=torch.float32)
        dataset = TensorDataset(inputs, targets)
        dataloader = DataLoader(dataset, batch_size=32)
    except Exception as e:
        return {"error": f"Failed to load dataset: {e}"}

    # Apply resource constraints
    if cpu_cores:
        psutil.Process().cpu_affinity(list(range(cpu_cores)))

    if memory_limit:
        # Simulating memory constraint by limiting data loading size
        inputs = inputs[:memory_limit]
        targets = targets[:memory_limit]

    # Benchmarking
    results = []
    total_latency = 0
    total_throughput = 0

    for batch in dataloader:
        inputs, targets = batch

        if simulate_latency:
            simulate_network_latency(simulate_latency)

        start_time = time.time()
        with torch.no_grad():
            outputs = model(inputs)
        end_time = time.time()

        latency = end_time - start_time
        throughput = len(inputs) / latency

        results.append({"latency": latency, "throughput": throughput})
        total_latency += latency
        total_throughput += throughput

    avg_latency = total_latency / len(results)
    avg_throughput = total_throughput / len(results)

    return {
        "average_latency": avg_latency,
        "average_throughput": avg_throughput,
        "results": results
    }

def main():
    parser = argparse.ArgumentParser(description="Edge Model Benchmarker")
    parser.add_argument('--model', required=True, help="Path to the model file")
    parser.add_argument('--dataset', required=True, help="Path to the test dataset")
    parser.add_argument('--cpu_cores', type=int, help="Number of CPU cores to use")
    parser.add_argument('--memory_limit', type=int, help="Limit on memory usage (number of samples)")
    parser.add_argument('--simulate_latency', type=int, help="Simulated network latency in milliseconds")
    parser.add_argument('--output', required=True, help="Path to save the benchmark results (JSON format)")

    args = parser.parse_args()

    results = benchmark_model(
        model_path=args.model,
        dataset_path=args.dataset,
        cpu_cores=args.cpu_cores,
        memory_limit=args.memory_limit,
        simulate_latency=args.simulate_latency
    )

    with open(args.output, 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()