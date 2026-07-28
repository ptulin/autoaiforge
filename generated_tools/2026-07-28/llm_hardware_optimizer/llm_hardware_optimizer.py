import argparse
import os
import psutil
import torch
import yaml

def profile_hardware():
    """Profiles local hardware capabilities."""
    hardware_info = {
        "cpu_count": psutil.cpu_count(logical=True),
        "total_memory_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "gpu_available": torch.cuda.is_available(),
        "gpu_count": torch.cuda.device_count(),
        "gpu_details": []
    }

    if hardware_info["gpu_available"]:
        for i in range(hardware_info["gpu_count"]):
            gpu_properties = torch.cuda.get_device_properties(i)
            hardware_info["gpu_details"].append({
                "name": gpu_properties.name,
                "memory_gb": round(gpu_properties.total_memory / (1024 ** 3), 2),
                "compute_capability": f"{gpu_properties.major}.{gpu_properties.minor}"
            })

    return hardware_info

def generate_configuration(hardware_info):
    """Generates an optimized configuration based on hardware info."""
    config = {
        "batch_size": 32,
        "precision": "FP32",
        "parallelism": "none"
    }

    if hardware_info["gpu_available"]:
        config["precision"] = "FP16"
        config["parallelism"] = "data_parallel" if hardware_info["gpu_count"] > 1 else "none"

        # Adjust batch size based on GPU memory
        if hardware_info["gpu_details"]:
            min_gpu_memory = min(gpu["memory_gb"] for gpu in hardware_info["gpu_details"])
            if min_gpu_memory >= 16:
                config["batch_size"] = 64
            elif min_gpu_memory >= 8:
                config["batch_size"] = 32
            else:
                config["batch_size"] = 16

    else:
        # Adjust batch size for CPU-only systems
        if hardware_info["total_memory_gb"] >= 16:
            config["batch_size"] = 16
        elif hardware_info["total_memory_gb"] >= 8:
            config["batch_size"] = 8
        else:
            config["batch_size"] = 4

    return config

def save_configuration(config, output_path):
    """Saves the configuration to a file in YAML or JSON format."""
    _, ext = os.path.splitext(output_path)
    ext = ext.lower()

    if ext == ".yaml" or ext == ".yml":
        with open(output_path, "w") as file:
            yaml.dump(config, file)
    elif ext == ".json":
        import json
        with open(output_path, "w") as file:
            json.dump(config, file, indent=4)
    else:
        raise ValueError("Unsupported file format. Use .yaml or .json.")

def main():
    parser = argparse.ArgumentParser(description="LLM Hardware Optimizer")
    parser.add_argument("--output", required=True, help="Path to save the configuration file (e.g., config.yaml or config.json)")
    args = parser.parse_args()

    try:
        hardware_info = profile_hardware()
        config = generate_configuration(hardware_info)
        save_configuration(config, args.output)
        print(f"Configuration saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
