import argparse
import yaml
import json
import os
import ray
import psutil
from transformers import pipeline

def load_config(config_path):
    """Load cluster configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def load_input_data(input_path):
    """Load input data from a JSON file."""
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input data file '{input_path}' not found.")
    with open(input_path, 'r') as file:
        return json.load(file)

def initialize_ray_cluster(cluster_config):
    """Initialize Ray cluster with the given configuration."""
    ray.init(address=cluster_config.get('address', 'auto'))

def run_inference(data, model_name):
    """Run inference on the data using the specified model."""
    inference_pipeline = pipeline("text-generation", model=model_name)
    return [inference_pipeline(item)[0]['generated_text'] for item in data]

@ray.remote
def distributed_inference(data_chunk, model_name):
    """Distributed inference using Ray remote function."""
    return run_inference(data_chunk, model_name)

def distribute_tasks(input_data, cluster_config):
    """Distribute tasks across the cluster nodes."""
    num_nodes = len(cluster_config['nodes'])
    model_name = cluster_config['model']
    chunk_size = max(1, len(input_data) // num_nodes)
    chunks = [input_data[i:i + chunk_size] for i in range(0, len(input_data), chunk_size)]

    tasks = [distributed_inference.remote(chunk, model_name) for chunk in chunks]
    results = ray.get(tasks)
    return [item for sublist in results for item in sublist]

def main():
    parser = argparse.ArgumentParser(description="Selixes Cluster Manager")
    parser.add_argument('--config', required=True, help="Path to the cluster configuration YAML file.")
    parser.add_argument('--input', required=True, help="Path to the input data JSON file.")
    parser.add_argument('--output', required=True, help="Path to save the aggregated results JSON file.")

    args = parser.parse_args()

    try:
        cluster_config = load_config(args.config)
        input_data = load_input_data(args.input)

        initialize_ray_cluster(cluster_config)
        results = distribute_tasks(input_data, cluster_config)

        with open(args.output, 'w') as output_file:
            json.dump(results, output_file)

        print(f"Inference completed. Results saved to '{args.output}'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
