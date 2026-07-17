import pytest
import os
import subprocess
import signal
from unittest.mock import patch, MagicMock
from agent_manager import start_agent, stop_agent, monitor_resources, validate_config

def test_start_agent_valid_config(tmp_path):
    config_path = tmp_path / "valid_config.yaml"
    config_path.write_text("""command: echo 'Agent started'""")

    with patch("subprocess.Popen") as mock_popen:
        mock_popen.return_value.pid = 12345
        pid = start_agent(str(config_path))
        assert pid == 12345
        mock_popen.assert_called_once()

def test_start_agent_missing_file():
    with pytest.raises(FileNotFoundError):
        start_agent("non_existent_config.yaml")

def test_start_agent_invalid_config(tmp_path):
    config_path = tmp_path / "invalid_config.yaml"
    config_path.write_text("""invalid_field: value""")

    with pytest.raises(ValueError):
        start_agent(str(config_path))

def test_stop_agent():
    with patch("os.killpg") as mock_killpg, patch("os.getpgid", return_value=12345):
        stop_agent(12345)
        mock_killpg.assert_called_once_with(12345, signal.SIGTERM)

def test_monitor_resources():
    with patch("psutil.Process") as mock_process:
        mock_instance = MagicMock()
        mock_instance.cpu_percent.return_value = 10.0
        mock_instance.memory_info.return_value.rss = 1048576
        mock_process.return_value = mock_instance

        monitor_resources(12345)
        mock_process.assert_called_once_with(12345)
        mock_instance.cpu_percent.assert_called_once_with(interval=1.0)
        mock_instance.memory_info.assert_called_once()

def test_validate_config_valid(tmp_path):
    config_path = tmp_path / "valid_config.yaml"
    config_path.write_text("""command: echo 'Agent started'""")

    validate_config(str(config_path))

def test_validate_config_invalid_yaml(tmp_path):
    config_path = tmp_path / "invalid_config.yaml"
    config_path.write_text("""command: [""")

    with pytest.raises(ValueError):
        validate_config(str(config_path))

def test_validate_config_missing_file():
    with pytest.raises(FileNotFoundError):
        validate_config("non_existent_config.yaml")
