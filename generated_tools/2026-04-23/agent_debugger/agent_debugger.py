import argparse
import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any

def load_config(config_path: str) -> Dict[str, Any]:
    """Load the agent configuration from a JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in configuration file: {config_path}")

def simulate_agent(config: Dict[str, Any]) -> nx.DiGraph:
    """Simulate the agent's task flow and return a directed graph."""
    graph = nx.DiGraph()

    tasks = config.get("tasks", [])
    if not tasks:
        raise ValueError("Configuration file must contain a 'tasks' key with a list of tasks.")

    for task in tasks:
        task_id = task.get("id")
        if not task_id:
            raise ValueError("Each task must have an 'id'.")
        graph.add_node(task_id, **task)

        for dependency in task.get("dependencies", []):
            graph.add_edge(dependency, task_id)

    return graph

def visualize_task_flow(graph: nx.DiGraph, output_path: str):
    """Generate a visual representation of the task flow graph."""
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, font_weight='bold')
    labels = nx.get_node_attributes(graph, 'name')
    nx.draw_networkx_labels(graph, pos, labels=labels)
    plt.title("Task Flow Graph")
    plt.savefig(output_path)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Agent Debugger: Simulate and visualize AI agent task flows.")
    parser.add_argument('--config', required=True, help="Path to the agent configuration JSON file.")
    parser.add_argument('--output', default="task_flow.png", help="Path to save the task flow graph image.")

    args = parser.parse_args()

    try:
        config = load_config(args.config)
        graph = simulate_agent(config)
        visualize_task_flow(graph, args.output)
        print(f"Task flow graph saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()