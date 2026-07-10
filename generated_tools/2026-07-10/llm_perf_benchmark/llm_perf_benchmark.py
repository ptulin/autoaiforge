import argparse
import time
import torch
import numpy as np
import matplotlib.pyplot as plt

def benchmark_model(model_path, hardware, batch_size, input_length):
    try:
        # Load the model
        device = torch.device(hardware)
        model = torch.jit.load(model_path, map_location=device)
        model.eval()

        # Generate dummy input
        input_tensor = torch.randint(0, 10000, (batch_size, input_length), dtype=torch.long, device=device)

        # Benchmarking
        latencies = []
        num_iterations = 10
        with torch.no_grad():
            for _ in range(num_iterations):
                start_time = time.time()
                model(input_tensor)
                end_time = time.time()
                latencies.append(end_time - start_time)

        # Metrics
        avg_latency = np.mean(latencies)
        throughput = batch_size / avg_latency

        return {
            "average_latency": avg_latency,
            "throughput": throughput,
            "latencies": latencies
        }

    except Exception as e:
        raise RuntimeError(f"Error during benchmarking: {e}")

def plot_metrics(latencies, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(latencies, marker='o', label='Latency per iteration')
    plt.xlabel('Iteration')
    plt.ylabel('Latency (seconds)')
    plt.title('Model Latency Over Iterations')
    plt.legend()
    plt.grid()
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="LLM Performance Benchmark Tool")
    parser.add_argument('--model_path', type=str, required=True, help="Path to the model file")
    parser.add_argument('--hardware', type=str, choices=['cpu', 'cuda'], required=True, help="Hardware type (cpu or cuda)")
    parser.add_argument('--batch_size', type=int, required=True, help="Batch size for inference")
    parser.add_argument('--input_length', type=int, required=True, help="Input length for inference")
    parser.add_argument('--plot', type=str, help="Path to save the latency plot (optional)")

    args = parser.parse_args()

    try:
        metrics = benchmark_model(args.model_path, args.hardware, args.batch_size, args.input_length)
        print(f"Average Latency: {metrics['average_latency']:.6f} seconds")
        print(f"Throughput: {metrics['throughput']:.2f} samples/second")

        if args.plot:
            plot_metrics(metrics['latencies'], args.plot)
            print(f"Latency plot saved to {args.plot}")

    except RuntimeError as e:
        print(str(e))

if __name__ == "__main__":
    main()