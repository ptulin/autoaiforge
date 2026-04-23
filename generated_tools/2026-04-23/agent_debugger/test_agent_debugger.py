import pytest
import json
import networkx as nx
from unittest.mock import patch, mock_open
from agent_debugger import load_config, simulate_agent, visualize_task_flow

def test_load_config_valid():
    mock_data = '{"tasks": [{"id": "task1", "name": "Task 1", "dependencies": []}]}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        config = load_config("dummy_path.json")
        assert config["tasks"][0]["id"] == "task1"

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_file.json")

def test_load_config_invalid_json():
    mock_data = '{invalid_json}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(ValueError):
            load_config("dummy_path.json")

def test_simulate_agent_valid():
    config = {
        "tasks": [
            {"id": "task1", "name": "Task 1", "dependencies": []},
            {"id": "task2", "name": "Task 2", "dependencies": ["task1"]}
        ]
    }
    graph = simulate_agent(config)
    assert isinstance(graph, nx.DiGraph)
    assert set(graph.nodes) == {"task1", "task2"}
    assert list(graph.edges) == [("task1", "task2")]

def test_simulate_agent_missing_tasks():
    config = {}
    with pytest.raises(ValueError):
        simulate_agent(config)

def test_visualize_task_flow():
    graph = nx.DiGraph()
    graph.add_node("task1", name="Task 1")
    graph.add_node("task2", name="Task 2")
    graph.add_edge("task1", "task2")

    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        visualize_task_flow(graph, "output.png")
        mock_savefig.assert_called_once_with("output.png")