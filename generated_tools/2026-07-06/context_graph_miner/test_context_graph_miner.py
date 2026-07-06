import pytest
import networkx as nx
from unittest.mock import patch, mock_open
import context_graph_miner
import json

def test_load_context_graph():
    graph_data = {
        "directed": True,
        "multigraph": False,
        "graph": {},
        "nodes": [{"id": "A"}, {"id": "B"}],
        "links": [{"source": "A", "target": "B"}]
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(graph_data))):
        graph = context_graph_miner.load_context_graph("dummy.json")
        assert isinstance(graph, nx.DiGraph)
        assert len(graph.nodes) == 2
        assert len(graph.edges) == 1

def test_query_graph():
    graph = nx.DiGraph()
    graph.add_node("A", attribute="decision_1")
    graph.add_node("B", attribute="decision_2")
    results = context_graph_miner.query_graph(graph, "decision_1")
    assert len(results) == 1
    assert results[0]["node"] == "A"

def test_generate_report_csv():
    graph = nx.DiGraph()
    graph.add_node("A", attribute="decision_1")
    graph.add_edge("A", "B", weight=1)
    with patch("pandas.DataFrame.to_csv") as mock_to_csv:
        message = context_graph_miner.generate_report(graph, "csv")
        assert "nodes_report.csv" in message
        assert "edges_report.csv" in message
        mock_to_csv.assert_called()

def test_generate_report_json():
    graph = nx.DiGraph()
    graph.add_node("A", attribute="decision_1")
    graph.add_edge("A", "B", weight=1)
    with patch("pandas.DataFrame.to_json") as mock_to_json:
        message = context_graph_miner.generate_report(graph, "json")
        assert "nodes_report.json" in message
        assert "edges_report.json" in message
        mock_to_json.assert_called()

def test_load_context_graph_file_not_found():
    with pytest.raises(ValueError, match="Failed to load graph"):
        context_graph_miner.load_context_graph("nonexistent.json")

def test_load_context_graph_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid_json")):
        with pytest.raises(ValueError, match="Failed to load graph"):
            context_graph_miner.load_context_graph("dummy.json")
