import argparse
import json
import yaml
import os
from jsonschema import validate, ValidationError
import openai

def load_workflow(file_path):
    """Load and validate the workflow configuration file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Workflow file '{file_path}' not found.")

    with open(file_path, 'r') as f:
        if str(file_path).endswith('.yaml') or str(file_path).endswith('.yml'):
            workflow = yaml.safe_load(f)
        elif str(file_path).endswith('.json'):
            workflow = json.load(f)
        else:
            raise ValueError("Unsupported file format. Use YAML or JSON.")

    schema = {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["task", "decision"]},
                        "prompt": {"type": "string"},
                        "options": {"type": "object"}
                    },
                    "required": ["name", "type", "prompt"]
                }
            }
        },
        "required": ["steps"]
    }

    try:
        validate(instance=workflow, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid workflow file: {e.message}")

    return workflow

def execute_workflow(workflow):
    """Execute the workflow step by step."""
    results = []
    for step in workflow['steps']:
        print(f"Executing step: {step['name']}")
        if step['type'] == 'task':
            result = call_claude(step['prompt'])
        elif step['type'] == 'decision':
            result = call_claude(step['prompt'], step.get('options', {}))
        else:
            raise ValueError(f"Unknown step type: {step['type']}")
        results.append({"step": step['name'], "result": result})
    return results

def call_claude(prompt, options=None):
    """Call Claude AI with a prompt and optional parameters."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=options.get('max_tokens', 100),
            temperature=options.get('temperature', 0.7)
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error calling Claude AI: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Workflow Builder")
    parser.add_argument('--workflow', required=True, help="Path to the YAML or JSON workflow file")
    args = parser.parse_args()

    try:
        workflow = load_workflow(args.workflow)
        results = execute_workflow(workflow)
        print("Workflow execution completed.")
        for result in results:
            print(f"Step: {result['step']}, Result: {result['result']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()