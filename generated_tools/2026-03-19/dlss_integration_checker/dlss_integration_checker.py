import argparse
import yaml
import json
from OpenGL.GL import *

def check_dlss_compatibility(config_path):
    """
    Check the DLSS compatibility of a given rendering pipeline configuration.

    Args:
        config_path (str): Path to the configuration file (YAML or JSON).

    Returns:
        dict: A dictionary containing the compatibility assessment and suggestions.
    """
    try:
        with open(config_path, 'r') as file:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config = yaml.safe_load(file)
            elif config_path.endswith('.json'):
                config = json.load(file)
            else:
                return {"error": "Unsupported file format. Use YAML or JSON."}
    except FileNotFoundError:
        return {"error": "Configuration file not found."}
    except (yaml.YAMLError, json.JSONDecodeError):
        return {"error": "Invalid configuration file format."}

    # Perform checks
    results = {}

    # Check rendering API
    api = config.get('rendering_api', '').lower()
    if api not in ['directx12', 'vulkan']:  # DLSS supports DirectX 12 and Vulkan
        results['rendering_api'] = f"Unsupported API: {api}. Use DirectX 12 or Vulkan."
    else:
        results['rendering_api'] = f"Supported API: {api}."

    # Check GPU compatibility
    gpu = config.get('gpu', '').lower()
    if 'nvidia' not in gpu:
        results['gpu'] = f"Unsupported GPU: {gpu}. NVIDIA GPUs are required for DLSS."
    else:
        results['gpu'] = f"Supported GPU: {gpu}."

    # Check rendering pipeline
    pipeline = config.get('rendering_pipeline', {}).get('type', '').lower()
    if pipeline not in ['deferred', 'forward']:  # Common rendering pipelines
        results['rendering_pipeline'] = f"Unsupported rendering pipeline: {pipeline}. Use 'deferred' or 'forward'."
    else:
        results['rendering_pipeline'] = f"Supported rendering pipeline: {pipeline}."

    # Add further checks as needed

    # Provide debugging tips if there are issues
    if any('Unsupported' in value for value in results.values()):
        results['debugging_tips'] = [
            "Ensure you are using a compatible NVIDIA GPU with the latest drivers.",
            "Verify that your rendering API is set to DirectX 12 or Vulkan.",
            "Check that your rendering pipeline is either 'deferred' or 'forward'.",
        ]

    return results

def main():
    parser = argparse.ArgumentParser(description="DLSS Integration Checker")
    parser.add_argument('config_path', type=str, help="Path to the rendering pipeline configuration file (YAML or JSON).")
    args = parser.parse_args()

    results = check_dlss_compatibility(args.config_path)

    if "error" in results:
        print(f"Error: {results['error']}")
    else:
        print("DLSS Compatibility Check Results:")
        for key, value in results.items():
            if key != 'debugging_tips':
                print(f"- {key}: {value}")
        if 'debugging_tips' in results:
            print("\nDebugging Tips:")
            for tip in results['debugging_tips']:
                print(f"* {tip}")

if __name__ == "__main__":
    main()