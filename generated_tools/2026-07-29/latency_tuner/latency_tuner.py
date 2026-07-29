import argparse
import time
import numpy as np

class LatencyTuner:
    def __init__(self, script, stages):
        self.script = script
        self.stages = stages
        self.script_globals = {}

    def benchmark_stage(self, stage_name, func, *args, **kwargs):
        """Benchmark a specific stage by measuring its execution time."""
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        return end_time - start_time

    def run_benchmark(self):
        """Run the benchmark on the specified stages."""
        latencies = {}
        for stage in self.stages:
            if stage not in self.script_globals:
                raise ValueError(f"Stage '{stage}' is not defined in the script.")
            func = self.script_globals[stage]
            latencies[stage] = self.benchmark_stage(stage, func)
        return latencies

    def suggest_optimizations(self, latencies):
        """Provide suggestions for optimization based on latency results."""
        suggestions = []
        for stage, latency in latencies.items():
            if latency > 1.0:  # Arbitrary threshold for optimization
                suggestions.append(f"Consider optimizing the '{stage}' stage. It took {latency:.2f}s.")
        return suggestions

def main():
    parser = argparse.ArgumentParser(description="Latency Tuner for AI Inference")
    parser.add_argument("--script", required=True, help="Path to the inference script")
    parser.add_argument("--stages", required=True, help="Comma-separated list of pipeline stages")
    args = parser.parse_args()

    # Load the script dynamically
    script_globals = {}
    try:
        with open(args.script, "r") as f:
            exec(f.read(), script_globals)
    except FileNotFoundError:
        print(f"Error: Script '{args.script}' not found.")
        return
    except Exception as e:
        print(f"Error loading script: {e}")
        return

    # Extract the stages
    stages = args.stages.split(",")

    # Initialize and run the latency tuner
    tuner = LatencyTuner(args.script, stages)
    tuner.script_globals = script_globals

    latencies = {}
    try:
        latencies = tuner.run_benchmark()
    except ValueError as e:
        print(e)
        return

    print("Latency Breakdown:")
    for stage, latency in latencies.items():
        print(f"{stage}: {latency:.4f} seconds")

    suggestions = tuner.suggest_optimizations(latencies)
    if suggestions:
        print("\nOptimization Suggestions:")
        for suggestion in suggestions:
            print(f"- {suggestion}")

if __name__ == "__main__":
    main()