import json
import yaml
from typing import Dict, Any
from pathlib import Path
from rich.console import Console
from rich.table import Table
import typer
from jsonschema import validate, ValidationError

app = typer.Typer()
console = Console()

def load_file(file_path: str) -> Dict[str, Any]:
    """Load a JSON or YAML file and return its contents as a dictionary."""
    path = Path(file_path)
    try:
        with open(path, 'r') as file:
            if path.suffix in ['.yaml', '.yml']:
                return yaml.safe_load(file)
            elif path.suffix == '.json':
                return json.load(file)
            else:
                raise ValueError("Unsupported file format. Use JSON or YAML.")
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        raise
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        console.print(f"[red]Error: Failed to parse file {file_path}: {e}[/red]")
        raise

def validate_agent_feedback(feedback: Dict[str, Any], schema: Dict[str, Any]):
    """Validate agent feedback against a given JSON schema."""
    try:
        validate(instance=feedback, schema=schema)
    except ValidationError as e:
        console.print(f"[red]Validation Error: {e.message}[/red]")
        raise

def evaluate_feedback(pr_template: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate the feedback based on the pull request template."""
    score = 0
    max_score = len(pr_template.get("issues", []))
    detailed_feedback = []

    for issue in pr_template.get("issues", []):
        issue_id = issue["id"]
        expected_feedback = issue["expected_feedback"]
        agent_response = feedback.get("feedback", {}).get(issue_id, "")

        if agent_response == expected_feedback:
            score += 1
            detailed_feedback.append({"issue_id": issue_id, "result": "correct"})
        else:
            detailed_feedback.append({"issue_id": issue_id, "result": "incorrect"})

    return {
        "score": score,
        "max_score": max_score,
        "details": detailed_feedback
    }

def display_results(results: Dict[str, Any]):
    """Display evaluation results in a formatted table."""
    table = Table(title="Evaluation Results")
    table.add_column("Issue ID", justify="center")
    table.add_column("Result", justify="center")

    for detail in results["details"]:
        table.add_row(str(detail["issue_id"]), detail["result"])

    console.print(table)
    console.print(f"[bold green]Total Score: {results['score']} / {results['max_score']}[/bold green]")

@app.command()
def main(pr_template: str = typer.Option(..., help="Path to the pull request template file (JSON or YAML)."),
         agent_feedback: str = typer.Option(..., help="Path to the agent feedback file (JSON)."),
         schema_file: str = typer.Option(..., help="Path to the JSON schema for validating agent feedback."),
         output_json: bool = typer.Option(False, help="Output results as JSON instead of a table.")):
    """Code Review Simulator: Evaluate AI agent feedback on pull requests."""
    try:
        pr_template_data = load_file(pr_template)
        agent_feedback_data = load_file(agent_feedback)
        schema_data = load_file(schema_file)

        validate_agent_feedback(agent_feedback_data, schema_data)
        results = evaluate_feedback(pr_template_data, agent_feedback_data)

        if output_json:
            console.print(json.dumps(results, indent=2))
        else:
            display_results(results)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    app()
