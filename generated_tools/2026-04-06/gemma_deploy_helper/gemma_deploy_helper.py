import os
import sys
import logging
import click
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def detect_hardware(device_preference):
    """Detect available hardware based on user preference."""
    if device_preference == 'gpu' and torch.cuda.is_available():
        return 'cuda'
    return 'cpu'

def download_model(model_name):
    """Download the specified model and tokenizer."""
    try:
        logging.info(f"Downloading model {model_name}...")
        model = AutoModelForCausalLM.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        logging.info("Model and tokenizer downloaded successfully.")
        return model, tokenizer
    except Exception as e:
        logging.error(f"Failed to download model {model_name}: {e}")
        sys.exit(1)

def launch_server(model, tokenizer, device, batch_size, port):
    """Launch the model server."""
    try:
        logging.info(f"Launching server on port {port} with batch size {batch_size}...")
        logging.info(f"Model running on {device}.")
        # Placeholder for actual server logic
        logging.info("Server is running. Press Ctrl+C to stop.")
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
    except Exception as e:
        logging.error(f"Error while running server: {e}")
        sys.exit(1)
@click.command()
@click.option('--model', required=True, help='Name of the model to deploy (e.g., gemma-4).')
@click.option('--device', default='auto', type=click.Choice(['auto', 'cpu', 'gpu']), help='Hardware preference (auto, cpu, gpu).')
@click.option('--batch-size', default=1, type=int, help='Batch size for inference.')
@click.option('--port', default=8080, type=int, help='Port to run the server on.')
def main(model, device, batch_size, port):
    """Main function to handle CLI arguments and start the deployment."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Gemma Deploy Helper...")

    # Detect hardware
    actual_device = detect_hardware(device)
    logging.info(f"Using device: {actual_device}")

    # Download model
    model, tokenizer = download_model(model)

    # Launch server
    launch_server(model, tokenizer, actual_device, batch_size, port)

if __name__ == "__main__":
    main()