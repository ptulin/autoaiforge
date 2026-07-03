import json
import yaml
import click
import networkx as nx
from networkx.drawing.nx_pydot import write_dot

@click.command()
@click.option('--output', '-o', required=True, type=click.Path(), help='Output file for the workflow blueprint (JSON or YAML).')
def main(output):
    """Agent Workflow Designer: Design modular workflows for AI agents."""
    click.echo("Welcome to the Agent Workflow Designer!")

    # Initialize an empty directed graph
    graph = nx.DiGraph()

    while True:
        click.echo("\nCurrent tasks in the workflow:")
        for node in graph.nodes:
            click.echo(f"- {node}")

        action = click.prompt("Choose an action: [add_task, add_dependency, remove_task, remove_dependency, save, quit]", type=str)

        if action == 'add_task':
            task_name = click.prompt("Enter the task name", type=str)
            if task_name in graph:
                click.echo("Task already exists!")
            else:
                graph.add_node(task_name)
                click.echo(f"Task '{task_name}' added.")

        elif action == 'add_dependency':
            task_from = click.prompt("Enter the source task (dependency)", type=str)
            task_to = click.prompt("Enter the target task (dependent)", type=str)
            if task_from in graph and task_to in graph:
                graph.add_edge(task_from, task_to)
                click.echo(f"Dependency added: {task_from} -> {task_to}")
            else:
                click.echo("One or both tasks do not exist.")

        elif action == 'remove_task':
            task_name = click.prompt("Enter the task name to remove", type=str)
            if task_name in graph:
                graph.remove_node(task_name)
                click.echo(f"Task '{task_name}' removed.")
            else:
                click.echo("Task does not exist.")

        elif action == 'remove_dependency':
            task_from = click.prompt("Enter the source task (dependency)", type=str)
            task_to = click.prompt("Enter the target task (dependent)", type=str)
            if graph.has_edge(task_from, task_to):
                graph.remove_edge(task_from, task_to)
                click.echo(f"Dependency removed: {task_from} -> {task_to}")
            else:
                click.echo("Dependency does not exist.")

        elif action == 'save':
            data = {
                'tasks': list(graph.nodes),
                'dependencies': list(graph.edges)
            }

            if output.endswith('.json'):
                with open(output, 'w') as f:
                    json.dump(data, f, indent=4)
                click.echo(f"Workflow saved to {output} as JSON.")

            elif output.endswith('.yaml') or output.endswith('.yml'):
                with open(output, 'w') as f:
                    yaml.dump(data, f)
                click.echo(f"Workflow saved to {output} as YAML.")

            else:
                click.echo("Unsupported file format. Please use .json or .yaml.")

        elif action == 'quit':
            click.echo("Exiting Agent Workflow Designer. Goodbye!")
            break

        else:
            click.echo("Invalid action. Please try again.")

if __name__ == '__main__':
    main()
