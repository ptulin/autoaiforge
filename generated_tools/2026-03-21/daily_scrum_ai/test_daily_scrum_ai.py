import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
from daily_scrum_ai import summarize_updates

@pytest.fixture
def mock_openai_response():
    return {
        'choices': [
            {
                'text': "Scrum Agenda:\n1. Task updates\n2. Blockers\n3. Developer summaries"
            }
        ]
    }

@patch('openai.Completion.create')
def test_summarize_updates_csv(mock_openai, mock_openai_response, tmp_path):
    mock_openai.return_value = mock_openai_response

    # Create a temporary CSV file
    csv_content = """task_id,developer,status,description,updated_at
1,Dev A,In Progress,Fixing bug in login,2023-10-01
2,Dev B,Completed,Implemented new feature,2023-10-02
"""
    csv_file = tmp_path / "updates.csv"
    csv_file.write_text(csv_content)

    result = summarize_updates(str(csv_file), "fake_api_key")
    assert "Scrum Agenda" in result
    assert "Task updates" in result

@patch('openai.Completion.create')
def test_summarize_updates_json(mock_openai, mock_openai_response, tmp_path):
    mock_openai.return_value = mock_openai_response

    # Create a temporary JSON file
    json_content = [
        {"task_id": 1, "developer": "Dev A", "status": "In Progress", "description": "Fixing bug in login", "updated_at": "2023-10-01"},
        {"task_id": 2, "developer": "Dev B", "status": "Completed", "description": "Implemented new feature", "updated_at": "2023-10-02"}
    ]
    json_file = tmp_path / "updates.json"
    json_file.write_text(json.dumps(json_content))

    result = summarize_updates(str(json_file), "fake_api_key")
    assert "Scrum Agenda" in result
    assert "Task updates" in result

@patch('openai.Completion.create')
def test_summarize_updates_invalid_file(mock_openai):
    result = summarize_updates("invalid_file.txt", "fake_api_key")
    assert "Unsupported file format" in result