import os
import time
import json
import psutil
import pandas as pd
import argparse
from typing import List, Dict

def adaptive_memory_optimizer(agent: str, strategy: str, output: str, interval: int):
    """
    Adaptive Memory Optimizer: Benchmarks memory usage of an AI agent and applies optimizations.
    """
    try:
        if not os.path.exists(agent):
            raise FileNotFoundError(f"Agent script '{agent}' does not exist.")

        # Start monitoring memory usage
        memory_usage = []
        process = psutil.Popen(["python", agent], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))

        print(f"Monitoring memory usage of agent: {agent}")
        while process.is_running():
            try:
                mem_info = process.memory_info()
                memory_usage.append({
                    'timestamp': time.time(),
                    'rss': mem_info.rss,  # Resident Set Size
                    'vms': mem_info.vms   # Virtual Memory Size
                })
                time.sleep(interval)
            except psutil.NoSuchProcess:
                break

        # Apply optimization strategy
        optimized_memory_usage = apply_optimization(memory_usage, strategy)

        # Generate report
        if output:
            generate_report(optimized_memory_usage, output)

        print("Memory optimization completed successfully.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def apply_optimization(memory_data: List[Dict], strategy: str) -> List[Dict]:
    """
    Applies the selected optimization strategy to the memory data.
    """
    if strategy == 'pruning':
        return memory_data[::2]  # Example: Keep every other sample
    elif strategy == 'compression':
        return compress_memory_data(memory_data)
    elif strategy == 'partitioning':
        return partition_memory_data(memory_data)
    else:
        raise ValueError("Unknown strategy")


def compress_memory_data(memory_data: List[Dict]) -> List[Dict]:
    """
    Example compression: Average memory usage over intervals.
    """
    if not memory_data:
        return []

    df = pd.DataFrame(memory_data)
    compressed = df.groupby(df.index // 2).mean().to_dict('records')
    return compressed


def partition_memory_data(memory_data: List[Dict]) -> List[List[Dict]]:
    """
    Example partitioning: Split memory data into chunks.
    """
    if not memory_data:
        return []

    chunk_size = max(1, len(memory_data) // 2)  # Adjusted to split into 2 chunks
    return [memory_data[i:i + chunk_size] for i in range(0, len(memory_data), chunk_size)]


def generate_report(memory_data: List[Dict], output_format: str):
    """
    Generates a report in the specified format.
    """
    if output_format == 'csv':
        df = pd.DataFrame(memory_data)
        df.to_csv('memory_report.csv', index=False)
        print("Report saved as memory_report.csv")
    elif output_format == 'json':
        with open('memory_report.json', 'w') as f:
            json.dump(memory_data, f, indent=4)
        print("Report saved as memory_report.json")


def main():
    parser = argparse.ArgumentParser(description="Adaptive Memory Optimizer")
    parser.add_argument('--agent', required=True, type=str, help='Path to the agent script to monitor.')
    parser.add_argument('--strategy', required=True, choices=['pruning', 'compression', 'partitioning'], help='Optimization strategy to apply.')
    parser.add_argument('--output', choices=['csv', 'json'], default=None, help='Optional output format for the benchmarking report.')
    parser.add_argument('--interval', default=1, type=int, help='Interval in seconds for memory usage sampling.')

    args = parser.parse_args()

    adaptive_memory_optimizer(args.agent, args.strategy, args.output, args.interval)

if __name__ == '__main__':
    main()
