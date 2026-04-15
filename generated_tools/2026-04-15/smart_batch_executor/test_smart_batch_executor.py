import pytest
from unittest.mock import patch, mock_open
import json
from smart_batch_executor import load_tasks, optimize_task_order, execute_task, execute_tasks

def test_load_tasks():
    mock_data = '{"tasks": [{"name": "task1"}], "dependencies": {}}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = load_tasks("mock_config.json")
        assert "tasks" in result
        assert len(result["tasks"]) == 1
        assert result["tasks"][0]["name"] == "task1"

def test_optimize_task_order():
    tasks = [{"name": "task1"}, {"name": "task2"}]
    dependencies = {}
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = type("obj", (object,), {"choices": [type("obj", (object,), {"text": json.dumps(tasks)})]})
        result = optimize_task_order(tasks, dependencies)
        assert len(result) == 2
        assert result[0]["name"] == "task1"

def test_execute_task():
    task = {"name": "task1"}
    result = execute_task(task)
    assert result["task"] == "task1"
    assert result["status"] == "success"

def test_execute_tasks():
    tasks = [{"name": "task1"}, {"name": "task2"}]
    dependencies = {}
    with patch("smart_batch_executor.execute_task", side_effect=[
        {"task": "task1", "status": "success", "output": "Output of task1"},
        {"task": "task2", "status": "failed", "error": "Simulated error"}
    ]):
        results = execute_tasks(tasks, dependencies)
        assert len(results) == 2
        assert results[0]["status"] == "success"
        assert results[1]["status"] == "failed"