import pytest
from unittest.mock import mock_open, patch, MagicMock
import ai_agent_policy_guard

def test_load_policy_yaml():
    mock_yaml = """rules:
    - pattern: "error"
      action: "log"
"""
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        logger = MagicMock()
        policy = ai_agent_policy_guard.load_policy("policy.yaml", logger)
        assert policy == {"rules": [{"pattern": "error", "action": "log"}]}

def test_load_policy_json():
    mock_json = '{"rules": [{"pattern": "error", "action": "log"}]}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        logger = MagicMock()
        policy = ai_agent_policy_guard.load_policy("policy.json", logger)
        assert policy == {"rules": [{"pattern": "error", "action": "log"}]}

def test_monitor_logs():
    policy = {"rules": [
        {"pattern": "error", "action": "log"},
        {"pattern": "critical", "action": "halt"}
    ]}
    log_lines = ["This is an error message", "This is a critical issue"]

    with patch("sys.exit") as mock_exit, \
         patch("ai_agent_policy_guard.logging.getLogger") as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        ai_agent_policy_guard.monitor_logs(policy, log_lines, mock_logger)

        mock_logger.warning.assert_called_once_with("Policy violation logged: This is an error message")
        mock_logger.critical.assert_called_once_with("Policy violation detected. Halting: This is a critical issue")
        mock_exit.assert_called_once_with(1)
