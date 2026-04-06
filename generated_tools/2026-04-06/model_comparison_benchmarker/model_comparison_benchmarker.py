import argparse
import time
import json
import os
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import matplotlib.pyplot as plt

def load_dataset(file_path):
    try:
        data = pd.read_csv(file_path)
        if 'text' not in data.columns or 'label' not in data.columns:
            raise ValueError("Dataset must contain 'text' and 'label' columns.")
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to load dataset: {e}")

def evaluate_model(model_name, dataset, batch_size):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        texts = dataset['text'].tolist()
        labels = dataset['label'].tolist()
        
        start_time = time.time()
        
        inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = model(**inputs)
        
        latency = time.time() - start_time
        accuracy = (torch.argmax(outputs.logits, dim=1) == torch.tensor(labels)).float().mean().item()
        
        memory_usage = torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
        
        return {
            "latency": latency,
            "accuracy": accuracy,
            "memory_usage": memory_usage
        }
    except Exception as e:
        raise RuntimeError(f"Failed to evaluate model {model_name}: {e}")

def benchmark(models, datasets, batch_size):
    results = {}
    for model_name in models:
        model_results = {}
        for dataset_path in datasets:
            dataset = load_dataset(dataset_path)
            model_results[os.path.basename(dataset_path)] = evaluate_model(model_name, dataset, batch_size)
        results[model_name] = model_results
    return results

def export_results(results, output_format, output_file):
    if output_format == "json":
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
    elif output_format == "csv":
        rows = []
        for model, datasets in results.items():
            for dataset, metrics in datasets.items():
                rows.append({"model": model, "dataset": dataset, **metrics})
        pd.DataFrame(rows).to_csv(output_file, index=False)
    else:
        raise ValueError("Unsupported output format. Use 'json' or 'csv'.")

def main():
    parser = argparse.ArgumentParser(description="Model Comparison Benchmarker")
    parser.add_argument("--models", required=True, nargs="+", help="List of model names to benchmark")
    parser.add_argument("--datasets", required=True, nargs="+", help="List of dataset file paths")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for evaluation")
    parser.add_argument("--output-format", choices=["json", "csv"], default="json", help="Output format for benchmarking results")
    parser.add_argument("--output-file", default="benchmark_results.json", help="Output file path")
    
    args = parser.parse_args()
    
    results = benchmark(args.models, args.datasets, args.batch_size)
    export_results(results, args.output_format, args.output_file)
    print(f"Benchmarking completed. Results saved to {args.output_file}")

if __name__ == "__main__":
    main()