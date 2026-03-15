import argparse
import json
import os
import torch
import tensorflow as tf
import matplotlib.pyplot as plt

def analyze_pytorch_model(model_path):
    try:
        model = torch.load(model_path)
        layer_types = {}
        total_params = 0

        for name, module in model.named_modules():
            if name == "":
                continue  # Skip the top-level module itself
            layer_type = type(module).__name__
            layer_types[layer_type] = layer_types.get(layer_type, 0) + 1
            total_params += sum(p.numel() for p in module.parameters() if p.requires_grad)

        return {
            "framework": "PyTorch",
            "layer_distribution": layer_types,
            "total_parameters": total_params,
        }
    except Exception as e:
        raise ValueError(f"Error analyzing PyTorch model: {e}")

def analyze_tensorflow_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        layer_types = {}
        total_params = model.count_params()

        for layer in model.layers:
            layer_type = type(layer).__name__
            layer_types[layer_type] = layer_types.get(layer_type, 0) + 1

        return {
            "framework": "TensorFlow",
            "layer_distribution": layer_types,
            "total_parameters": total_params,
        }
    except Exception as e:
        raise ValueError(f"Error analyzing TensorFlow model: {e}")

def generate_visualization(layer_distribution, output_path):
    try:
        plt.figure(figsize=(10, 6))
        plt.bar(layer_distribution.keys(), layer_distribution.values())
        plt.xlabel("Layer Types")
        plt.ylabel("Count")
        plt.title("Layer Distribution")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(output_path)
    except Exception as e:
        raise ValueError(f"Error generating visualization: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI Model Profiler")
    parser.add_argument("--model", required=True, help="Path to the pretrained model file")
    parser.add_argument("--output", required=True, help="Path to save the JSON report")
    parser.add_argument("--chart", help="Path to save the visualization chart (optional)")

    args = parser.parse_args()

    model_path = args.model
    output_path = args.output
    chart_path = args.chart

    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' does not exist.")
        return

    try:
        if model_path.endswith(".pt"):
            analysis = analyze_pytorch_model(model_path)
        elif model_path.endswith(".h5"):
            analysis = analyze_tensorflow_model(model_path)
        else:
            print("Error: Unsupported model format. Use .pt for PyTorch or .h5 for TensorFlow.")
            return

        with open(output_path, "w") as f:
            json.dump(analysis, f, indent=4)

        print(f"Analysis saved to {output_path}")

        if chart_path:
            generate_visualization(analysis["layer_distribution"], chart_path)
            print(f"Visualization chart saved to {chart_path}")

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
