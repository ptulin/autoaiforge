import argparse
import yaml
import requests
import psutil
from typing import List, Dict

def load_config(config_path: str) -> Dict:
    """Load the YAML configuration file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration: {e}")

def get_instance_health(instance: Dict) -> Dict:
    """Fetch the health metrics of an instance."""
    try:
        response = requests.get(instance['health_url'], timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def filter_healthy_instances(instances: List[Dict], thresholds: Dict) -> List[Dict]:
    """Filter instances based on health thresholds."""
    healthy_instances = []
    for instance in instances:
        health = get_instance_health(instance)
        if 'error' in health:
            continue

        if (health.get('latency', float('inf')) <= thresholds['latency'] and
            health.get('uptime', 0) >= thresholds['uptime'] and
            health.get('cpu_usage', 100) <= thresholds['cpu_usage'] and
            health.get('memory_usage', 100) <= thresholds['memory_usage']):
            healthy_instances.append(instance)

    return healthy_instances

def route_query(instances: List[Dict], query: str) -> str:
    """Route the query to the healthiest instance."""
    if not instances:
        raise RuntimeError("No healthy instances available.")

    # Sort instances by latency (ascending)
    sorted_instances = sorted(instances, key=lambda x: x['latency'])
    target_instance = sorted_instances[0]

    try:
        response = requests.post(target_instance['query_url'], json={"query": query}, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to route query to {target_instance['name']}: {e}")

def main():
    parser = argparse.ArgumentParser(description="LLM Health-Aware Router")
    parser.add_argument('--config', required=True, help="Path to the YAML configuration file.")
    parser.add_argument('--query', required=True, help="The query to route.")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        thresholds = config['thresholds']
        instances = config['instances']

        healthy_instances = filter_healthy_instances(instances, thresholds)
        response = route_query(healthy_instances, args.query)
        print(response)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()