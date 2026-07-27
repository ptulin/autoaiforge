import argparse
import time
import torch
import numpy as np
import pandas as pd
from tabulate import tabulate


def load_model(model_path):
    """Load a PyTorch model from a file."""
    try:
        model = torch.load(model_path)
        model.eval()
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model from {model_path}: {e}")


def evaluate_model(model, data_loader):
    """Evaluate a model on a dataset and return metrics."""
    accuracy = 0
    total_samples = 0
    correct_predictions = 0
    latency_list = []

    for inputs, labels in data_loader:
        start_time = time.time()
        with torch.no_grad():
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
        latency_list.append(time.time() - start_time)

        correct_predictions += (predicted == labels).sum().item()
        total_samples += labels.size(0)

    accuracy = correct_predictions / total_samples
    avg_latency = np.mean(latency_list)

    return {
        "accuracy": accuracy,
        "avg_latency": avg_latency,
    }


def memory_usage(model):
    """Calculate the memory usage of a model."""
    return sum(p.numel() for p in model.parameters()) * 4 / (1024 ** 2)  # Convert to MB


def main():
    parser = argparse.ArgumentParser(description="Distilled Model Evaluator")
    parser.add_argument("--student", required=True, help="Path to the student model file")
    parser.add_argument("--teacher", required=True, help="Path to the teacher model file")
    parser.add_argument("--data", required=True, help="Path to the evaluation dataset (CSV)")
    parser.add_argument("--output", help="Path to save the comparison report (CSV)")

    args = parser.parse_args()

    try:
        student_model = load_model(args.student)
        teacher_model = load_model(args.teacher)

        # Load dataset
        dataset = pd.read_csv(args.data)
        data_loader = [(torch.tensor(row[:-1].values, dtype=torch.float32), torch.tensor(row[-1], dtype=torch.long)) for _, row in dataset.iterrows()]

        student_metrics = evaluate_model(student_model, data_loader)
        teacher_metrics = evaluate_model(teacher_model, data_loader)

        student_memory = memory_usage(student_model)
        teacher_memory = memory_usage(teacher_model)

        comparison = [
            ["Metric", "Student Model", "Teacher Model"],
            ["Accuracy", f"{student_metrics['accuracy']:.2f}", f"{teacher_metrics['accuracy']:.2f}"],
            ["Latency (s)", f"{student_metrics['avg_latency']:.4f}", f"{teacher_metrics['avg_latency']:.4f}"],
            ["Memory Usage (MB)", f"{student_memory:.2f}", f"{teacher_memory:.2f}"],
        ]

        print(tabulate(comparison, headers="firstrow", tablefmt="grid"))

        if args.output:
            output_df = pd.DataFrame(comparison[1:], columns=comparison[0])
            output_df.to_csv(args.output, index=False)
            print(f"Comparison report saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()