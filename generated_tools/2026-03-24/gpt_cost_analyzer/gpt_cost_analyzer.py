import argparse
import json
import pandas as pd
import numpy as np
from openai import OpenAIError

def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def calculate_tokens_per_dollar(pricing_data, model, token_count):
    if model not in pricing_data:
        raise ValueError(f"Model '{model}' not found in pricing data.")

    model_pricing = pricing_data[model]
    if 'price_per_1k_tokens' not in model_pricing:
        raise ValueError(f"Pricing data for model '{model}' is incomplete.")

    price_per_1k_tokens = model_pricing['price_per_1k_tokens']
    if price_per_1k_tokens <= 0:
        raise ValueError(f"Invalid price for model '{model}': {price_per_1k_tokens}")

    return token_count / (price_per_1k_tokens * 1000)

def analyze_costs(prompts, models, pricing_data):
    results = []

    for model in models:
        total_tokens = sum(len(prompt.split()) for prompt in prompts)
        try:
            tokens_per_dollar = calculate_tokens_per_dollar(pricing_data, model, total_tokens)
            results.append({
                'model': model,
                'total_tokens': total_tokens,
                'tokens_per_dollar': tokens_per_dollar
            })
        except ValueError as e:
            results.append({
                'model': model,
                'error': str(e)
            })

    return results

def save_results(results, output_file, output_format):
    df = pd.DataFrame(results)

    if output_format == 'csv':
        df.to_csv(output_file, index=False)
    elif output_format == 'json':
        df.to_json(output_file, orient='records', indent=4)
    else:
        raise ValueError("Unsupported output format. Use 'csv' or 'json'.")

def main():
    parser = argparse.ArgumentParser(description="GPT Cost Analyzer")
    parser.add_argument('--models', required=True, help="Comma-separated list of GPT models to analyze (e.g., gpt-4,gpt-5)")
    parser.add_argument('--prompts', required=True, help="Path to JSON file containing prompts")
    parser.add_argument('--pricing', required=True, help="Path to JSON file containing pricing data")
    parser.add_argument('--output', required=True, help="Path to output file (CSV or JSON format)")
    parser.add_argument('--format', required=True, choices=['csv', 'json'], help="Output file format")

    args = parser.parse_args()

    try:
        models = args.models.split(',')
        prompts = load_json(args.prompts)
        pricing_data = load_json(args.pricing)

        if not isinstance(prompts, list) or not all(isinstance(p, str) for p in prompts):
            raise ValueError("Prompts file must contain a JSON array of strings.")

        results = analyze_costs(prompts, models, pricing_data)
        save_results(results, args.output, args.format)

        print("Analysis complete. Results saved to", args.output)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()