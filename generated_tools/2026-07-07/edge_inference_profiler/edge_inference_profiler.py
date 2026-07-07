import argparse
import time
import torch
import numpy as np
import matplotlib.pyplot as plt
from torch import nn
from torch.utils.data import DataLoader

def profile_model(model_path, input_shape, output_graph):
    """
    Profiles the inference latency and memory usage of a PyTorch model.

    Args:
        model_path (str): Path to the PyTorch model file.
        input_shape (tuple): Shape of the input tensor.
        output_graph (str): Path to save the performance graph.

    Returns:
        dict: Profiling results containing latency and memory usage.
    """
    # Load the model
    try:
        model = torch.load(model_path)
        model.eval()
    except Exception as e:
        raise ValueError(f"Failed to load model: {e}")

    # Create a dummy input tensor
    try:
        input_tensor = torch.randn(input_shape)
    except Exception as e:
        raise ValueError(f"Invalid input shape: {e}")

    # Warm-up runs
    for _ in range(5):
        _ = model(input_tensor)

    # Measure inference latency
    start_time = time.time()
    with torch.no_grad():
        for _ in range(100):
            _ = model(input_tensor)
    end_time = time.time()

    latency = (end_time - start_time) / 100  # Average latency per inference

    # Measure memory usage (only if CUDA is available)
    memory_usage = 0
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        with torch.no_grad():
            _ = model(input_tensor)
        memory_usage = torch.cuda.max_memory_allocated() / (1024 ** 2)  # Convert to MB

    # Generate performance graph
    metrics = [latency * 1000, memory_usage]  # Latency in ms, memory in MB
    labels = ['Latency (ms)', 'Memory (MB)']

    plt.bar(labels, metrics, color=['blue', 'orange'])
    plt.title('Model Performance Metrics')
    plt.ylabel('Value')
    plt.savefig(output_graph)

    return {
        "latency_ms": latency * 1000,
        "memory_mb": memory_usage
    }

def main():
    parser = argparse.ArgumentParser(description="Edge Inference Profiler")
    parser.add_argument('--model', type=str, required=True, help="Path to the model file (e.g., model.pth)")
    parser.add_argument('--input_shape', type=str, required=True, help="Input tensor shape as comma-separated values (e.g., 1,3,224,224)")
    parser.add_argument('--output_graph', type=str, required=True, help="Path to save the performance graph (e.g., performance.png)")

    args = parser.parse_args()

    try:
        input_shape = tuple(map(int, args.input_shape.split(',')))
        results = profile_model(args.model, input_shape, args.output_graph)
        print("Profiling Results:")
        print(f"Latency: {results['latency_ms']:.2f} ms")
        print(f"Memory Usage: {results['memory_mb']:.2f} MB")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
