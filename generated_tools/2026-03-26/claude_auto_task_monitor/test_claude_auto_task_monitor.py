import pytest
import json
from unittest.mock import patch, mock_open
from claude_auto_task_monitor import load_tasks_from_json, monitor_tasks

def test_load_tasks_from_json_valid():
    mock_data = '[{"id": "1", "progress": 0}]'
    with patch('builtins.open', mock_open(read_data=mock_data)):
        tasks = load_tasks_from_json('tasks.json')
        assert len(tasks) == 1
        assert tasks[0]['id'] == '1'

def test_load_tasks_from_json_file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError):
        tasks = load_tasks_from_json('missing.json')
        assert tasks == []

def test_monitor_tasks():
    tasks = [{"id": "1", "progress": 0, "status": ""}]
    monitor_tasks(tasks)
    assert tasks[0]['progress'] == 100
    assert tasks[0]['status'] == 'completed'