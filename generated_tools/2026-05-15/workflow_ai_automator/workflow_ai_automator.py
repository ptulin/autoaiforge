import argparse
import json
import logging
import os
import time
from jsonschema import validate, ValidationError
import requests

def execute_workflow(workflow_file, api_key):
    """
    Executes a workflow defined in a JSON file using Claude AI.

    Args:
        workflow_file (str): Path to the JSON file defining the workflow.
        api_key (str): API key for Claude AI.

    Returns:
        dict: Execution logs and outputs.
    """
    try:
        # Load the workflow file
        with open(workflow_file, 'r') as file:
            workflow = json.load(file)

        # Validate the workflow structure
        schema = {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "task": {"type": "string"},
                            "input": {"type": "string"}
                        },
                        "required": ["task", "input"]
                    }
                }
            },
            "required": ["steps"]
        }
        validate(instance=workflow, schema=schema)

        logs = []
        outputs = []

        for step in workflow['steps']:
            task = step['task']
            input_data = step['input']

            try:
                response = requests.post(
                    "https://api.openai.com/v1/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"prompt": input_data, "model": "claude-v1"}
                )

                if response.status_code == 200:
                    result = response.json()
                    outputs.append({"task": task, "output": result.get("choices", [{}])[0].get("text", "")})
                    logs.append(f"Task '{task}' completed successfully.")
                else:
                    logs.append(f"Task '{task}' failed with status code {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                logs.append(f"Task '{task}' encountered an error: {str(e)}")

        return {"logs": logs, "outputs": outputs}

    except FileNotFoundError:
        logging.error(f"Workflow file '{workflow_file}' not found.")
        return {"logs": [f"Workflow file '{workflow_file}' not found."], "outputs": []}

    except ValidationError as e:
        logging.error(f"Invalid workflow file format: {str(e)}")
        return {"logs": [f"Invalid workflow file format: {str(e)}"], "outputs": []}

def main():
    parser = argparse.ArgumentParser(description="Workflow AI Automator")
    parser.add_argument("--workflow", required=True, help="Path to the workflow JSON file")
    parser.add_argument("--api-key", required=True, help="API key for Claude AI")

    args = parser.parse_args()

    result = execute_workflow(args.workflow, args.api_key)

    print("Execution Logs:")
    for log in result["logs"]:
        print(log)

    print("\nTask Outputs:")
    for output in result["outputs"]:
        print(f"Task: {output['task']}, Output: {output['output']}")

if __name__ == "__main__":
    main()
