import json
import os
import logging
from pathlib import Path
from typing import Dict, Any
import requests
import typer

app = typer.Typer()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ClaudeTaskOrchestrator")

API_BASE_URL = "https://api.openai.com/v1/engines/claude/completions"

def load_workflow(workflow_path: str) -> Dict[str, Any]:
    """Load the workflow configuration from a JSON file."""
    try:
        with open(workflow_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error(f"Workflow file not found: {workflow_path}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON format in workflow file: {workflow_path}")
        raise

def execute_task(task: Dict[str, Any], input_data: str, api_key: str) -> str:
    """Execute a single task using the Claude API."""
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            "prompt": task["prompt_template"].format(input=input_data),
            "max_tokens": task.get("max_tokens", 100)
        }
        response = requests.post(API_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "")
    except requests.RequestException as e:
        logger.error(f"Error during API request: {e}")
        raise

def run_workflow(workflow: Dict[str, Any], input_path: str, api_key: str):
    """Run the entire workflow defined in the JSON configuration."""
    input_data = Path(input_path).read_text() if os.path.isfile(input_path) else ""
    for task in workflow.get("tasks", []):
        logger.info(f"Executing task: {task['name']}")
        input_data = execute_task(task, input_data, api_key)
        logger.info(f"Task '{task['name']}' completed. Output: {input_data[:100]}...")
    logger.info("Workflow execution completed.")

@app.command()
def main(workflow: str, input: str, api_key: str):
    """Run the Claude Task Orchestrator."""
    try:
        workflow_config = load_workflow(workflow)
        run_workflow(workflow_config, input, api_key)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
