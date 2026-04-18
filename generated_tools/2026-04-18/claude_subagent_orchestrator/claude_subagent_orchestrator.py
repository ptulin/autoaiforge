import json
import logging
from argparse import ArgumentParser
from typing import List, Dict
from pydantic import BaseModel, ValidationError
from rich.console import Console
from rich.table import Table
import openai

# Configure logging
logging.basicConfig(
    filename="subagent_communications.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

console = Console()

class SubAgent(BaseModel):
    name: str
    role: str
    tasks: List[str]

class Orchestrator:
    def __init__(self, subagents: List[SubAgent]):
        self.subagents = subagents
        self.task_log = []

    def execute_tasks(self):
        for subagent in self.subagents:
            console.print(f"[bold green]Executing tasks for subagent: {subagent.name}[/bold green]")
            for task in subagent.tasks:
                console.print(f"[yellow]Task: {task}[/yellow]")
                try:
                    response = self.communicate_with_subagent(subagent, task)
                    self.log_communication(subagent.name, task, response)
                except Exception as e:
                    console.print(f"[red]Error executing task '{task}' for subagent '{subagent.name}': {e}[/red]")

    def communicate_with_subagent(self, subagent: SubAgent, task: str) -> str:
        # Mocking OpenAI API call for simplicity
        # Replace this with actual OpenAI API call in production
        return f"Response from {subagent.name} for task '{task}'"

    def log_communication(self, subagent_name: str, task: str, response: str):
        log_entry = {
            "subagent": subagent_name,
            "task": task,
            "response": response
        }
        self.task_log.append(log_entry)
        logging.info(json.dumps(log_entry))

    def display_log(self):
        table = Table(title="Subagent Communication Log")
        table.add_column("Subagent", style="cyan")
        table.add_column("Task", style="magenta")
        table.add_column("Response", style="green")

        for entry in self.task_log:
            table.add_row(entry["subagent"], entry["task"], entry["response"])

        console.print(table)

def load_config(config_path: str) -> List[SubAgent]:
    try:
        with open(config_path, "r") as file:
            data = json.load(file)
            return [SubAgent(**agent) for agent in data]
    except FileNotFoundError:
        console.print(f"[red]Error: Config file '{config_path}' not found.[/red]")
        raise
    except json.JSONDecodeError:
        console.print(f"[red]Error: Config file '{config_path}' is not a valid JSON file.[/red]")
        raise
    except ValidationError as e:
        console.print(f"[red]Error: Invalid subagent configuration - {e}[/red]")
        raise

def main():
    parser = ArgumentParser(description="Claude Subagent Orchestrator")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the JSON configuration file defining subagents and their tasks."
    )
    args = parser.parse_args()

    try:
        subagents = load_config(args.config)
        orchestrator = Orchestrator(subagents)
        orchestrator.execute_tasks()
        orchestrator.display_log()
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")

if __name__ == "__main__":
    main()