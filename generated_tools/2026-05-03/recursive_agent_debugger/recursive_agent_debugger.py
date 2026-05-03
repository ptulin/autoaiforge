import argparse
import importlib.util
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich import print

console = Console()

def load_agent_class(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    spec = importlib.util.spec_from_file_location("agent_module", file_path)
    agent_module = importlib.util.module_from_spec(spec)
    sys.modules["agent_module"] = agent_module
    spec.loader.exec_module(agent_module)

    if not hasattr(agent_module, "Agent"):
        raise AttributeError("The provided file does not define an 'Agent' class.")

    return agent_module.Agent

def visualize_decision_tree(tree, output_file="decision_tree.png"):
    pos = nx.spring_layout(tree)
    plt.figure(figsize=(12, 8))
    nx.draw(tree, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.savefig(output_file)
    plt.close()
    console.print(f"[green]Decision tree visualization saved to {output_file}[/green]")

def debug_agent(agent_class, steps):
    agent = agent_class()
    decision_tree = nx.DiGraph()
    performance_metrics = []

    prev_state = None
    for step in range(steps):
        console.print(f"[bold blue]Step {step + 1}[/bold blue]")
        state = agent.get_state()
        decision = agent.make_decision()
        improvement = agent.improve_logic()

        decision_tree.add_node(f"Step {step + 1}: {state}")
        if step > 0:
            decision_tree.add_edge(f"Step {step}: {prev_state}", f"Step {step + 1}: {state}")

        performance_metrics.append((step + 1, state, decision, improvement))
        prev_state = state

    return decision_tree, performance_metrics

def display_metrics(metrics):
    table = Table(title="Performance Metrics")
    table.add_column("Step", justify="right", style="cyan")
    table.add_column("State", style="magenta")
    table.add_column("Decision", style="green")
    table.add_column("Improvement", style="yellow")

    for step, state, decision, improvement in metrics:
        table.add_row(str(step), str(state), str(decision), str(improvement))

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Recursive Agent Debugger")
    parser.add_argument("--agent_file", required=True, help="Path to the Python file containing the Agent class.")
    parser.add_argument("--steps", type=int, default=10, help="Number of recursive iterations to debug.")
    args = parser.parse_args()

    try:
        agent_class = load_agent_class(args.agent_file)
        decision_tree, metrics = debug_agent(agent_class, args.steps)
        visualize_decision_tree(decision_tree)
        display_metrics(metrics)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    main()