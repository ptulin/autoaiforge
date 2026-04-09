import argparse
import yaml
import json
import logging
import httpx
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_workflow(file_path):
    """Load the workflow definition from a YAML file."""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Workflow file not found: {file_path}")
        raise
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
        raise

def execute_task(task):
    """Execute a single task defined in the workflow."""
    try:
        logging.info(f"Executing task: {task['name']}")
        response = httpx.post(task['endpoint'], json=task['parameters'], headers={'Authorization': f"Bearer {task['api_key']}"})
        response.raise_for_status()
        logging.info(f"Task {task['name']} completed successfully.")
        return {"task": task['name'], "result": response.json()}
    except httpx.RequestError as e:
        logging.error(f"Network error during task {task['name']}: {e}")
        return {"task": task['name'], "error": str(e)}
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error during task {task['name']}: {e}")
        return {"task": task['name'], "error": str(e)}

def execute_workflow(workflow):
    """Execute the workflow tasks based on the configuration."""
    results = []
    if workflow.get('execution_mode') == 'parallel':
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(execute_task, task) for task in workflow['tasks']]
            for future in futures:
                results.append(future.result())
    else:  # Sequential execution
        for task in workflow['tasks']:
            results.append(execute_task(task))
    return results

def main():
    parser = argparse.ArgumentParser(description='Claude Workflow Manager')
    parser.add_argument('--workflow', required=True, help='Path to the YAML workflow file')
    parser.add_argument('--output', required=True, help='Path to save the JSON results')
    args = parser.parse_args()

    try:
        workflow = load_workflow(args.workflow)
        results = execute_workflow(workflow)
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        logging.info(f"Workflow execution completed. Results saved to {args.output}")
    except Exception as e:
        logging.error(f"Error during workflow execution: {e}")

if __name__ == '__main__':
    main()
