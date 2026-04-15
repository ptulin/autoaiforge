import pytest
from unittest.mock import patch, MagicMock
import json
import ai_task_flow

def test_load_workflow_yaml():
    yaml_content = """
    tasks:
      - name: task1
        dependencies: []
        ai_step:
          prompt: "What is the weather today?"
    """
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = yaml_content
        workflow = ai_task_flow.load_workflow("workflow.yaml")
        assert workflow['tasks'][0]['name'] == "task1"

def test_load_workflow_json():
    json_content = {
        "tasks": [
            {
                "name": "task1",
                "dependencies": [],
                "ai_step": {
                    "prompt": "What is the weather today?"
                }
            }
        ]
    }
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(json_content)
        workflow = ai_task_flow.load_workflow("workflow.json")
        assert workflow['tasks'][0]['name'] == "task1"

def test_execute_task():
    task = {
        "name": "task1",
        "ai_step": {
            "prompt": "What is the weather today?"
        }
    }
    mock_ai_model = MagicMock()
    mock_ai_model.create.return_value.choices = [MagicMock(message={'content': 'Sunny'})]

    output = ai_task_flow.execute_task(task, mock_ai_model)
    assert output == "Sunny"

def test_execute_workflow():
    workflow = {
        "tasks": [
            {
                "name": "task1",
                "dependencies": [],
                "ai_step": {
                    "prompt": "What is the weather today?"
                }
            },
            {
                "name": "task2",
                "dependencies": ["task1"],
                "ai_step": {
                    "prompt": "What is the temperature today?"
                }
            }
        ]
    }

    mock_ai_model = MagicMock()
    mock_ai_model.create.side_effect = [
        MagicMock(choices=[MagicMock(message={'content': 'Sunny'})]),
        MagicMock(choices=[MagicMock(message={'content': '25 degrees'})])
    ]

    with patch("ai_task_flow.ChatCompletion", return_value=mock_ai_model):
        ai_task_flow.execute_workflow(workflow, "fake_api_key")

    assert mock_ai_model.create.call_count == 2
    mock_ai_model.create.assert_any_call(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "What is the weather today?"}]
    )
    mock_ai_model.create.assert_any_call(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "What is the temperature today?"}]
    )
