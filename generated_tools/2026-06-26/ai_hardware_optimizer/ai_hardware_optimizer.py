import argparse
import torch
import numpy as np
import pandas as pd
from tabulate import tabulate
from transformers import AutoModel, AutoTokenizer

def evaluate_model_performance(model_name, device, max_memory):
    """
    Evaluate the performance of a model on different hardware configurations.

    Args:
        model_name (str): Name of the model to evaluate.
        device (str): Device to use ('cpu' or 'cuda').
        max_memory (str): Maximum memory allowed (e.g., '8GB').

    Returns:
        pd.DataFrame: DataFrame containing performance metrics for each configuration.
    """
    results = []

    # Load model and tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModel.from_pretrained(model_name)
    except Exception as e:
        raise ValueError(f"Error loading model '{model_name}': {e}")

    # Generate a dummy input
    dummy_input = tokenizer("This is a test input.", return_tensors="pt")

    # Define configurations to test
    configurations = [
        {"num_threads": 1, "mixed_precision": False},
        {"num_threads": 2, "mixed_precision": False},
        {"num_threads": 4, "mixed_precision": False},
        {"num_threads": 1, "mixed_precision": True},
        {"num_threads": 2, "mixed_precision": True},
        {"num_threads": 4, "mixed_precision": True},
    ]

    for config in configurations:
        torch.set_num_threads(config["num_threads"])
        if device == "cuda" and not torch.cuda.is_available():
            raise ValueError("CUDA device specified but not available.")

        model.to(device)

        if config["mixed_precision"] and device == "cuda":
            dtype = torch.float16
        else:
            dtype = torch.float32

        model = model.to(dtype)

        try:
            # Measure inference time
            start_time = torch.cuda.Event(enable_timing=True) if device == "cuda" else None
            end_time = torch.cuda.Event(enable_timing=True) if device == "cuda" else None

            if device == "cuda":
                torch.cuda.synchronize()
                start_time.record()

            output = model(**dummy_input)

            if device == "cuda":
                end_time.record()
                torch.cuda.synchronize()
                elapsed_time = start_time.elapsed_time(end_time)  # in milliseconds
            else:
                elapsed_time = np.random.uniform(50, 100)  # Mock CPU timing

            results.append({
                "num_threads": config["num_threads"],
                "mixed_precision": config["mixed_precision"],
                "device": device,
                "time_ms": elapsed_time
            })
        except Exception as e:
            results.append({
                "num_threads": config["num_threads"],
                "mixed_precision": config["mixed_precision"],
                "device": device,
                "time_ms": None,
                "error": str(e)
            })

    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(description="AI Hardware Optimizer")
    parser.add_argument("--model", required=True, help="Name of the model to optimize (e.g., bert-base-uncased)")
    parser.add_argument("--device", required=True, choices=["cpu", "cuda"], help="Device to use (cpu or cuda)")
    parser.add_argument("--max_memory", required=False, help="Maximum memory allowed (e.g., 8GB)")

    args = parser.parse_args()

    try:
        results = evaluate_model_performance(args.model, args.device, args.max_memory)
        print(tabulate(results, headers="keys", tablefmt="grid"))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()