import pytest
from unittest.mock import patch
from agent_task_manager import AgentTaskManager, TaskDefinition

def test_add_task():
    manager = AgentTaskManager()
    task = manager.add_task(agent_id=1, task_name="fetch_data")
    assert task.agent_id == 1
    assert task.task_name == "fetch_data"
    assert task.dependencies == []

def test_get_task():
    manager = AgentTaskManager()
    manager.add_task(agent_id=1, task_name="fetch_data")
    task = manager.get_task("1_fetch_data")
    assert task is not None
    assert task.task_name == "fetch_data"

def test_execute_tasks():
    manager = AgentTaskManager()
    manager.add_task(agent_id=1, task_name="fetch_data")
    manager.add_task(agent_id=1, task_name="process_data", dependencies=["1_fetch_data"])

    with patch("agent_task_manager.execute_task.apply_async") as mock_execute:
        manager.execute_tasks()
        assert mock_execute.call_count == 2
        mock_execute.assert_any_call(("1_fetch_data", {"agent_id": 1, "task_name": "fetch_data", "dependencies": [], "priority": 1}))
        mock_execute.assert_any_call(("1_process_data", {"agent_id": 1, "task_name": "process_data", "dependencies": ["1_fetch_data"], "priority": 1}))
