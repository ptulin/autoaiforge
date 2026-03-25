import os
import json
import time
import requests
import click
from rich.console import Console
from rich.progress import Progress

console = Console()

API_BASE_URL = "https://api.claude.ai/workflows"

def trigger_workflow(workflow_name, input_payload, retries, delay):
    """Trigger a workflow and optionally retry on failure."""
    url = f"{API_BASE_URL}/{workflow_name}/trigger"
    headers = {"Content-Type": "application/json"}

    for attempt in range(retries + 1):
        try:
            response = requests.post(url, headers=headers, json=input_payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            console.print(f"[red]Attempt {attempt + 1} failed: {e}[/red]")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise

def monitor_workflow(workflow_id):
    """Monitor the status of a triggered workflow."""
    url = f"{API_BASE_URL}/{workflow_id}/status"
    headers = {"Content-Type": "application/json"}

    with Progress() as progress:
        task = progress.add_task("[cyan]Monitoring workflow...", total=None)

        while not progress.finished:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                status_data = response.json()
                status = status_data.get("status")

                if status == "completed":
                    progress.update(task, completed=100)
                    progress.stop()
                    return status_data
                elif status == "failed":
                    progress.stop()
                    raise Exception("Workflow execution failed.")

                time.sleep(2)
            except requests.RequestException as e:
                progress.stop()
                raise Exception(f"Error monitoring workflow: {e}")

@click.command()
@click.option('--workflow', required=True, help='Name of the workflow to trigger.')
@click.option('--input', 'input_file', required=True, type=click.Path(exists=True), help='Path to the JSON input file.')
@click.option('--retries', default=3, show_default=True, help='Number of retries on failure.')
@click.option('--delay', default=5, show_default=True, help='Delay between retries in seconds.')
def main(workflow, input_file, retries, delay):
    """CLI tool to trigger and monitor Claude AI workflows."""
    try:
        with open(input_file, 'r') as f:
            input_payload = json.load(f)

        console.print(f"[green]Triggering workflow '{workflow}' with input from {input_file}...[/green]")
        response = trigger_workflow(workflow, input_payload, retries, delay)
        workflow_id = response.get("workflow_id")

        if not workflow_id:
            console.print("[red]Failed to retrieve workflow ID from response.[/red]")
            return

        console.print(f"[green]Workflow triggered successfully. ID: {workflow_id}[/green]")
        console.print("[green]Monitoring workflow execution...[/green]")
        result = monitor_workflow(workflow_id)

        console.print("[green]Workflow completed successfully![/green]")
        console.print(json.dumps(result, indent=2))

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()