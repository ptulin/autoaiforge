import os
import sys
import torch
import argparse
from torch.quantization import quantize_dynamic, prepare, convert

def quantize_model(model_path, quantization_type, output_path):
    """
    Applies quantization to a given PyTorch model and saves the quantized model.

    :param model_path: Path to the pre-trained PyTorch model file.
    :param quantization_type: Type of quantization ('dynamic' or 'static').
    :param output_path: Path to save the quantized model.
    """
    try:
        # Load the model
        model = torch.load(model_path)

        if quantization_type == 'dynamic':
            # Apply dynamic quantization
            quantized_model = quantize_dynamic(
                model, {torch.nn.Linear}, dtype=torch.qint8
            )
        elif quantization_type == 'static':
            # Apply static quantization
            model.eval()
            prepared_model = prepare(model)
            quantized_model = convert(prepared_model)
        else:
            raise ValueError("Unsupported quantization type.")

        # Save the quantized model
        torch.save(quantized_model, output_path)
        print(f"Quantized model saved to {output_path}")

    except Exception as e:
        print(f"Error during quantization: {e}", file=sys.stderr)
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Quantize a PyTorch model.")
    parser.add_argument('--model_path', required=True, type=str, help='Path to the pre-trained PyTorch model file.')
    parser.add_argument('--quantization_type', required=True, choices=['dynamic', 'static'], help='Type of quantization to apply.')
    parser.add_argument('--output_path', required=True, type=str, help='Path to save the quantized model.')

    args = parser.parse_args()

    quantize_model(args.model_path, args.quantization_type, args.output_path)