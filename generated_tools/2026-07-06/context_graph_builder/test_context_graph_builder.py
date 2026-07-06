import pytest
from unittest.mock import patch
from context_graph_builder import ContextGraphBuilder

def test_add_decision():
    cg = ContextGraphBuilder()
    cg.add_decision("decision_1", {"outcome": "positive"})
    assert "decision_1" in cg.graph.nodes
    assert cg.graph.nodes["decision_1"]["outcome"] == "positive"

def test_add_outcome():
    cg = ContextGraphBuilder()
    cg.add_decision("decision_1", {"outcome": "positive"})
    cg.add_outcome("decision_1", "outcome_1", {"result": "success"})
    assert "outcome_1" in cg.graph.nodes
    assert cg.graph.nodes["outcome_1"]["result"] == "success"
    assert ("decision_1", "outcome_1") in cg.graph.edges

def test_query_graph():
    cg = ContextGraphBuilder()
    cg.add_decision("decision_1", {"outcome": "positive"})
    cg.add_outcome("decision_1", "outcome_1", {"result": "success"})
    result = cg.query_graph("decision_1")
    assert result == {
        "attributes": {"outcome": "positive"},
        "neighbors": ["outcome_1"]
    }

def test_query_graph_invalid_node():
    cg = ContextGraphBuilder()
    with pytest.raises(ValueError, match="Node 'invalid_node' does not exist in the graph."):
        cg.query_graph("invalid_node")

@patch("matplotlib.pyplot.show")
def test_visualize_graph(mock_show):
    cg = ContextGraphBuilder()
    cg.add_decision("decision_1", {"outcome": "positive"})
    cg.add_outcome("decision_1", "outcome_1", {"result": "success"})
    cg.visualize_graph()
    mock_show.assert_called_once()
