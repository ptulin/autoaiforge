import pytest
import json
from unittest.mock import patch, mock_open, Mock
from ai_desktop_health_monitor import monitor_system

def test_monitor_system_high_cpu():
    """Test monitor_system with high CPU usage."""
    mock_claude_action_file = json.dumps({"prompt": "What should I do?"})

    with patch("builtins.open", mock_open(read_data=mock_claude_action_file)):
        with patch("psutil.cpu_percent", return_value=90):
            with patch("ai_desktop_health_monitor.Mock") as mock_anthropic:
                mock_anthropic.return_value.completions.create.return_value = {"completion": "Close unresponsive apps."}
                with patch("time.sleep", side_effect=KeyboardInterrupt):
                    monitor_system(80, "mock_actions.json", 1)


def test_monitor_system_low_cpu():
    """Test monitor_system with low CPU usage."""
    mock_claude_action_file = json.dumps({"prompt": "What should I do?"})

    with patch("builtins.open", mock_open(read_data=mock_claude_action_file)):
        with patch("psutil.cpu_percent", return_value=50):
            with patch("ai_desktop_health_monitor.Mock") as mock_anthropic:
                with patch("time.sleep", side_effect=KeyboardInterrupt):
                    monitor_system(80, "mock_actions.json", 1)
                    mock_anthropic.return_value.completions.create.assert_not_called()


def test_monitor_system_invalid_file():
    """Test monitor_system with invalid JSON file."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("psutil.cpu_percent", return_value=90):
            with patch("time.sleep", side_effect=KeyboardInterrupt):
                monitor_system(80, "mock_actions.json", 1)


def test_monitor_system_file_not_found():
    """Test monitor_system with missing file."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("time.sleep", side_effect=KeyboardInterrupt):
            monitor_system(80, "mock_actions.json", 1)
