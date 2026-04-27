import argparse
import yaml
import torch
from transformers import AutoModel

def freeze_model_layers(model, layers_to_freeze):
    """
    Freezes the specified layers of a Hugging Face model.

    Args:
        model (torch.nn.Module): The Hugging Face model.
        layers_to_freeze (list): List of layer names to freeze.

    Returns:
        torch.nn.Module: The model with specified layers frozen.
    """
    for name, param in model.named_parameters():
        param.requires_grad = not any(layer in name for layer in layers_to_freeze)
    return model

def load_config(config_path):
    """
    Loads the YAML configuration file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    parser = argparse.ArgumentParser(description="Model Parameter Freezer")
    parser.add_argument("--model", type=str, required=True, help="Pre-trained model checkpoint")
    parser.add_argument("--config", type=str, required=True, help="YAML configuration file specifying frozen layers")
    parser.add_argument("--output", type=str, required=False, help="Path to save the modified model")

    args = parser.parse_args()

    # Load the model
    try:
        model = AutoModel.from_pretrained(args.model)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Load the configuration
    try:
        config = load_config(args.config)
        layers_to_freeze = config.get("freeze_layers", [])
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return

    # Freeze specified layers
    model = freeze_model_layers(model, layers_to_freeze)

    # Optionally save the model
    if args.output:
        try:
            model.save_pretrained(args.output)
            print(f"Modified model saved to {args.output}")
        except Exception as e:
            print(f"Error saving model: {e}")

if __name__ == "__main__":
    main()
