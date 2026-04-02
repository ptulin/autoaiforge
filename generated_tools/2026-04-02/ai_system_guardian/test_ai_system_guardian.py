import pytest
import json
import os
from unittest.mock import patch, MagicMock, mock_open
from ai_system_guardian import ConfigLoader, CommandExecutor, TaskHandler

def test_config_loader():
    config_data = {"tasks": [{"command": "echo Hello"}], "allowed_commands": ["echo Hello"]}
    with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
        with patch("os.path.exists", return_value=True):
            loader = ConfigLoader("test_config.json")
            config = loader.load_config()
            assert config == config_data

def test_command_executor():
    logger = MagicMock()
    executor = CommandExecutor(["echo Hello"], logger)

    # Test allowed command
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="Hello", returncode=0)
        result = executor.execute("echo Hello")
        assert result == "Hello"
        logger.info.assert_called_once()

    # Test blocked command
    result = executor.execute("rm -rf /")
    assert "not allowed" in result
    logger.warning.assert_called_once()

def test_task_handler():
    config_data = {"tasks": [{"command": "echo Hello"}], "allowed_commands": ["echo Hello"]}
    config_loader = MagicMock()
    config_loader.config = config_data
    logger = MagicMock()
    executor = CommandExecutor(["echo Hello"], logger)
    task_handler = TaskHandler(config_loader, executor)

    with patch.object(executor, "execute", return_value="Hello") as mock_execute:
        task_handler.handle_tasks()
        mock_execute.assert_called_once_with("echo Hello")