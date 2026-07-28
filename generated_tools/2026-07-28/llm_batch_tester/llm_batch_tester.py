import argparse
import time
import numpy as np
import torch
import matplotlib.pyplot as plt

def load_model(model_path):
    """Load a PyTorch model from the specified path."""
    try:
        model = torch.load(model_path)
        model.eval()
        return model
    except Exception as e:
        raise ValueError(f"Failed to load model: {e}")

def benchmark_model(model, batch_size, input_shape, device):
    """Benchmark the model with a given batch size and input shape."""
    inputs = torch.randn(batch_size, *input_shape).to(device)
    model.to(device)

    # Warm-up
    for _ in range(5):
        _ = model(inputs)

    # Measure latency
    start_time = time.time()
    with torch.no_grad():
        _ = model(inputs)
    latency = time.time() - start_time

    throughput = batch_size / latency
    return latency, throughput

def run_benchmark(model_path, min_batch, max_batch, input_shape, device):
    """Run the benchmark for a range of batch sizes."""
    model = load_model(model_path)
    results = []

    for batch_size in range(min_batch, max_batch + 1):
        try:
            latency, throughput = benchmark_model(model, batch_size, input_shape, device)
            results.append((batch_size, latency, throughput))
        except Exception as e:
            print(f"Error benchmarking batch size {batch_size}: {e}")

    return results

def plot_results(results, output_file):
    """Plot the results and save to a file."""
    batch_sizes, latencies, throughputs = zip(*results)

    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Batch Size')
    ax1.set_ylabel('Latency (s)', color='tab:red')
    ax1.plot(batch_sizes, latencies, color='tab:red', label='Latency')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Throughput (samples/s)', color='tab:blue')
    ax2.plot(batch_sizes, throughputs, color='tab:blue', label='Throughput')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    fig.tight_layout()
    plt.title('Batch Size vs Latency and Throughput')
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='LLM Batch Inference Tester')
    parser.add_argument('--model', required=True, help='Path to the model file')
    parser.add_argument('--min_batch', type=int, required=True, help='Minimum batch size')
    parser.add_argument('--max_batch', type=int, required=True, help='Maximum batch size')
    parser.add_argument('--input_shape', type=int, nargs='+', required=True, help='Input shape for the model (excluding batch size)')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Device to run the benchmark on')
    parser.add_argument('--output', default='benchmark_results.png', help='Output file for the plot')

    args = parser.parse_args()

    results = run_benchmark(args.model, args.min_batch, args.max_batch, tuple(args.input_shape), args.device)

    if results:
        for batch_size, latency, throughput in results:
            print(f"Batch Size: {batch_size}, Latency: {latency:.4f}s, Throughput: {throughput:.2f} samples/s")

        plot_results(results, args.output)
        print(f"Results plotted and saved to {args.output}")
    else:
        print("No results to display.")

if __name__ == '__main__':
    main()