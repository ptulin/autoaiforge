import os
import yaml
import click
import tiktoken

def load_pricing_config(config_path):
    """Load pricing configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Pricing configuration file '{config_path}' not found.")
    except yaml.YAMLError:
        raise ValueError(f"Error parsing YAML file '{config_path}'.")

def count_tokens(prompt, model):
    """Count tokens in a prompt using tiktoken for the specified model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(prompt))
    except Exception:
        raise ValueError(f"Unsupported model '{model}' for token counting.")

def estimate_cost(prompts, model, pricing_config):
    """Estimate the cost of processing prompts based on token counts and pricing."""
    if model not in pricing_config:
        raise ValueError(f"Model '{model}' not found in pricing configuration.")

    model_pricing = pricing_config[model]
    cost_per_token = model_pricing.get('cost_per_token', 0)

    total_tokens = sum(count_tokens(prompt, model) for prompt in prompts)
    total_cost = total_tokens * cost_per_token

    return total_tokens, total_cost

def read_prompts(file_path):
    """Read prompts from a text file."""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file '{file_path}' not found.")
@click.command()
@click.option('--file', 'file_path', type=click.Path(exists=True), required=True, help='Path to the file containing prompts.')
@click.option('--config', 'config_path', type=click.Path(exists=True), required=True, help='Path to the YAML pricing configuration file.')
@click.option('--llm', 'model', type=str, required=True, help='The LLM model to use for token counting.')
def main(file_path, config_path, model):
    """Main CLI entry point for the LLM Cost Estimator tool."""
    try:
        prompts = read_prompts(file_path)
        pricing_config = load_pricing_config(config_path)

        total_tokens, total_cost = estimate_cost(prompts, model, pricing_config)

        click.echo(f"Total tokens: {total_tokens}")
        click.echo(f"Estimated cost: ${total_cost:.4f}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    main()
