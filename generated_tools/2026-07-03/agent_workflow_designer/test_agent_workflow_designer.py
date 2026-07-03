import pytest
from click.testing import CliRunner
from agent_workflow_designer import main
from unittest.mock import patch, MagicMock

def test_add_task():
    runner = CliRunner()
    with patch('agent_workflow_designer.click.prompt', side_effect=['add_task', 'Task1', 'quit']):
        result = runner.invoke(main, ['--output', 'test_output.json'])
        assert result.exit_code == 0
        assert "Task 'Task1' added." in result.output

def test_add_dependency():
    runner = CliRunner()
    with patch('agent_workflow_designer.click.prompt', side_effect=['add_task', 'Task1', 'add_task', 'Task2', 'add_dependency', 'Task1', 'Task2', 'quit']):
        result = runner.invoke(main, ['--output', 'test_output.json'])
        assert result.exit_code == 0
        assert "Dependency added: Task1 -> Task2" in result.output

def test_save_workflow():
    runner = CliRunner()
    with patch('agent_workflow_designer.click.prompt', side_effect=['add_task', 'Task1', 'save', 'quit']):
        with patch('builtins.open', new_callable=MagicMock):
            result = runner.invoke(main, ['--output', 'test_output.json'])
            assert result.exit_code == 0
            assert "Workflow saved to test_output.json as JSON." in result.output
