import argparse
import yaml
import psutil

def autodetect_hardware():
    """Autodetects hardware specifications."""
    memory = psutil.virtual_memory().total // (1024 ** 3)  # Convert bytes to GB
    cpu_count = psutil.cpu_count()
    return {
        "memory_gb": memory,
        "cpu_cores": cpu_count
    }

def generate_config(hardware_specs, model, dataset_size):
    """Generates optimized training configuration based on inputs."""
    config = {
        "model": model,
        "dataset_size": dataset_size,
        "hardware": hardware_specs,
        "training": {
            "batch_size": min(64, hardware_specs["memory_gb"] * 2),
            "num_workers": max(1, hardware_specs["cpu_cores"] // 2),
            "precision": "fp16" if hardware_specs["memory_gb"] >= 16 else "fp32"
        }
    }
    return config

def main():
    parser = argparse.ArgumentParser(description="LLM Training Optimizer")
    parser.add_argument("--model", required=True, help="Model type (e.g., gpt-j, llama, etc.)")
    parser.add_argument("--dataset_size", required=True, help="Dataset size (e.g., 10GB, 500MB)")
    parser.add_argument("--hardware_specs", help="Hardware specs as a YAML file")
    parser.add_argument("--output", default="config.yaml", help="Output configuration file")

    args = parser.parse_args()

    if args.hardware_specs:
        try:
            with open(args.hardware_specs, "r") as file:
                hardware_specs = yaml.safe_load(file)
        except FileNotFoundError:
            print("Error: Hardware specs file not found.")
            return
        except yaml.YAMLError:
            print("Error: Invalid YAML format in hardware specs file.")
            return
    else:
        hardware_specs = autodetect_hardware()

    dataset_size = args.dataset_size
    model = args.model

    config = generate_config(hardware_specs, model, dataset_size)

    try:
        with open(args.output, "w") as file:
            yaml.dump(config, file)
        print(f"Configuration saved to {args.output}")
    except Exception as e:
        print(f"Error: Unable to save configuration file. {e}")

if __name__ == "__main__":
    main()