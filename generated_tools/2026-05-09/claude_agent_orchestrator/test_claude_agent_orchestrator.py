import pytest
import json
import yaml
from unittest.mock import patch, mock_open
from claude_agent_orchestrator import ClaudeAgentOrchestrator

def test_load_workflow_json():
    mock_data = json.dumps({
        "tasks": {
            "task1": {"status": "pending", "dependencies": []},
            "task2": {"status": "pending", "dependencies": ["task1"]}
        }
    })

    with patch("builtins.open", mock_open(read_data=mock_data)):
        orchestrator = ClaudeAgentOrchestrator(workflow_file="workflow.json")
        orchestrator.load_workflow()
        assert len(orchestrator.tasks) == 2
        assert orchestrator.graph.has_edge("task1", "task2")

def test_load_workflow_yaml():
    mock_data = yaml.dump({
        "tasks": {
            "task1": {"status": "pending", "dependencies": []},
            "task2": {"status": "pending", "dependencies": ["task1"]}
        }
    })

    with patch("builtins.open", mock_open(read_data=mock_data)):
        orchestrator = ClaudeAgentOrchestrator(workflow_file="workflow.yaml")
        orchestrator.load_workflow()
        assert len(orchestrator.tasks) == 2
        assert orchestrator.graph.has_edge("task1", "task2")

def test_execute_workflow():
    mock_data = json.dumps({
        "tasks": {
            "task1": {"status": "pending", "dependencies": []},
            "task2": {"status": "pending", "dependencies": ["task1"]}
        }
    })

    with patch("builtins.open", mock_open(read_data=mock_data)):
        orchestrator = ClaudeAgentOrchestrator(workflow_file="workflow.json")
        orchestrator.load_workflow()
        orchestrator.execute_workflow()

        assert orchestrator.tasks["task1"]["status"] == "completed"
        assert orchestrator.tasks["task2"]["status"] == "completed"

def test_cyclic_workflow():
    mock_data = json.dumps({
        "tasks": {
            "task1": {"status": "pending", "dependencies": ["task2"]},
            "task2": {"status": "pending", "dependencies": ["task1"]}
        }
    })

    with patch("builtins.open", mock_open(read_data=mock_data)):
        orchestrator = ClaudeAgentOrchestrator(workflow_file="workflow.json")
        with pytest.raises(ValueError, match="The workflow contains cyclic dependencies."):
            orchestrator.load_workflow()

def test_invalid_file_format():
    with patch("builtins.open", mock_open(read_data="invalid data")):
        orchestrator = ClaudeAgentOrchestrator(workflow_file="workflow.txt")
        with pytest.raises(ValueError, match="Unsupported file format. Use YAML or JSON."):
            orchestrator.load_workflow()