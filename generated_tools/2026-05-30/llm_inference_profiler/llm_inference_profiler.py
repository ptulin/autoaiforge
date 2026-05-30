import argparse
import time
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import psutil

def profile_inference(model_name, batch_size, input_length, iterations, output_file):
    try:
        # Load model and tokenizer
        print("Loading model and tokenizer...")
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Generate dummy input
        print("Generating dummy input...")
        dummy_text = "Hello, world! " * max(1, (input_length // 13))
        inputs = tokenizer([dummy_text] * batch_size, return_tensors="pt", padding=True, truncation=True)

        # Move model and inputs to GPU if available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = model.to(device)
        inputs = {key: val.to(device) for key, val in inputs.items()}

        # Warm-up
        print("Warming up...")
        for _ in range(2):
            with torch.no_grad():
                model(**inputs)

        # Benchmarking
        print("Benchmarking...")
        latencies = []
        gpu_memory_usage = []
        for _ in range(iterations):
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            start_time = time.time()
            with torch.no_grad():
                model(**inputs)
            latency = time.time() - start_time
            latencies.append(latency)

            if torch.cuda.is_available():
                gpu_memory_usage.append(torch.cuda.memory_allocated(device))

        # Calculate statistics
        avg_latency = sum(latencies) / len(latencies)
        throughput = batch_size / avg_latency
        max_gpu_memory = max(gpu_memory_usage) if gpu_memory_usage else 0

        # Generate report
        report = {
            "model_name": model_name,
            "batch_size": batch_size,
            "input_length": input_length,
            "iterations": iterations,
            "average_latency": avg_latency,
            "throughput": throughput,
            "max_gpu_memory_usage": max_gpu_memory
        }

        # Output results
        print("\nPerformance Report:")
        print(json.dumps(report, indent=4))

        if output_file:
            with open(output_file, "w") as f:
                json.dump(report, f, indent=4)

        return report

    except Exception as e:
        print(f"Error during profiling: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="LLM Inference Profiler")
    parser.add_argument("--model", type=str, required=True, help="Name of the model to benchmark (e.g., gpt-2)")
    parser.add_argument("--batch_size", type=int, required=True, help="Batch size for inference")
    parser.add_argument("--input_length", type=int, required=True, help="Input length for each sequence")
    parser.add_argument("--iterations", type=int, required=True, help="Number of iterations to run")
    parser.add_argument("--output_file", type=str, default=None, help="Optional JSON file to save the report")

    args = parser.parse_args()

    profile_inference(
        model_name=args.model,
        batch_size=args.batch_size,
        input_length=args.input_length,
        iterations=args.iterations,
        output_file=args.output_file
    )

if __name__ == "__main__":
    main()
