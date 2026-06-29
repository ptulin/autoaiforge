import argparse
import json
import os
import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_name):
    """Load the specified model and tokenizer."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Failed to load model '{model_name}': {e}")

def check_resources():
    """Check system resources and return available memory in MB."""
    memory_info = psutil.virtual_memory()
    return memory_info.available / (1024 * 1024)

def run_model(model, tokenizer, input_text):
    """Generate a response from the model given input text."""
    try:
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(inputs['input_ids'], max_length=50, num_return_sequences=1)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise RuntimeError(f"Failed to generate response: {e}")

def load_fallback_response(fallback_path):
    """Load fallback responses from a JSON file."""
    if not os.path.exists(fallback_path):
        raise FileNotFoundError(f"Fallback file '{fallback_path}' not found.")
    with open(fallback_path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="LLM Edge Runner: Run LLMs on edge devices with failover.")
    parser.add_argument('--model', required=True, help="Path or name of the model to load.")
    parser.add_argument('--fallback', required=True, help="Path to fallback JSON file.")
    parser.add_argument('--input', required=True, help="Input text for the model.")
    args = parser.parse_args()

    try:
        available_memory = check_resources()
        print(f"Available memory: {available_memory:.2f} MB")

        if available_memory < 500:  # Arbitrary threshold for low memory
            print("Low memory detected. Using fallback responses.")
            fallback_responses = load_fallback_response(args.fallback)
            print(fallback_responses.get('default', "No fallback response available."))
            return

        model, tokenizer = load_model(args.model)
        response = run_model(model, tokenizer, args.input)
        print(response)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()