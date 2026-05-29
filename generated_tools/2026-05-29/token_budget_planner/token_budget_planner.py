import json
import argparse
import matplotlib.pyplot as plt
from unittest.mock import Mock

def encoding_for_model(model):
    """Mock function to simulate tiktoken.encoding_for_model."""
    class MockEncoder:
        def encode(self, prompt):
            return [ord(char) for char in prompt]

    return MockEncoder()

def load_config(config_path):
    """Load and validate the JSON configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        if not isinstance(config, list):
            raise ValueError("Configuration file must contain a list of steps.")
        for step in config:
            if not all(key in step for key in ('name', 'prompt', 'model', 'max_tokens')):
                raise ValueError("Each step must contain 'name', 'prompt', 'model', and 'max_tokens'.")
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in configuration file.")

def estimate_tokens(prompt, model):
    """Estimate the number of tokens for a given prompt and model."""
    try:
        encoder = encoding_for_model(model)
        return len(encoder.encode(prompt))
    except KeyError:
        raise ValueError(f"Model '{model}' is not supported.")

def calculate_token_usage(config):
    """Calculate token usage for each step and check for token limit violations."""
    results = []
    for step in config:
        tokens_used = estimate_tokens(step['prompt'], step['model'])
        tokens_remaining = step['max_tokens'] - tokens_used
        results.append({
            'name': step['name'],
            'tokens_used': tokens_used,
            'tokens_remaining': tokens_remaining,
            'exceeded': tokens_remaining < 0
        })
    return results

def visualize_token_usage(results, output_path=None):
    """Generate a bar chart to visualize token usage."""
    names = [step['name'] for step in results]
    tokens_used = [step['tokens_used'] for step in results]
    tokens_remaining = [max(0, step['tokens_remaining']) for step in results]

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.4
    indices = range(len(results))

    ax.bar(indices, tokens_used, bar_width, label='Tokens Used', color='blue')
    ax.bar(indices, tokens_remaining, bar_width, bottom=tokens_used, label='Tokens Remaining', color='green')

    ax.set_xlabel('Steps')
    ax.set_ylabel('Tokens')
    ax.set_title('Token Usage per Step')
    ax.set_xticks(indices)
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Token Budget Planner')
    parser.add_argument('--config', required=True, help='Path to the JSON configuration file.')
    parser.add_argument('--output', help='Path to save the visualization image (optional).')
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        results = calculate_token_usage(config)

        print("Token Usage Report:")
        for step in results:
            print(f"Step: {step['name']}, Tokens Used: {step['tokens_used']}, Tokens Remaining: {step['tokens_remaining']}, Exceeded: {step['exceeded']}")

        visualize_token_usage(results, args.output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()