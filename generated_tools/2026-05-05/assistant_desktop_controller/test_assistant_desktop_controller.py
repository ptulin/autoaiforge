import pytest
from unittest.mock import patch, mock_open
from assistant_desktop_controller import parse_command, execute_task

@patch("assistant_desktop_controller.openai.Completion.create")
def test_parse_command(mock_openai):
    mock_openai.return_value.choices = [type("obj", (object,), {"text": "Create a file"})]
    result = parse_command("Create a file")
    assert result == "Create a file"

@patch("builtins.open", new_callable=mock_open)
def test_execute_task_create_file(mock_open):
    result = execute_task("Create file")
    mock_open.assert_called_once_with("example.txt", "w")
    assert result == "File 'example.txt' created successfully."

def test_execute_task_unrecognized():
    result = execute_task("Unknown command")
    assert result == "Command not recognized or not implemented."

@patch("assistant_desktop_controller.schedule.every")
def test_execute_task_schedule_task(mock_schedule):
    mock_schedule.return_value.do.return_value = None
    result = execute_task("Schedule task")
    mock_schedule.assert_called_once()
    assert result == "Task scheduled to run every minute."