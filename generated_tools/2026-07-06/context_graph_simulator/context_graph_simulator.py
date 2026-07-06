import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class ContextGraphSimulator:
    def __init__(self, graph_data):
        """
        Initialize the ContextGraphSimulator with serialized graph data.

        :param graph_data: A dictionary representing the graph structure.
        """
        self.graph = nx.node_link_graph(graph_data)

    def simulate_changes(self, node, new_outcome):
        """
        Simulate the impact of changing a node's outcome.

        :param node: The node whose outcome is to be changed.
        :param new_outcome: The new outcome to assign to the node.
        :return: A tuple containing the modified graph and simulation results.
        """
        if node not in self.graph.nodes:
            raise ValueError(f"Node '{node}' does not exist in the graph.")

        # Update the node's outcome
        self.graph.nodes[node]['outcome'] = new_outcome

        # Simulate the impact of the change
        results = {}
        for neighbor in self.graph.neighbors(node):
            original_weight = self.graph[node][neighbor].get('weight', 1.0)
            self.graph[node][neighbor]['weight'] = self._calculate_new_weight(original_weight, new_outcome)
            results[neighbor] = self.graph[node][neighbor]['weight']

        return self.graph, results

    def _calculate_new_weight(self, original_weight, new_outcome):
        """
        Calculate a new weight for an edge based on the new outcome.

        :param original_weight: The original weight of the edge.
        :param new_outcome: The new outcome of the node.
        :return: The updated weight.
        """
        # Example logic: Adjust weight based on the new outcome
        if new_outcome == 'positive':
            return original_weight * 1.2
        elif new_outcome == 'neutral':
            return original_weight * 1.0
        elif new_outcome == 'negative':
            return original_weight * 0.8
        else:
            raise ValueError("Invalid outcome value. Must be 'positive', 'neutral', or 'negative'.")

    def visualize_graph(self):
        """
        Visualize the current state of the graph.
        """
        pos = nx.spring_layout(self.graph)
        edge_weights = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_weights)
        plt.show()

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Context Graph Simulator")
    parser.add_argument("--graph", type=str, required=True, help="Path to the serialized graph JSON file.")
    parser.add_argument("--node", type=str, required=True, help="Node to modify.")
    parser.add_argument("--outcome", type=str, required=True, choices=['positive', 'neutral', 'negative'], help="New outcome for the node.")
    parser.add_argument("--output", type=str, required=False, help="Path to save the modified graph JSON file.")

    args = parser.parse_args()

    # Load graph data
    try:
        with open(args.graph, 'r') as f:
            graph_data = json.load(f)
    except FileNotFoundError:
        print("Error: Graph file not found.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in graph file.")
        exit(1)

    # Initialize simulator
    sim = ContextGraphSimulator(graph_data)

    try:
        # Perform simulation
        modified_graph, results = sim.simulate_changes(args.node, args.outcome)
        print("Simulation Results:", results)

        # Save modified graph if output path is provided
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(nx.node_link_data(modified_graph), f)

        # Visualize the graph
        sim.visualize_graph()

    except Exception as e:
        print(f"Error: {e}")
        exit(1)
