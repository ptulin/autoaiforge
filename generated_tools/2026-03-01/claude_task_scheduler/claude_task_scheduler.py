import argparse
import yaml
import httpx
import os
import json
from datetime import datetime

def create_task(task_name, interval, prompt, output, api_url, api_key):
    """
    Create a task in the Claude AI ecosystem.

    Args:
        task_name (str): Name of the task.
        interval (str): Recurrence interval (e.g., '24h').
        prompt (str): Prompt to send to Claude AI.
        output (str): Output file to save results.
        api_url (str): Claude API endpoint.
        api_key (str): API key for authentication.

    Returns:
        dict: Response from the API.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "task_name": task_name,
        "interval": interval,
        "prompt": prompt
    }

    try:
        response = httpx.post(f"{api_url}/tasks", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if output:
            with open(output, "w") as f:
                json.dump(result, f, indent=4)

        return result
    except httpx.RequestError as e:
        raise RuntimeError(f"An error occurred while communicating with the API: {e}")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"API returned an error: {e.response.text}")

def load_config(config_file):
    """
    Load configuration from a YAML file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration data.
    """
    try:
        with open(config_file, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {config_file} not found.")
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML configuration: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Task Scheduler")
    parser.add_argument("--task-name", required=False, help="Name of the task to schedule.")
    parser.add_argument("--interval", required=False, help="Recurrence interval (e.g., '24h').")
    parser.add_argument("--prompt", required=False, help="Prompt to send to Claude AI.")
    parser.add_argument("--output", required=False, help="Output file to save results.")
    parser.add_argument("--config", required=False, help="Path to YAML configuration file.")
    parser.add_argument("--api-url", required=True, help="Claude API endpoint.")
    parser.add_argument("--api-key", required=True, help="API key for authentication.")

    args = parser.parse_args()

    if args.config:
        config = load_config(args.config)
        task_name = config.get("task_name")
        interval = config.get("interval")
        prompt = config.get("prompt")
        output = config.get("output")
    else:
        task_name = args.task_name
        interval = args.interval
        prompt = args.prompt
        output = args.output

    if not task_name or not interval or not prompt:
        parser.error("--task-name, --interval, and --prompt are required unless using --config.")

    try:
        result = create_task(task_name, interval, prompt, output, args.api_url, args.api_key)
        print("Task created successfully:")
        print(json.dumps(result, indent=4))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()