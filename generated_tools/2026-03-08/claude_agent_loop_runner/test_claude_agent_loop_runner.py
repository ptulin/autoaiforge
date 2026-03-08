import pytest
from unittest.mock import MagicMock, patch
from claude_agent_loop_runner import load_workflow, execute_workflow

def test_load_workflow_json():
    """Test loading a JSON workflow."""
    mock_json = '{"steps": [{"name": "Step 1", "prompt": "Hello Claude!"}]}'
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = mock_json
        workflow = load_workflow("workflow.json")
        assert workflow["steps"][0]["name"] == "Step 1"

def test_load_workflow_yaml():
    """Test loading a YAML workflow."""
    mock_yaml = """steps:
  - name: Step 1
    prompt: Hello Claude!"""
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = mock_yaml
        workflow = load_workflow("workflow.yaml")
        assert workflow["steps"][0]["name"] == "Step 1"

def test_execute_workflow():
    """Test executing a workflow."""
    workflow = {
        "steps": [
            {"name": "Step 1", "prompt": "Hello Claude!", "max_tokens": 50}
        ]
    }
    mock_client = MagicMock()
    mock_client.completions.create.return_value = {"completion": "Hi there!"}

    execute_workflow(workflow, mock_client, max_iterations=1)
    mock_client.completions.create.assert_called_once_with(
        model="claude-v1",
        prompt="Hello Claude!",
        max_tokens_to_sample=50
    )

@pytest.mark.parametrize("workflow, max_iterations, expected_calls", [
    ({"steps": []}, 5, 0),
    ({"steps": [{"name": "Step 1", "prompt": "Hello Claude!", "max_tokens": 50}]}, 0, 0),
    ({"steps": [{"name": "Step 1", "prompt": "Hello Claude!", "max_tokens": 50}]}, 1, 1),
])
def test_execute_workflow_edge_cases(workflow, max_iterations, expected_calls):
    """Test edge cases for execute_workflow."""
    mock_client = MagicMock()
    mock_client.completions.create.return_value = {"completion": "Hi there!"}

    execute_workflow(workflow, mock_client, max_iterations=max_iterations)
    assert mock_client.completions.create.call_count == expected_calls
