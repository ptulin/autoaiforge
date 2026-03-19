import argparse
import json
import sys
import pandas as pd
from transformers import GPT2TokenizerFast
from tiktoken import get_encoding

def tokenize_text(text, model):
    """
    Tokenizes the input text based on the specified model.
    """
    if model.startswith("gpt-4") or model.startswith("gpt-3.5"):
        encoding = get_encoding("cl100k_base")
        tokens = encoding.encode(text)
    elif model.startswith("claude"):
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        tokens = tokenizer.encode(text)
    else:
        raise ValueError(f"Unsupported model: {model}")
    return tokens

def calculate_cost(tokens, model, pricing):
    """
    Calculates the cost of using the API based on the number of tokens and pricing.
    """
    if model not in pricing:
        raise ValueError(f"Pricing information for model {model} is not available.")
    cost_per_1k_tokens = pricing[model]
    return (len(tokens) / 1000) * cost_per_1k_tokens

def main():
    parser = argparse.ArgumentParser(description="API Cost Calculator")
    parser.add_argument("--input", type=str, help="Path to the input text file. Use '-' for stdin.")
    parser.add_argument("--models", nargs='+', required=True, help="List of models to compare (e.g., gpt-4 gpt-3.5 claude-2).")
    parser.add_argument("--pricing", type=str, required=True, help="Path to JSON file with pricing information.")
    parser.add_argument("--output", type=str, choices=["human", "json"], default="human", help="Output format.")

    args = parser.parse_args()

    # Read input text
    if args.input == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File {args.input} not found.", file=sys.stderr)
            sys.exit(1)

    # Load pricing information
    try:
        with open(args.pricing, "r", encoding="utf-8") as f:
            pricing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Invalid pricing file {args.pricing}.", file=sys.stderr)
        sys.exit(1)

    # Calculate costs
    results = []
    for model in args.models:
        try:
            tokens = tokenize_text(text, model)
            cost = calculate_cost(tokens, model, pricing)
            results.append({"model": model, "tokens": len(tokens), "cost": cost})
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Output results
    if args.output == "human":
        print("Model Comparison:")
        df = pd.DataFrame(results)
        print(df.to_string(index=False))
    else:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()