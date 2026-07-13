import argparse
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import os

def load_model(model_path):
    """Load the pre-trained model and tokenizer."""
    try:
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")

def simulate_intervention(model, tokenizer, sequence, components):
    """Simulate interventions on specific components of the model."""
    try:
        inputs = tokenizer(sequence, return_tensors="pt")
        original_outputs = model(**inputs, output_hidden_states=True)

        # Clone the model to simulate intervention
        intervened_model = model

        # Apply interventions (mock example: zero out specific neurons)
        for component in components:
            if component.startswith("neuron_"):
                neuron_idx = int(component.split("_")[1])
                for layer in intervened_model.transformer.h:
                    layer.mlp.c_proj.weight.data[neuron_idx] = 0

        intervened_outputs = intervened_model(**inputs, output_hidden_states=True)

        # Extract logits and compute metrics
        original_logits = original_outputs.logits.detach().numpy()
        intervened_logits = intervened_outputs.logits.detach().numpy()

        return original_logits, intervened_logits

    except Exception as e:
        raise RuntimeError(f"Error during intervention simulation: {e}")

def save_results_to_csv(original_logits, intervened_logits, output_file):
    """Save the results to a CSV file."""
    try:
        original_logits_flat = original_logits.flatten()
        intervened_logits_flat = intervened_logits.flatten()

        df = pd.DataFrame({
            "Original Logits": original_logits_flat,
            "Intervened Logits": intervened_logits_flat
        })
        df.to_csv(output_file, index=False)
    except Exception as e:
        raise RuntimeError(f"Error saving results to CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description="Causal Intervention Simulator")
    parser.add_argument("--model", required=True, help="Path to the pre-trained model")
    parser.add_argument("--sequence", required=True, help="Input token sequence")
    parser.add_argument("--components", required=True, nargs='+', help="List of components to intervene on (e.g., neuron_45)")
    parser.add_argument("--output", required=True, help="Path to save the output CSV file")

    args = parser.parse_args()

    try:
        model, tokenizer = load_model(args.model)
        original_logits, intervened_logits = simulate_intervention(model, tokenizer, args.sequence, args.components)
        save_results_to_csv(original_logits, intervened_logits, args.output)
        print(f"Results saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
