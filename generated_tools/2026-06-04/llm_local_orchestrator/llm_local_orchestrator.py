import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import click

def load_model(model_path, device):
    """Load the model and tokenizer."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(model_path)
        model.to(device)
        return model, tokenizer
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

def run_inference(model, tokenizer, input_text, device, max_length):
    """Run inference on the input text."""
    try:
        inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
        inputs = {key: value.to(device) for key, value in inputs.items()}
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=max_length)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise RuntimeError(f"Failed during inference: {e}")

@click.command()
@click.option('--model-path', required=True, type=click.Path(exists=True), help='Path to the local model.')
@click.option('--input', required=True, type=str, help='Input text for the model.')
@click.option('--device', default='cuda' if torch.cuda.is_available() else 'cpu', type=str, help='Device to run the model on (e.g., cuda or cpu).')
@click.option('--max-length', default=128, type=int, help='Maximum length for generated text.')
def main(model_path, input, device, max_length):
    """Main CLI entry point."""
    try:
        model, tokenizer = load_model(model_path, device)
        result = run_inference(model, tokenizer, input, device, max_length)
        click.echo(result)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    main()
