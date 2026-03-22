import yaml
import json
import click
import openai
from typing import Any, Dict, List

class WorkflowAgentBuilder:
    def __init__(self, model: str = "text-davinci-003", api_key: str = None):
        self.model = model
        if api_key:
            openai.api_key = api_key

    def execute_task(self, task: Dict[str, Any]) -> Any:
        """Executes a single task using the AI model."""
        prompt = task.get("prompt", "")
        if not prompt:
            raise ValueError("Task is missing a 'prompt' field.")

        try:
            response = openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=task.get("max_tokens", 100),
                temperature=task.get("temperature", 0.7)
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error executing task: {str(e)}"

    def execute_workflow(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Executes a workflow defined in a YAML file."""
        results = []
        tasks = workflow.get("tasks", [])

        for task in tasks:
            if "condition" in task:
                condition_result = self.execute_task({"prompt": task["condition"]})
                if condition_result.lower() != "true":
                    continue

            result = self.execute_task(task)
            results.append({"task": task.get("name", "Unnamed Task"), "result": result})

        return results

@click.command()
@click.option('--workflow', type=click.Path(exists=True), required=True, help="Path to the YAML workflow file.")
@click.option('--output', type=click.Path(), required=False, help="Path to save the JSON output.")
@click.option('--api-key', type=str, required=True, help="API key for the AI model.")
def main(workflow, output, api_key):
    """CLI entry point for the Workflow Agent Builder tool."""
    try:
        with open(workflow, 'r') as file:
            workflow_data = yaml.safe_load(file)

        builder = WorkflowAgentBuilder(api_key=api_key)
        results = builder.execute_workflow(workflow_data)

        if output:
            with open(output, 'w') as outfile:
                json.dump(results, outfile, indent=4)
        else:
            click.echo(json.dumps(results, indent=4))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    main()
