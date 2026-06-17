import argparse
import time
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

def load_model(model_name):
    """Load a pre-trained model and tokenizer."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Failed to load model '{model_name}': {e}")

def run_inference(model, tokenizer, dataset):
    """Run inference on the dataset using the provided model and tokenizer."""
    results = []
    latencies = []

    for text in dataset:
        inputs = tokenizer(text, return_tensors="pt")
        start_time = time.time()
        with torch.no_grad():
            outputs = model.generate(**inputs)
        latency = time.time() - start_time
        latencies.append(latency)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        results.append({"input": text, "output": generated_text, "latency": latency})

    return results, latencies

def compute_metrics(latencies):
    """Compute performance metrics based on latencies."""
    return {
        "mean_latency": float(np.mean(latencies)),
        "max_latency": float(np.max(latencies)),
        "min_latency": float(np.min(latencies))
    }

def load_dataset(file_path):
    """Load dataset from a text file."""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise RuntimeError(f"Dataset file '{file_path}' not found.")

def main():
    parser = argparse.ArgumentParser(description="LLM Experiment Runner")
    parser.add_argument('--dataset', required=True, help="Path to the text dataset file.")
    parser.add_argument('--model', required=True, help="Pre-trained model name (e.g., glm-5.2).")
    parser.add_argument('--output', help="Path to save the results as a JSON file.")

    args = parser.parse_args()

    try:
        dataset = load_dataset(args.dataset)
        model, tokenizer = load_model(args.model)
        results, latencies = run_inference(model, tokenizer, dataset)
        metrics = compute_metrics(latencies)

        output = {
            "results": results,
            "metrics": metrics
        }

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=4)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(output, indent=4))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
