import pytest
import yaml
import json
from unittest.mock import patch, MagicMock
from workflow_agent_builder import WorkflowAgentBuilder

@pytest.fixture
def mock_openai():
    with patch("openai.Completion.create") as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(text="true")])
        yield mock_create

def test_execute_task(mock_openai):
    builder = WorkflowAgentBuilder(api_key="test_key")
    task = {"prompt": "What is 2+2?", "max_tokens": 10}
    result = builder.execute_task(task)
    assert result == "true"
    mock_openai.assert_called_once()

def test_execute_workflow(mock_openai):
    builder = WorkflowAgentBuilder(api_key="test_key")
    workflow = {
        "tasks": [
            {"name": "Task 1", "prompt": "What is 2+2?"},
            {"name": "Task 2", "prompt": "What is the capital of France?"}
        ]
    }
    results = builder.execute_workflow(workflow)
    assert len(results) == 2
    assert results[0]["task"] == "Task 1"
    assert results[1]["task"] == "Task 2"

def test_execute_workflow_with_condition(mock_openai):
    builder = WorkflowAgentBuilder(api_key="test_key")
    workflow = {
        "tasks": [
            {"name": "Conditional Task", "prompt": "What is 2+2?", "condition": "Is this a test?"}
        ]
    }
    results = builder.execute_workflow(workflow)
    assert len(results) == 1
    assert results[0]["task"] == "Conditional Task"
