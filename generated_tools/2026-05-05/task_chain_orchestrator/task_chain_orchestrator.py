import argparse
import json
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def call_ai_api(api_url, api_key, prompt):
    """
    Call the AI API with the given prompt.

    Args:
        api_url (str): The API endpoint URL.
        api_key (str): The API key for authentication.
        prompt (str): The input prompt for the AI model.

    Returns:
        dict: The response from the AI API.
    """
    try:
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        response = requests.post(api_url, headers=headers, json={"prompt": prompt})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return {"error": str(e)}

def execute_task_chain(config, api_url, api_key):
    """
    Execute the task chain defined in the configuration.

    Args:
        config (dict): The task chain configuration.
        api_url (str): The API endpoint URL.
        api_key (str): The API key for authentication.

    Returns:
        list: A list of results for each task in the chain.
    """
    results = []
    for task in config.get("tasks", []):
        task_type = task.get("type")
        prompt = task.get("prompt")
        condition = task.get("condition")

        if task_type == "sequential":
            logging.info(f"Executing sequential task: {prompt}")
            response = call_ai_api(api_url, api_key, prompt)
            results.append(response)
        elif task_type == "conditional":
            logging.info(f"Evaluating condition: {condition}")
            try:
                if eval(condition, {}, {"results": results}):
                    logging.info(f"Condition met, executing task: {prompt}")
                    response = call_ai_api(api_url, api_key, prompt)
                    results.append(response)
                else:
                    logging.info("Condition not met, skipping task.")
            except Exception as e:
                logging.error(f"Error evaluating condition '{condition}': {e}")
                results.append({"error": f"Condition evaluation failed: {e}"})
        else:
            logging.warning(f"Unknown task type: {task_type}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Task Chain Orchestrator")
    parser.add_argument('--config', required=True, help="Path to the JSON configuration file.")
    parser.add_argument('--api_url', required=True, help="The API endpoint URL for the AI model.")
    parser.add_argument('--api_key', required=True, help="The API key for the AI model.")
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load configuration file: {e}")
        return

    results = execute_task_chain(config, args.api_url, args.api_key)
    logging.info("Task chain execution completed.")
    logging.info(f"Results: {json.dumps(results, indent=2)}")

if __name__ == "__main__":
    main()
