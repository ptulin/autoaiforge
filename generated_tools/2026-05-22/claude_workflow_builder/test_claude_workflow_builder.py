import pytest
import json
import yaml
from unittest.mock import patch, MagicMock
from claude_workflow_builder import load_workflow, execute_workflow, call_claude

def test_load_workflow_valid_yaml(tmp_path):
    workflow_content = """
    steps:
      - name: Step 1
        type: task
        prompt: "What is the capital of France?"
    """
    file_path = tmp_path / "workflow.yaml"
    file_path.write_text(workflow_content)

    workflow = load_workflow(str(file_path))
    assert "steps" in workflow
    assert workflow["steps"][0]["name"] == "Step 1"

def test_load_workflow_invalid_schema(tmp_path):
    invalid_workflow_content = """
    steps:
      - name: Step 1
        prompt: "What is the capital of France?"
    """
    file_path = tmp_path / "workflow.yaml"
    file_path.write_text(invalid_workflow_content)

    with pytest.raises(ValueError, match="Invalid workflow file"):
        load_workflow(str(file_path))

@patch("claude_workflow_builder.call_claude")
def test_execute_workflow(mock_call_claude):
    mock_call_claude.return_value = "Paris"

    workflow = {
        "steps": [
            {"name": "Step 1", "type": "task", "prompt": "What is the capital of France?"}
        ]
    }

    results = execute_workflow(workflow)
    assert len(results) == 1
    assert results[0]["step"] == "Step 1"
    assert results[0]["result"] == "Paris"

@patch("openai.Completion.create")
def test_call_claude(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Paris")]
    mock_create.return_value = mock_response

    result = call_claude("What is the capital of France?", {"max_tokens": 10, "temperature": 0.5})
    assert result == "Paris"
    mock_create.assert_called_once_with(
        engine="text-davinci-003",
        prompt="What is the capital of France?",
        max_tokens=10,
        temperature=0.5
    )