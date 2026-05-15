import pytest
from unittest.mock import patch, mock_open
import ai_task_scheduler
import yaml

def test_load_config():
    mock_yaml = """
    api_key: test_key
    tasks:
      task1:
        prompt: "Generate a report"
        output_file: "output.txt"
        schedule_type: "interval"
        interval: 10
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        config = ai_task_scheduler.load_config("test.yaml")
        assert config['api_key'] == 'test_key'
        assert 'task1' in config['tasks']
        assert config['tasks']['task1']['prompt'] == "Generate a report"

def test_execute_task():
    task_config = {
        'prompt': "Generate a report",
        'output_file': "output.txt",
        'engine': "text-davinci-003",
        'max_tokens': 50
    }
    with patch("openai.Completion.create") as mock_openai, \
         patch("builtins.open", mock_open()) as mock_file:
        mock_openai.return_value = {'choices': [{'text': 'Generated content'}]}
        ai_task_scheduler.execute_task("task1", task_config)
        mock_openai.assert_called_once()
        mock_file.assert_called_once_with("output.txt", 'w')
        mock_file().write.assert_called_once_with("Generated content")

def test_schedule_tasks():
    mock_config = {
        'tasks': {
            'task1': {
                'prompt': "Generate a report",
                'output_file': "output.txt",
                'schedule_type': "interval",
                'interval': 10
            }
        }
    }
    with patch("schedule.every") as mock_schedule:
        mock_interval = mock_schedule.return_value
        ai_task_scheduler.schedule_tasks(mock_config)
        mock_schedule.assert_called_once_with(10)
        mock_interval.seconds.do.assert_called_once()
