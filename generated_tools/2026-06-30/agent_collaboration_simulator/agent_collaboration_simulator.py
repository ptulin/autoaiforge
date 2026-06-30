import argparse
import json
import yaml
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any


def load_config(file_path: str) -> Dict[str, Any]:
    """Load the configuration from a JSON or YAML file."""
    try:
        with open(file_path, 'r') as file:
            if file_path.endswith('.json'):
                return json.load(file)
            elif file_path.endswith('.yml') or file_path.endswith('.yaml'):
                return yaml.safe_load(file)
            else:
                raise ValueError("Unsupported file format. Use JSON or YAML.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    except (json.JSONDecodeError, yaml.YAMLError):
        raise ValueError("Error parsing the configuration file.")


def simulate_agents(config: Dict[str, Any], visualize: bool):
    """Simulate agent collaboration based on the provided configuration."""
    agents = config.get("agents", [])
    tasks = config.get("tasks", [])
    communication = config.get("communication", [])

    if not agents or not tasks:
        raise ValueError("Configuration must include at least one agent and one task.")

    # Create a directed graph to represent agent interactions
    graph = nx.DiGraph()

    for agent in agents:
        graph.add_node(agent["name"], **agent)

    for comm in communication:
        graph.add_edge(comm["from"], comm["to"], **comm)

    # Simulate task assignments and interactions
    logs = []
    for task in tasks:
        assigned_agent = task.get("assigned_to")
        if assigned_agent not in graph.nodes:
            logs.append(f"Task '{task['name']}' could not be assigned. Agent '{assigned_agent}' not found.")
        else:
            logs.append(f"Task '{task['name']}' assigned to agent '{assigned_agent}'.")

    # Visualize the graph if requested
    if visualize:
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        edge_labels = nx.get_edge_attributes(graph, 'type')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        plt.title("Agent Collaboration Network")
        plt.show()

    return logs


def main():
    parser = argparse.ArgumentParser(description="Agent Collaboration Simulator")
    parser.add_argument("--config", required=True, help="Path to the configuration file (JSON or YAML).")
    parser.add_argument("--visualize", action="store_true", help="Visualize the agent collaboration network.")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        logs = simulate_agents(config, args.visualize)
        for log in logs:
            print(log)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()