import argparse
import torch
import torch.nn.utils.prune as prune
import numpy as np
import json
import time
import os
from io import BytesIO

def load_model(model_path):
    """Load a PyTorch model from the specified path."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return torch.load(model_path)

def save_metrics(metrics, output_file):
    """Save metrics to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=4)

def measure_inference_speed(model, input_tensor):
    """Measure the inference speed of the model."""
    model.eval()
    start_time = time.time()
    with torch.no_grad():
        model(input_tensor)
    end_time = time.time()
    return end_time - start_time

def prune_model(model, method, sparsity):
    """Apply pruning to the model based on the specified method and sparsity."""
    if method == "structured":
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Linear):
                prune.ln_structured(module, name='weight', amount=sparsity, n=2, dim=0)
    elif method == "unstructured":
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Linear):
                prune.random_unstructured(module, name='weight', amount=sparsity)
    else:
        raise ValueError(f"Unsupported pruning method: {method}")
    return model

def calculate_model_size(model):
    """Calculate the size of the model in bytes."""
    buffer = BytesIO()
    torch.save(model, buffer)
    return buffer.tell()

def analyze_pruning(model_path, method, sparsity):
    """Main function to analyze model pruning."""
    model = load_model(model_path)

    # Generate a random input tensor for inference speed measurement
    input_tensor = torch.randn(1, *model.input_shape)

    # Measure initial metrics
    original_size = calculate_model_size(model)
    original_speed = measure_inference_speed(model, input_tensor)

    # Apply pruning
    pruned_model = prune_model(model, method, sparsity)

    # Measure post-pruning metrics
    pruned_size = calculate_model_size(pruned_model)
    pruned_speed = measure_inference_speed(pruned_model, input_tensor)

    # Calculate metrics
    size_reduction = (original_size - pruned_size) / original_size * 100
    speed_change = (pruned_speed - original_speed) / original_speed * 100

    # Round metrics to avoid floating-point precision issues
    metrics = {
        "original_size": original_size,
        "pruned_size": pruned_size,
        "size_reduction_percent": round(size_reduction, 2),
        "original_inference_speed": round(original_speed, 6),
        "pruned_inference_speed": round(pruned_speed, 6),
        "speed_change_percent": round(speed_change, 2)
    }

    return metrics

def main():
    parser = argparse.ArgumentParser(description="Model Pruning Analyzer")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the PyTorch model file.")
    parser.add_argument("--method", type=str, choices=["structured", "unstructured"], required=True, help="Pruning method to use.")
    parser.add_argument("--sparsity", type=float, required=True, help="Sparsity level (0 to 1).")
    parser.add_argument("--output", type=str, default="pruning_metrics.json", help="Output file for metrics.")

    args = parser.parse_args()

    try:
        metrics = analyze_pruning(args.model_path, args.method, args.sparsity)
        print(json.dumps(metrics, indent=4))
        save_metrics(metrics, args.output)
        print(f"Metrics saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()