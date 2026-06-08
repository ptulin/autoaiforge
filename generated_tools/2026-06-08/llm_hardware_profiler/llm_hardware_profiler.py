import argparse
import json
import time
import psutil
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def benchmark_model(model_name, framework, batch_size, output_file=None):
    if framework != "huggingface":
        raise ValueError("Currently, only the 'huggingface' framework is supported.")

    try:
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model.eval()

        # Generate dummy input
        input_text = "Hello, how are you?" * batch_size
        inputs = tokenizer([input_text] * batch_size, return_tensors="pt", padding=True, truncation=True)

        # Measure memory usage before inference
        initial_memory = psutil.virtual_memory().used

        # Measure inference latency
        start_time = time.time()
        with torch.no_grad():
            _ = model(**inputs)
        end_time = time.time()

        # Measure memory usage after inference
        final_memory = psutil.virtual_memory().used

        # Calculate metrics
        latency = end_time - start_time
        memory_usage = final_memory - initial_memory

        # Collect CPU and GPU utilization
        cpu_usage = psutil.cpu_percent(interval=None)
        gpu_usage = None
        if torch.cuda.is_available():
            gpu_usage = torch.cuda.memory_allocated() / (1024 ** 2)  # Convert to MB

        # Prepare results
        results = {
            "model_name": model_name,
            "framework": framework,
            "batch_size": batch_size,
            "latency_seconds": latency,
            "memory_usage_bytes": memory_usage,
            "cpu_usage_percent": cpu_usage,
            "gpu_usage_mb": gpu_usage,
        }

        # Output results
        if output_file:
            with open(output_file, "w") as f:
                json.dump(results, f, indent=4)
        else:
            print(json.dumps(results, indent=4))

        return results

    except Exception as e:
        raise RuntimeError(f"Error during benchmarking: {e}")


def main():
    parser = argparse.ArgumentParser(description="LLM Hardware Profiler")
    parser.add_argument("--model", required=True, help="Name of the model to benchmark (e.g., gpt-2)")
    parser.add_argument("--framework", required=True, choices=["huggingface"], help="Framework to use (currently only 'huggingface' is supported)")
    parser.add_argument("--batch_size", type=int, required=True, help="Batch size for inference")
    parser.add_argument("--output", help="Optional output file to save the results as JSON")

    args = parser.parse_args()

    benchmark_model(
        model_name=args.model,
        framework=args.framework,
        batch_size=args.batch_size,
        output_file=args.output
    )

if __name__ == "__main__":
    main()