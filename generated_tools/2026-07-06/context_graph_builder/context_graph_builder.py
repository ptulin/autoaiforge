import networkx as nx
import matplotlib.pyplot as plt

class ContextGraphBuilder:
    """
    A Python library for creating and managing context graphs that store AI agent decisions
    and their outcomes. This helps developers improve agent memory by enabling retrieval
    and analysis of past interactions.
    """

    def __init__(self):
        """Initialize an empty directed graph."""
        self.graph = nx.DiGraph()

    def add_decision(self, decision_id, attributes):
        """
        Add a decision node to the graph.

        :param decision_id: A unique identifier for the decision.
        :param attributes: A dictionary of attributes related to the decision.
        """
        if not isinstance(attributes, dict):
            raise ValueError("Attributes must be a dictionary.")

        self.graph.add_node(decision_id, **attributes)

    def add_outcome(self, decision_id, outcome_id, attributes):
        """
        Add an outcome node and connect it to a decision node.

        :param decision_id: The ID of the decision node.
        :param outcome_id: A unique identifier for the outcome.
        :param attributes: A dictionary of attributes related to the outcome.
        """
        if decision_id not in self.graph:
            raise ValueError(f"Decision node '{decision_id}' does not exist.")

        if not isinstance(attributes, dict):
            raise ValueError("Attributes must be a dictionary.")

        self.graph.add_node(outcome_id, **attributes)
        self.graph.add_edge(decision_id, outcome_id)

    def query_graph(self, node_id):
        """
        Retrieve the attributes of a node and its neighbors.

        :param node_id: The ID of the node to query.
        :return: A dictionary containing the node's attributes and its neighbors.
        """
        if node_id not in self.graph:
            raise ValueError(f"Node '{node_id}' does not exist in the graph.")

        node_data = {
            "attributes": self.graph.nodes[node_id],
            "neighbors": list(self.graph.neighbors(node_id))
        }
        return node_data

    def visualize_graph(self, output_file=None):
        """
        Visualize the graph using matplotlib.

        :param output_file: Optional file path to save the graph image.
        """
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={(u, v): f"" for u, v in self.graph.edges})

        if output_file:
            plt.savefig(output_file)
        else:
            plt.show()

if __name__ == "__main__":
    # Example usage
    cg = ContextGraphBuilder()
    cg.add_decision("decision_1", {"outcome": "positive"})
    cg.add_outcome("decision_1", "outcome_1", {"result": "success"})
    print(cg.query_graph("decision_1"))
    cg.visualize_graph()
