import pytest
from unittest.mock import patch, mock_open
import json
import yaml
from agent_collaboration_simulator import load_config, simulate_agents


def test_load_config_json():
    mock_json = '{"agents": [{"name": "Agent1"}], "tasks": []}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        config = load_config("config.json")
        assert config["agents"] == [{"name": "Agent1"}]
        assert config["tasks"] == []


def test_load_config_yaml():
    mock_yaml = """agents:
  - name: Agent1
tasks: []"""
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        config = load_config("config.yml")
        assert config["agents"] == [{"name": "Agent1"}]
        assert config["tasks"] == []


def test_simulate_agents():
    config = {
        "agents": [{"name": "Agent1"}, {"name": "Agent2"}],
        "tasks": [{"name": "Task1", "assigned_to": "Agent1"}],
        "communication": [{"from": "Agent1", "to": "Agent2", "type": "message"}]
    }
    with patch("matplotlib.pyplot.show"):
        logs = simulate_agents(config, visualize=True)
        assert "Task 'Task1' assigned to agent 'Agent1'." in logs


def test_simulate_agents_missing_agent():
    config = {
        "agents": [{"name": "Agent1"}],
        "tasks": [{"name": "Task1", "assigned_to": "Agent2"}],
        "communication": []
    }
    logs = simulate_agents(config, visualize=False)
    assert "Task 'Task1' could not be assigned. Agent 'Agent2' not found." in logs