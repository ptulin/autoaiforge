import argparse
import yaml
import requests
import sys

def load_config(config_path):
    """Load the routing configuration from a YAML file."""
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        sys.exit(f"Error: Configuration file '{config_path}' not found.")
    except yaml.YAMLError as e:
        sys.exit(f"Error: Failed to parse configuration file. {e}")

def select_llm(task, config):
    """Select the most suitable LLM based on the task and routing rules."""
    if task not in config['tasks']:
        raise ValueError(f"Task '{task}' is not supported.")

    candidates = config['tasks'][task]
    if not candidates:
        raise ValueError(f"No LLMs configured for task '{task}'.")

    # Sort by priority (lower is better)
    candidates.sort(key=lambda x: x['priority'])
    return candidates[0]

def call_llm(endpoint, api_key, payload):
    """Call the LLM endpoint with the given payload."""
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to LLM endpoint. {e}")

def main():
    parser = argparse.ArgumentParser(description="LLM Router Middleware")
    parser.add_argument('--task', required=True, help="The task type (e.g., summarization, translation, text_generation).")
    parser.add_argument('--input_file', required=True, help="Path to the input text file.")
    parser.add_argument('--config', required=True, help="Path to the routing configuration file (YAML format).")

    args = parser.parse_args()

    # Load input text
    try:
        with open(args.input_file, 'r') as file:
            input_text = file.read().strip()
    except FileNotFoundError:
        sys.exit(f"Error: Input file '{args.input_file}' not found.")

    if not input_text:
        sys.exit("Error: Input file is empty.")

    # Load configuration
    config = load_config(args.config)

    # Select the most suitable LLM
    try:
        selected_llm = select_llm(args.task, config)
    except ValueError as e:
        sys.exit(f"Error: {e}")

    # Prepare payload
    payload = {
        'task': args.task,
        'input': input_text
    }

    # Call the selected LLM
    try:
        response = call_llm(selected_llm['endpoint'], selected_llm['api_key'], payload)
        print(response.get('output', 'No output received from the LLM.'))
    except RuntimeError as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()
