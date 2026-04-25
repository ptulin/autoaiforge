import json
import argparse
from typing import List, Union, Dict

def count_tokens(prompt: str, model: str = "gpt-4") -> int:
    """Counts the number of tokens in a prompt using a mock tokenizer."""
    try:
        # Simulate token count logic based on word count for testing purposes
        return len(prompt.split())
    except Exception as e:
        raise ValueError(f"Error counting tokens: {e}")

def estimate_cost(token_count: int, model: str = "gpt-4") -> float:
    """Estimates the cost of processing a prompt based on token count."""
    # Example pricing (adjust based on actual API pricing)
    pricing = {
        "gpt-4": 0.03 / 1000,  # $0.03 per 1k tokens
        "claude-v1": 0.02 / 1000  # $0.02 per 1k tokens
    }
    if model not in pricing:
        raise ValueError(f"Unsupported model for cost estimation: {model}")
    return token_count * pricing[model]

def analyze_prompt(prompt: str, model: str = "gpt-4") -> Dict[str, Union[str, int, float]]:
    """Analyzes a single prompt for token count, cost, and optimization suggestions."""
    token_count = count_tokens(prompt, model)
    cost = estimate_cost(token_count, model)

    suggestions = []
    if token_count > 1000:
        suggestions.append("Consider shortening the prompt to reduce token usage.")
    if len(prompt.split()) < 10:
        suggestions.append("The prompt is very short. Consider adding more context.")
    if not prompt.endswith("?"):
        suggestions.append("Consider rephrasing the prompt as a question for clarity.")

    return {
        "original_prompt": prompt,
        "token_count": token_count,
        "estimated_cost": cost,
        "suggestions": suggestions
    }

def optimize_prompt(input_data: Union[str, List[str]], model: str = "gpt-4") -> List[Dict[str, Union[str, int, float]]]:
    """Optimizes one or more prompts and returns analysis results."""
    if isinstance(input_data, str):
        input_data = [input_data]
    elif not isinstance(input_data, list):
        raise ValueError("Input must be a string or a list of strings.")

    results = []
    for prompt in input_data:
        if not isinstance(prompt, str):
            raise ValueError("Each prompt must be a string.")
        results.append(analyze_prompt(prompt, model))

    return results

def main():
    parser = argparse.ArgumentParser(description="LLM Input Optimizer")
    parser.add_argument("--input", type=str, required=True, help="Input prompt or JSON array of prompts.")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for tokenization (default: gpt-4).")

    args = parser.parse_args()

    try:
        input_data = json.loads(args.input) if args.input.strip().startswith("[") else args.input
        results = optimize_prompt(input_data, args.model)
        print(json.dumps(results, indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()