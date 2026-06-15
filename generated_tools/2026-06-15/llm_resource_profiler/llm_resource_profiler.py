import argparse
import time
import psutil
import matplotlib.pyplot as plt
from transformers import pipeline

def profile_resources(model_path, device, duration):
    """
    Profiles resource usage during model inference.

    Args:
        model_path (str): Path to the model.
        device (str): Device type ('cpu' or 'gpu').
        duration (int): Profiling duration in seconds.

    Returns:
        dict: Resource usage data.
    """
    resource_data = {
        "cpu_usage": [],
        "ram_usage": [],
        "vram_usage": []
    }

    # Load the model
    try:
        model = pipeline("text-generation", model=model_path, device=0 if device == "gpu" else -1)
    except Exception as e:
        raise ValueError(f"Failed to load model: {e}")

    # Start profiling
    start_time = time.time()
    while time.time() - start_time < duration:
        # Simulate inference
        try:
            model("Hello world")
        except Exception as e:
            raise RuntimeError(f"Inference failed: {e}")

        # Collect resource usage
        resource_data["cpu_usage"].append(psutil.cpu_percent(interval=0.1))
        resource_data["ram_usage"].append(psutil.virtual_memory().used / (1024 ** 2))
        if device == "gpu":
            try:
                import torch
                vram_usage = torch.cuda.memory_allocated() / (1024 ** 2)
                resource_data["vram_usage"].append(vram_usage)
            except ImportError:
                raise RuntimeError("PyTorch is required for GPU profiling.")

    return resource_data

def generate_report(resource_data, output_file):
    """
    Generates a resource usage report.

    Args:
        resource_data (dict): Resource usage data.
        output_file (str): Path to save the report.
    """
    plt.figure(figsize=(10, 6))

    plt.plot(resource_data["cpu_usage"], label="CPU Usage (%)")
    plt.plot(resource_data["ram_usage"], label="RAM Usage (MB)")
    if resource_data["vram_usage"]:
        plt.plot(resource_data["vram_usage"], label="VRAM Usage (MB)")

    plt.xlabel("Time (s)")
    plt.ylabel("Usage")
    plt.title("Resource Usage During Model Inference")
    plt.legend()
    plt.savefig(output_file)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Resource Profiler")
    parser.add_argument("--model", required=True, help="Path to the model file")
    parser.add_argument("--device", choices=["cpu", "gpu"], required=True, help="Device type")
    parser.add_argument("--duration", type=int, required=True, help="Profiling duration in seconds")
    parser.add_argument("--output", default="report.png", help="Output file for the report")

    args = parser.parse_args()

    try:
        data = profile_resources(args.model, args.device, args.duration)
        generate_report(data, args.output)
        print(f"Resource usage report saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")