import argparse
import json
import yaml
import logging
from rich.console import Console
from rich.table import Table
import networkx as nx
from typing import Dict, Any

console = Console()

class ClaudeAgentOrchestrator:
    def __init__(self, workflow_file: str, log_file: str = None):
        self.workflow_file = workflow_file
        self.log_file = log_file
        self.graph = nx.DiGraph()
        self.tasks = {}

        if log_file:
            logging.basicConfig(filename=log_file, level=logging.INFO, 
                                format='%(asctime)s - %(levelname)s - %(message)s')

    def load_workflow(self):
        """Load the workflow configuration from a YAML or JSON file."""
        try:
            with open(self.workflow_file, 'r') as file:
                if self.workflow_file.endswith('.yaml') or self.workflow_file.endswith('.yml'):
                    data = yaml.safe_load(file)
                elif self.workflow_file.endswith('.json'):
                    data = json.load(file)
                else:
                    raise ValueError("Unsupported file format. Use YAML or JSON.")

            self.tasks = data.get('tasks', {})
            for task_name, task_info in self.tasks.items():
                self.graph.add_node(task_name, **task_info)
                for dependency in task_info.get('dependencies', []):
                    self.graph.add_edge(dependency, task_name)

            if not nx.is_directed_acyclic_graph(self.graph):
                raise ValueError("The workflow contains cyclic dependencies.")

        except Exception as e:
            console.print(f"[red]Error loading workflow: {e}")
            raise

    def display_workflow(self):
        """Display the workflow tasks and dependencies."""
        table = Table(title="Workflow Tasks")
        table.add_column("Task", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Dependencies", style="magenta")

        for task_name, task_info in self.tasks.items():
            dependencies = ", ".join(task_info.get('dependencies', []))
            table.add_row(task_name, task_info.get('status', 'pending'), dependencies)

        console.print(table)

    def execute_workflow(self):
        """Execute the tasks in the workflow based on dependencies."""
        try:
            for task in nx.topological_sort(self.graph):
                task_info = self.graph.nodes[task]
                console.print(f"[yellow]Executing task: {task}")
                logging.info(f"Executing task: {task}")

                # Simulate task execution
                task_info['status'] = 'completed'
                self.tasks[task]['status'] = 'completed'  # Update the tasks dictionary

                console.print(f"[green]Task {task} completed.")
                logging.info(f"Task {task} completed.")

        except Exception as e:
            console.print(f"[red]Error executing workflow: {e}")
            logging.error(f"Error executing workflow: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(description="Claude Agent Orchestrator")
    parser.add_argument('--workflow', required=True, help="Path to the workflow configuration file (YAML/JSON).")
    parser.add_argument('--log', help="Path to the log file.")
    args = parser.parse_args()

    orchestrator = ClaudeAgentOrchestrator(workflow_file=args.workflow, log_file=args.log)
    orchestrator.load_workflow()
    orchestrator.display_workflow()
    orchestrator.execute_workflow()

if __name__ == "__main__":
    main()