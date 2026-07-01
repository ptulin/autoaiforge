import argparse
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from torch.profiler import profile, record_function, ProfilerActivity
import torch

def profile_script(script_path):
    """Profiles the given Python script for GPU kernel execution."""
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"The script {script_path} does not exist.")

    # Dictionary to store profiling results
    profiling_results = []

    # Use PyTorch profiler to capture GPU kernel execution
    with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
                 on_trace_ready=lambda trace: trace.export_chrome_trace("trace.json")) as prof:
        with record_function("model_inference"):
            with open(script_path, "r") as script_file:
                script_code = script_file.read()
                exec(script_code, {"__name__": "__main__"})

    # Parse the profiling results
    for evt in prof.key_averages():
        profiling_results.append({
            "name": evt.key,
            "cpu_time": evt.cpu_time_total,
            "cuda_time": evt.cuda_time_total,
            "occurrences": evt.count
        })

    return pd.DataFrame(profiling_results)

def analyze_fusion_opportunities(profiling_data):
    """Analyzes the profiling data to identify kernel fusion opportunities."""
    # Identify consecutive kernels with high memory or compute overhead
    profiling_data = profiling_data.sort_values(by="cuda_time", ascending=False)
    suggestions = []

    for idx, row in profiling_data.iterrows():
        if row['occurrences'] > 1 and row['cuda_time'] > 1000:  # Arbitrary thresholds
            suggestions.append(f"Consider fusing kernel '{row['name']}' with similar operations.")

    return suggestions

def visualize_profiling_data(profiling_data):
    """Generates a visualization of the profiling data."""
    plt.figure(figsize=(10, 6))
    sns.barplot(x="cuda_time", y="name", data=profiling_data)
    plt.xlabel("CUDA Time (us)")
    plt.ylabel("Kernel Name")
    plt.title("GPU Kernel Execution Times")
    plt.tight_layout()
    plt.savefig("profiling_results.png")
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Kernel Fusion Profiler: Optimize GPU kernel execution.")
    parser.add_argument("--script", type=str, required=True, help="Path to the Python script to profile.")
    args = parser.parse_args()

    try:
        profiling_data = profile_script(args.script)
        suggestions = analyze_fusion_opportunities(profiling_data)

        print("\nProfiling Results:\n")
        print(profiling_data)

        print("\nFusion Suggestions:\n")
        for suggestion in suggestions:
            print(f"- {suggestion}")

        visualize_profiling_data(profiling_data)
        print("\nVisualization saved as 'profiling_results.png'.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()