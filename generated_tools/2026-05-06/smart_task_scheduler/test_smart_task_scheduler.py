import pytest
from unittest.mock import patch, MagicMock
from smart_task_scheduler import TaskScheduler
import json

@pytest.fixture
def sample_config_json(tmp_path):
    config_data = {
        "tasks": [
            {
                "name": "Test API Task",
                "type": "api_request",
                "method": "GET",
                "url": "https://example.com/api",
                "trigger": {"cron": "12:00"}
            },
            {
                "name": "Test Script Task",
                "type": "custom_script",
                "script": "print('Hello, World!')",
                "trigger": {"cron": "13:00"}
            }
        ]
    }
    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    return config_path

@patch('smart_task_scheduler.requests.request')
def test_execute_api_task(mock_request, sample_config_json):
    mock_request.return_value = MagicMock(status_code=200, text="Success")
    scheduler = TaskScheduler(sample_config_json)
    api_task = scheduler.tasks[0]
    scheduler.execute_task(api_task)
    mock_request.assert_called_once_with(method="GET", url="https://example.com/api", headers={}, json={})

def test_execute_custom_script_task(sample_config_json):
    scheduler = TaskScheduler(sample_config_json)
    script_task = scheduler.tasks[1]
    with patch("builtins.print") as mock_print:
        scheduler.execute_task(script_task)
        mock_print.assert_called_once_with("Hello, World!")

@patch("schedule.every")
def test_schedule_tasks(mock_schedule, sample_config_json):
    mock_job = MagicMock()
    mock_schedule.return_value = mock_job
    scheduler = TaskScheduler(sample_config_json)
    scheduler.schedule_tasks()
    assert mock_schedule.call_count == 2
    mock_schedule().day.at.assert_any_call("12:00")
    mock_schedule().day.at.assert_any_call("13:00")