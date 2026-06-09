import argparse
import json
import logging
import psutil
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def get_device_availability(devices):
    """Check the availability of devices."""
    available_devices = {}
    for device in devices:
        if device == 'cuda' and torch.cuda.is_available():
            available_devices['cuda'] = torch.cuda.get_device_properties(0).total_memory - torch.cuda.memory_allocated(0)
        elif device == 'cpu':
            available_devices['cpu'] = psutil.virtual_memory().available
    return available_devices

def load_model(model_name, device):
    """Load the specified model and tokenizer on the given device."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        if device == 'cuda' and torch.cuda.is_available():
            model = model.to('cuda')
        return model, tokenizer
    except Exception as e:
        logging.error(f"Error loading model {model_name} on {device}: {e}")
        raise

def route_request(input_text, models, devices):
    """Route the request to the optimal model and device."""
    available_devices = get_device_availability(devices)
    if not available_devices:
        raise RuntimeError("No available devices.")

    # Sort devices by available memory (descending)
    sorted_devices = sorted(available_devices.items(), key=lambda x: x[1], reverse=True)

    for device, _ in sorted_devices:
        for model_name in models:
            try:
                model, tokenizer = load_model(model_name, device)
                inputs = tokenizer(input_text, return_tensors="pt")
                if device == 'cuda':
                    inputs = {key: value.to('cuda') for key, value in inputs.items()}
                outputs = model.generate(**inputs)
                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                return {
                    "model": model_name,
                    "device": device,
                    "response": response
                }
            except Exception as e:
                logging.warning(f"Failed to process with model {model_name} on {device}: {e}")
    raise RuntimeError("Failed to process the request with all available models and devices.")

def main():
    parser = argparse.ArgumentParser(description="Dynamic LLM Router")
    parser.add_argument('--input', type=str, required=True, help="Input text for the LLM.")
    parser.add_argument('--models', type=str, required=True, help="Comma-separated list of model names.")
    parser.add_argument('--devices', type=str, required=True, help="Comma-separated list of devices (e.g., cuda,cpu).")

    args = parser.parse_args()

    input_text = args.input
    models = args.models.split(',')
    devices = args.devices.split(',')

    try:
        result = route_request(input_text, models, devices)
        print(json.dumps(result, indent=2))
    except Exception as e:
        logging.error(f"Error: {e}")
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    setup_logging()
    main()