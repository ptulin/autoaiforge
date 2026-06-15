import argparse
import json
import os
from rich.console import Console
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def load_model(model_name, device):
    """Load the specified model and tokenizer on the given device."""
    console = Console()
    try:
        console.print(f"[bold green]Loading model '{model_name}' on {device}...[/bold green]")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model = model.to(device)
        console.print("[bold green]Model loaded successfully![/bold green]")
        return model, tokenizer
    except Exception as e:
        console.print(f"[bold red]Error loading model: {e}[/bold red]")
        raise

def parse_config(config_file):
    """Parse the configuration file for model settings."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    with open(config_file, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Local LLM Launcher")
    parser.add_argument("--model", required=True, help="Name of the model to load (e.g., 'gpt-j', 'llama-13b').")
    parser.add_argument("--device", choices=["cpu", "gpu"], default="cpu", help="Device to run the model on (default: cpu).")
    parser.add_argument("--config", required=True, help="Path to the configuration JSON file.")

    args = parser.parse_args()

    console = Console()

    try:
        config = parse_config(args.config)
        device = "cuda" if args.device == "gpu" and torch.cuda.is_available() else "cpu"
        model, tokenizer = load_model(args.model, device)

        console.print("[bold green]Model is ready for interaction![/bold green]")
        console.print("[bold blue]Note: This is a placeholder. Add interaction logic as needed.[/bold blue]")

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()
