import argparse
import yaml
import paramiko
import os
from typing import List, Dict

def parse_nodes(nodes: str) -> List[Dict[str, str]]:
    """Parse the nodes argument into a list of dictionaries."""
    node_list = []
    for node in nodes.split(','):
        try:
            ip, gpus = node.split(':')
            node_list.append({'ip': ip, 'gpus': int(gpus)})
        except ValueError:
            raise ValueError(f"Invalid node format: {node}. Expected format: IP:GPUs")
    return node_list

def generate_yaml_config(nodes: List[Dict[str, str]], model: str, script: str) -> str:
    """Generate a YAML configuration for Mesh LLM."""
    config = {
        'model': model,
        'script': script,
        'nodes': [
            {'ip': node['ip'], 'gpus': node['gpus']} for node in nodes
        ]
    }
    return yaml.dump(config, sort_keys=False)

def validate_nodes(nodes: List[Dict[str, str]]) -> None:
    """Validate node connectivity and resource availability."""
    for node in nodes:
        ip = node['ip']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username='root', timeout=5)
            ssh.close()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to node {ip}: {e}")

def launch_training(nodes: List[Dict[str, str]], model: str, script: str) -> None:
    """Launch the distributed training job."""
    # Simulate launching a distributed job
    print("Launching distributed training job...")
    print(f"Model: {model}")
    print(f"Script: {script}")
    print("Nodes:")
    for node in nodes:
        print(f"  - IP: {node['ip']}, GPUs: {node['gpus']}")

def main():
    parser = argparse.ArgumentParser(
        description="Mesh Orchestration Helper: Simplify distributed AI workload orchestration."
    )
    parser.add_argument('--nodes', required=True, help="Comma-separated list of nodes in the format IP:GPUs")
    parser.add_argument('--model', required=True, help="Model type (e.g., gpt3)")
    parser.add_argument('--script', required=True, help="Path to the training script")
    parser.add_argument('--output', default='mesh_config.yaml', help="Output YAML configuration file")
    parser.add_argument('--validate', action='store_true', help="Validate node connectivity")
    parser.add_argument('--launch', action='store_true', help="Launch the distributed training job")

    args = parser.parse_args()

    try:
        nodes = parse_nodes(args.nodes)
        if args.validate:
            validate_nodes(nodes)

        yaml_config = generate_yaml_config(nodes, args.model, args.script)
        with open(args.output, 'w') as f:
            f.write(yaml_config)
        print(f"Configuration saved to {args.output}")

        if args.launch:
            launch_training(nodes, args.model, args.script)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
