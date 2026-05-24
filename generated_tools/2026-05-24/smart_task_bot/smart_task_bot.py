import argparse
import json
import os
import requests
import openai
from typing import List, Dict, Any

def load_tasks(task_file: str) -> List[Dict[str, Any]]:
    """Load task sequence from a JSON file."""
    try:
        with open(task_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError(f"Task file '{task_file}' not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Task file '{task_file}' is not a valid JSON file.")

def execute_task(task: Dict[str, Any]) -> Any:
    """Execute a single task based on its type."""
    task_type = task.get("type")
    if task_type == "api_call":
        return execute_api_call(task)
    elif task_type == "ai_agent":
        return execute_ai_agent(task)
    elif task_type == "file_io":
        return execute_file_io(task)
    else:
        raise ValueError(f"Unsupported task type: {task_type}")

def execute_api_call(task: Dict[str, Any]) -> Any:
    """Execute an API call task."""
    try:
        response = requests.request(
            method=task.get("method", "GET"),
            url=task["url"],
            headers=task.get("headers"),
            json=task.get("payload")
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def execute_ai_agent(task: Dict[str, Any]) -> Any:
    """Execute an AI agent task using OpenAI API."""
    try:
        openai.api_key = task["api_key"]
        response = openai.Completion.create(
            model=task.get("model", "text-davinci-003"),
            prompt=task["prompt"],
            max_tokens=task.get("max_tokens", 100)
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        return {"error": str(e)}

def execute_file_io(task: Dict[str, Any]) -> Any:
    """Execute a file I/O task."""
    try:
        file_path = task["file_path"]
        if task["operation"] == "read":
            with open(file_path, 'r') as f:
                return f.read()
        elif task["operation"] == "write":
            with open(file_path, 'w') as f:
                f.write(task["content"])
                return f"Content written to {file_path}"
        else:
            raise ValueError("Unsupported file operation.")
    except Exception as e:
        return {"error": str(e)}

def execute_tasks(tasks: List[Dict[str, Any]], output_dir: str) -> None:
    """Execute a sequence of tasks and optionally save results."""
    results = []
    for i, task in enumerate(tasks):
        try:
            result = execute_task(task)
            results.append({"task": i + 1, "result": result})
        except Exception as e:
            results.append({"task": i + 1, "error": str(e)})

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {output_file}")
    else:
        print(json.dumps(results, indent=4))

def main():
    parser = argparse.ArgumentParser(description="Smart Task Automation Bot")
    parser.add_argument("--tasks", required=True, help="Path to the JSON file defining the task sequence.")
    parser.add_argument("--output-dir", help="Directory to save the task results.")
    args = parser.parse_args()

    try:
        tasks = load_tasks(args.tasks)
        execute_tasks(tasks, args.output_dir)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()