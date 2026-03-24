import argparse
import json
import time
import psutil
import matplotlib.pyplot as plt
from openai import ChatCompletion

def profile_power_usage(models, prompts):
    """
    Profiles power consumption during GPT model inference.

    Args:
        models (list): List of GPT models to profile.
        prompts (list): List of prompts to send to the models.

    Returns:
        dict: Summary of power usage and CPU/GPU utilization.
    """
    results = {}

    for model in models:
        print(f"Profiling model: {model}")
        cpu_usage = []
        gpu_usage = []
        power_usage = []

        for prompt in prompts:
            print(f"Sending prompt to {model}: {prompt[:30]}...")
            start_time = time.time()

            # Simulate API call to OpenAI (mocked in tests)
            try:
                response = ChatCompletion.create(model=model, messages=[{"role": "user", "content": prompt}])
            except Exception as e:
                print(f"Error during API call: {e}")
                continue

            elapsed_time = time.time() - start_time

            # Monitor system resource usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            gpu_percent = 0  # Placeholder for GPU usage (requires additional libraries for actual GPU monitoring)
            power = psutil.sensors_battery().percent if psutil.sensors_battery() else 0

            cpu_usage.append(cpu_percent)
            gpu_usage.append(gpu_percent)
            power_usage.append(power)

            print(f"Response time: {elapsed_time:.2f}s, CPU: {cpu_percent}%, GPU: {gpu_percent}%, Power: {power}%")

        results[model] = {
            "cpu_usage": cpu_usage,
            "gpu_usage": gpu_usage,
            "power_usage": power_usage,
        }

    return results

def plot_results(results):
    """
    Generates and saves power usage graphs.

    Args:
        results (dict): Profiling results.
    """
    for model, data in results.items():
        plt.figure(figsize=(10, 6))
        plt.plot(data["cpu_usage"], label="CPU Usage (%)")
        plt.plot(data["gpu_usage"], label="GPU Usage (%)")
        plt.plot(data["power_usage"], label="Power Usage (%)")
        plt.title(f"Power Usage Profile for {model}")
        plt.xlabel("Prompt Index")
        plt.ylabel("Usage (%)")
        plt.legend()
        plt.grid()
        plt.savefig(f"{model}_power_usage.png")
        plt.close()

def main():
    parser = argparse.ArgumentParser(description="GPT Power Profiler")
    parser.add_argument("--models", type=str, required=True, help="Comma-separated list of GPT models to profile (e.g., gpt-4,gpt-5)")
    parser.add_argument("--prompts", type=str, required=True, help="Path to JSON file containing prompts")

    args = parser.parse_args()

    # Parse models
    models = args.models.split(",")

    # Load prompts from JSON file
    try:
        with open(args.prompts, "r") as f:
            prompts = json.load(f)
        if not isinstance(prompts, list):
            raise ValueError("Prompts file must contain a JSON array of strings.")
    except Exception as e:
        print(f"Error loading prompts: {e}")
        return

    # Profile power usage
    results = profile_power_usage(models, prompts)

    # Display summary
    for model, data in results.items():
        print(f"\nSummary for {model}:")
        print(f"Average CPU Usage: {sum(data['cpu_usage']) / len(data['cpu_usage']):.2f}%")
        print(f"Average GPU Usage: {sum(data['gpu_usage']) / len(data['gpu_usage']):.2f}%")
        print(f"Average Power Usage: {sum(data['power_usage']) / len(data['power_usage']):.2f}%")

    # Generate graphs
    plot_results(results)

if __name__ == "__main__":
    main()
