import pytest
import networkx as nx
from unittest.mock import patch
from context_graph_simulator import ContextGraphSimulator

def test_simulate_changes_positive():
    graph_data = {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"id": "decision_1", "outcome": "neutral"},
            {"id": "decision_2", "outcome": "neutral"}
        ],
        "links": [
            {"source": "decision_1", "target": "decision_2", "weight": 1.0}
        ]
    }
    sim = ContextGraphSimulator(graph_data)
    modified_graph, results = sim.simulate_changes("decision_1", "positive")

    assert modified_graph.nodes["decision_1"]["outcome"] == "positive"
    assert results["decision_2"] == 1.2

def test_simulate_changes_negative():
    graph_data = {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"id": "decision_1", "outcome": "neutral"},
            {"id": "decision_2", "outcome": "neutral"}
        ],
        "links": [
            {"source": "decision_1", "target": "decision_2", "weight": 1.0}
        ]
    }
    sim = ContextGraphSimulator(graph_data)
    modified_graph, results = sim.simulate_changes("decision_1", "negative")

    assert modified_graph.nodes["decision_1"]["outcome"] == "negative"
    assert results["decision_2"] == 0.8

def test_simulate_changes_invalid_node():
    graph_data = {
        "directed": False,
        "multigraph": False,
        "graph": {},
        "nodes": [
            {"id": "decision_1", "outcome": "neutral"}
        ],
        "links": []
    }
    sim = ContextGraphSimulator(graph_data)
    with pytest.raises(ValueError, match="Node 'decision_2' does not exist in the graph."):
        sim.simulate_changes("decision_2", "positive")