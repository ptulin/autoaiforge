import pytest
from unittest.mock import patch, mock_open
from claude_subagent_orchestrator import Orchestrator, SubAgent, load_config
import json

def test_load_config_valid():
    mock_data = '[{"name": "Agent1", "role": "Assistant", "tasks": ["Task1", "Task2"]}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        subagents = load_config("mock_config.json")
        assert len(subagents) == 1
        assert subagents[0].name == "Agent1"
        assert subagents[0].role == "Assistant"
        assert subagents[0].tasks == ["Task1", "Task2"]

def test_load_config_invalid_json():
    mock_data = '{"name": "Agent1", "role": "Assistant", "tasks": ["Task1", "Task2"]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(json.JSONDecodeError):
            load_config("mock_config.json")

def test_execute_tasks():
    subagents = [
        SubAgent(name="Agent1", role="Assistant", tasks=["Task1"]),
        SubAgent(name="Agent2", role="Helper", tasks=["Task2"])
    ]
    orchestrator = Orchestrator(subagents)

    with patch.object(orchestrator, "communicate_with_subagent", return_value="Mocked Response") as mock_method:
        orchestrator.execute_tasks()

    assert len(orchestrator.task_log) == 2
    assert orchestrator.task_log[0]["response"] == "Mocked Response"
    assert orchestrator.task_log[1]["response"] == "Mocked Response"
