import argparse
import json
import time
import numpy as np
import pandas as pd
from transformers import pipeline

def evaluate_model(model_name, task, dataset_path):
    """
    Evaluate the performance of a model on a given task and dataset.

    Args:
        model_name (str): Name or path of the model.
        task (str): Task type (e.g., 'summarization', 'text-classification').
        dataset_path (str): Path to the evaluation dataset.

    Returns:
        dict: Dictionary containing performance metrics.
    """
    try:
        # Validate task
        if task not in ['summarization', 'text-classification']:
            raise ValueError(f"Unsupported task: {task}")

        # Load the model pipeline
        model_pipeline = pipeline(task, model=model_name)

        # Load the dataset
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        dataset = [{'text': item['text']} for item in data]

        metrics = []

        for example in dataset:
            input_text = example['text']
            start_time = time.time()
            output = model_pipeline(input_text)

            # Collect metrics (e.g., latency)
            latency = time.time() - start_time
            metrics.append({
                'input': input_text,
                'output': output,
                'latency': latency
            })

        # Calculate average latency
        avg_latency = np.mean([m['latency'] for m in metrics])

        return {
            'model': model_name,
            'task': task,
            'avg_latency': avg_latency,
            'num_samples': len(metrics)
        }

    except Exception as e:
        return {
            'model': model_name,
            'task': task,
            'error': str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="AI Model Comparator")
    parser.add_argument('--models', nargs='+', required=True, help="List of model names or paths")
    parser.add_argument('--task', required=True, choices=['summarization', 'text-classification'], help="Task type")
    parser.add_argument('--dataset', required=True, help="Path to evaluation dataset in JSON format")
    parser.add_argument('--output', required=True, choices=['csv', 'json'], help="Output format")

    args = parser.parse_args()

    results = []
    for model_name in args.models:
        result = evaluate_model(model_name, args.task, args.dataset)
        results.append(result)

    if args.output == 'csv':
        df = pd.DataFrame(results)
        df.to_csv('model_comparison.csv', index=False)
        print("Results saved to model_comparison.csv")
    elif args.output == 'json':
        with open('model_comparison.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("Results saved to model_comparison.json")

if __name__ == "__main__":
    main()
