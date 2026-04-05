import argparse
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline

def load_dataset(file_path):
    """Load dataset from a CSV or JSONL file."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.jsonl'):
        return pd.read_json(file_path, lines=True)
    else:
        raise ValueError("Unsupported file format. Use CSV or JSONL.")

def evaluate_model(model_name, dataset, metric):
    """Evaluate the model on the dataset using the specified metric."""
    try:
        model = pipeline("text-classification", model=model_name)
    except Exception as e:
        raise RuntimeError(f"Failed to load model '{model_name}': {e}")

    results = []
    for _, row in dataset.iterrows():
        try:
            prediction = model(row['text'])[0]
            if metric == 'accuracy':
                results.append(prediction['label'] == row['label'])
            elif metric == 'perplexity':
                # Placeholder for perplexity calculation
                results.append(1.0)  # Replace with actual perplexity logic
            else:
                raise ValueError("Unsupported metric. Use 'accuracy' or 'perplexity'.")
        except Exception as e:
            results.append(None)  # Handle errors gracefully

    dataset['result'] = results
    return dataset

def generate_visualizations(dataset, metric, output_dir):
    """Generate heatmaps and line charts for performance trends."""
    os.makedirs(output_dir, exist_ok=True)

    # Heatmap
    heatmap_data = dataset.pivot_table(index='label', columns='text', values='result', aggfunc='mean')
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
    plt.title(f"Heatmap of {metric} by label and text")
    heatmap_path = os.path.join(output_dir, 'heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()

    # Line chart
    line_chart_data = dataset.groupby('label')['result'].mean()
    line_chart_data.plot(kind='line', marker='o')
    plt.title(f"Line Chart of {metric} by label")
    plt.xlabel('Label')
    plt.ylabel(metric.capitalize())
    line_chart_path = os.path.join(output_dir, 'line_chart.png')
    plt.savefig(line_chart_path)
    plt.close()

    return heatmap_path, line_chart_path

def main():
    parser = argparse.ArgumentParser(description="LLM Performance Visualizer")
    parser.add_argument('--model', required=True, help="Hugging Face model name (e.g., gpt2)")
    parser.add_argument('--dataset', required=True, help="Path to dataset file (CSV/JSONL)")
    parser.add_argument('--metric', required=True, choices=['accuracy', 'perplexity'], help="Evaluation metric")
    parser.add_argument('--output_dir', default='output', help="Directory to save visualizations and report")
    args = parser.parse_args()

    try:
        dataset = load_dataset(args.dataset)
        evaluated_dataset = evaluate_model(args.model, dataset, args.metric)

        heatmap_path, line_chart_path = generate_visualizations(evaluated_dataset, args.metric, args.output_dir)

        report_path = os.path.join(args.output_dir, 'report.csv')
        evaluated_dataset.to_csv(report_path, index=False)

        print(f"Visualizations saved to: {heatmap_path}, {line_chart_path}")
        print(f"Report saved to: {report_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()