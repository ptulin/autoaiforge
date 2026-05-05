import json
import yaml
import os
from typing import Any, Dict, List
from jsonschema import validate, ValidationError
from rich.console import Console
from rich.table import Table
import typer

app = typer.Typer()
console = Console()

# Define the schema for validating the workflow configuration
WORKFLOW_SCHEMA = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "dependencies": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "action": {"type": "string"}
                },
                "required": ["id", "action"],
                "additionalProperties": False
            }
        }
    },
    "required": ["tasks"],
    "additionalProperties": False
}

def load_config(config_path: str) -> Dict[str, Any]:
    """Load and validate the workflow configuration from a YAML or JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as file:
        if config_path.endswith('.yaml') or config_path.endswith('.yml'):
            config = yaml.safe_load(file)
        elif config_path.endswith('.json'):
            config = json.load(file)
        else:
            raise ValueError("Unsupported file format. Use .yaml, .yml, or .json")

    try:
        validate(instance=config, schema=WORKFLOW_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Invalid configuration: {e.message}")

    return config

def execute_task(task: Dict[str, Any], results: Dict[str, Any]) -> Any:
    """Execute a single task and return its result."""
    console.log(f"Executing task: {task['id']} - {task.get('description', 'No description')}")
    # Simulate task execution (replace with custom logic as needed)
    result = f"Result of {task['id']}"
    console.log(f"Task {task['id']} completed with result: {result}")
    return result

def execute_workflow(config: Dict[str, Any]):
    """Execute the workflow defined in the configuration."""
    tasks = {task['id']: task for task in config['tasks']}
    results = {}
    completed_tasks = set()

    while len(completed_tasks) < len(tasks):
        for task_id, task in tasks.items():
            if task_id in completed_tasks:
                continue

            dependencies = task.get('dependencies', [])
            if all(dep in completed_tasks for dep in dependencies):
                results[task_id] = execute_task(task, results)
                completed_tasks.add(task_id)

    return results

@app.command()
def main(config: str, output: str = typer.Option(None, help="Path to save the execution results.")):
    """Agent Task Orchestrator: Execute a workflow defined in a YAML or JSON configuration file."""
    try:
        config_data = load_config(config)
        results = execute_workflow(config_data)

        if output:
            with open(output, 'w') as file:
                json.dump(results, file, indent=4)
            console.log(f"Results saved to {output}")
        else:
            console.log("Execution Results:")
            console.print(results)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    app()
