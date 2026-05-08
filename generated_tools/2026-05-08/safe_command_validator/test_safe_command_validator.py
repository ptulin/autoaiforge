import pytest
from unittest.mock import mock_open, patch
import json
from safe_command_validator import validate_command

def test_validate_command_whitelist():
    mock_rules = {
        "whitelist": ["^ls", "^echo"],
        "blacklist": []
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_rules))):
        assert validate_command("ls -la", "rules.json") is True
        assert validate_command("echo 'Hello'", "rules.json") is True
        assert validate_command("rm -rf /", "rules.json") is False

def test_validate_command_blacklist():
    mock_rules = {
        "whitelist": [],
        "blacklist": ["rm -rf", "shutdown"]
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_rules))):
        assert validate_command("rm -rf /", "rules.json") is False
        assert validate_command("shutdown now", "rules.json") is False
        assert validate_command("ls -la", "rules.json") is True

def test_validate_command_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert validate_command("ls -la", "nonexistent.json") is False

def test_validate_command_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid_json")):
        assert validate_command("ls -la", "rules.json") is False

def test_validate_command_unexpected_error():
    with patch("builtins.open", side_effect=Exception("Unexpected error")):
        assert validate_command("ls -la", "rules.json") is False