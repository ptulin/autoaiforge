import pytest
import os
import json
from unittest.mock import patch, mock_open
from ai_agent_task_orchestrator import AIAgentTaskOrchestrator

@pytest.fixture
def mock_config_yaml():
    return """steps:
  - name: Step 1
    model: gpt-3.5-turbo
    prompt: "Summarize the following text."
  - name: Step 2
    model: gpt-3.5-turbo
    prompt: "Generate a Python function."
"""

@pytest.fixture
def mock_config_json():
    return json.dumps({
        "steps": [
            {"name": "Step 1", "model": "gpt-3.5-turbo", "prompt": "Summarize the following text."},
            {"name": "Step 2", "model": "gpt-3.5-turbo", "prompt": "Generate a Python function."}
        ]
    })

@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("ai_agent_task_orchestrator.ChatCompletion.create")
def test_execute_workflow_yaml(mock_chat_completion, mock_makedirs, mock_file, mock_config_yaml):
    mock_chat_completion.return_value = {"choices": [{"message": {"content": "Test output"}}]}
    mock_file.side_effect = [mock_open(read_data=mock_config_yaml).return_value, mock_open().return_value]

    orchestrator = AIAgentTaskOrchestrator("config.yaml", None, "output")
    orchestrator.load_config()
    orchestrator.execute_workflow()

    mock_chat_completion.assert_called()
    mock_makedirs.assert_called_with("output", exist_ok=True)
    mock_file.assert_any_call("config.yaml", "r")
    mock_file.assert_any_call(os.path.join("output", "results.json"), "w")

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"steps": []}))
@patch("os.makedirs")
def test_empty_workflow(mock_makedirs, mock_file):
    orchestrator = AIAgentTaskOrchestrator("config.json", None, "output")
    orchestrator.load_config()

    with pytest.raises(RuntimeError, match="Workflow configuration is not loaded or is invalid."):
        orchestrator.execute_workflow()

@patch("builtins.open", new_callable=mock_open, read_data="invalid_yaml")
def test_invalid_config(mock_file):
    orchestrator = AIAgentTaskOrchestrator("config.yaml", None, "output")

    with pytest.raises(RuntimeError, match="Failed to load configuration: .*"):
        orchestrator.load_config()
