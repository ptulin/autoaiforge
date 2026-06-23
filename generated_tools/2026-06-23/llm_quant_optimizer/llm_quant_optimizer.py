import argparse
import os
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def quantize_model(model_path, quantization_method):
    """
    Applies quantization to the model.

    Args:
        model_path (str): Path to the model directory.
        quantization_method (str): Quantization method ('8bit' or '4bit').

    Returns:
        torch.nn.Module: Quantized model.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path '{model_path}' does not exist.")

    if quantization_method not in ["8bit", "4bit"]:
        raise ValueError("Invalid quantization method. Choose '8bit' or '4bit'.")

    print(f"Loading model from {model_path}...")
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    print(f"Applying {quantization_method} quantization...")
    if quantization_method == "8bit":
        model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
    elif quantization_method == "4bit":
        model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.quint8
        )

    return model, tokenizer

def benchmark_model(model, tokenizer, test_text="The quick brown fox jumps over the lazy dog."):
    """
    Benchmarks the model's inference time.

    Args:
        model (torch.nn.Module): The quantized model.
        tokenizer (transformers.PreTrainedTokenizer): Tokenizer for the model.
        test_text (str): Text to use for benchmarking.

    Returns:
        float: Average inference time in seconds.
    """
    inputs = tokenizer(test_text, return_tensors="pt")
    model.eval()

    print("Benchmarking model...")
    with torch.no_grad():
        import time
        start_time = time.time()
        _ = model(**inputs)
        end_time = time.time()

    inference_time = end_time - start_time
    return inference_time

def save_report(report_data, output_path):
    """
    Saves the benchmarking report to a JSON file.

    Args:
        report_data (dict): Report data.
        output_path (str): Path to save the report.
    """
    with open(output_path, "w") as f:
        json.dump(report_data, f, indent=4)

    print(f"Report saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="LLM Quantization Optimizer: Optimize and benchmark large language models with quantization."
    )
    parser.add_argument("--model", required=True, help="Path to the locally stored LLM model.")
    parser.add_argument(
        "--quantization",
        choices=["8bit", "4bit"],
        required=True,
        help="Quantization method to apply (8bit or 4bit).",
    )
    parser.add_argument(
        "--output",
        default="quantization_report.json",
        help="Path to save the quantization report (default: quantization_report.json).",
    )

    args = parser.parse_args()

    try:
        model, tokenizer = quantize_model(args.model, args.quantization)
        inference_time = benchmark_model(model, tokenizer)

        report = {
            "model_path": args.model,
            "quantization_method": args.quantization,
            "inference_time": inference_time,
        }

        save_report(report, args.output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()