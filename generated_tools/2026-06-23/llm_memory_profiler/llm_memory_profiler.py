import argparse
import tracemalloc
import psutil
import os
import sys
from typing import Any, Dict

def profile_memory(script_path: str) -> Dict[str, Any]:
    """
    Profiles the memory usage of a Python script that uses a large language model.

    Args:
        script_path (str): Path to the Python script to profile.

    Returns:
        dict: A dictionary containing memory usage breakdown and optimization tips.
    """
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"The script file '{script_path}' does not exist.")

    tracemalloc.start()

    # Capture initial memory usage
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / (1024 ** 2)  # in MB

    # Execute the script in a controlled environment
    try:
        exec_globals = {}
        with open(script_path, "r", encoding="utf-8") as script_file:
            script_code = script_file.read()
        exec(script_code, exec_globals)
    except Exception as e:
        tracemalloc.stop()
        raise RuntimeError(f"Error executing the script: {e}")

    # Capture memory usage after execution
    current_memory = process.memory_info().rss / (1024 ** 2)  # in MB
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()

    # Analyze memory usage
    top_stats = snapshot.statistics("lineno")
    memory_breakdown = [
        {
            "file": stat.traceback[0].filename,
            "line": stat.traceback[0].lineno,
            "size_kb": stat.size / 1024
        }
        for stat in top_stats[:10]
    ]

    # Generate optimization tips
    optimization_tips = []
    if current_memory - initial_memory > 1000:  # Arbitrary threshold for high memory usage
        optimization_tips.append("Consider using smaller batch sizes or model quantization.")
    if any(stat.size > 10 * 1024 * 1024 for stat in top_stats):  # Large allocations
        optimization_tips.append("Investigate large memory allocations for potential optimizations.")

    return {
        "initial_memory_mb": initial_memory,
        "peak_memory_mb": current_memory,
        "memory_breakdown": memory_breakdown,
        "optimization_tips": optimization_tips
    }

def main():
    parser = argparse.ArgumentParser(
        description="LLM Memory Profiler: Profile memory usage of large language models during inference."
    )
    parser.add_argument(
        "--script",
        required=True,
        help="Path to the Python script using the large language model."
    )
    args = parser.parse_args()

    try:
        result = profile_memory(args.script)
        print("Memory Profiling Report:")
        print(f"Initial Memory Usage: {result['initial_memory_mb']:.2f} MB")
        print(f"Peak Memory Usage: {result['peak_memory_mb']:.2f} MB")
        print("Memory Breakdown:")
        for entry in result['memory_breakdown']:
            print(f"  File: {entry['file']}, Line: {entry['line']}, Size: {entry['size_kb']:.2f} KB")
        if result['optimization_tips']:
            print("Optimization Tips:")
            for tip in result['optimization_tips']:
                print(f"  - {tip}")
        else:
            print("No optimization tips available. Memory usage is within acceptable limits.")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
