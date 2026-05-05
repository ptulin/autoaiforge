import pytest
import json
from unittest.mock import patch, mock_open
from agent_task_orchestrator import load_config, execute_workflow

VALID_CONFIG = {
    "tasks": [
        {"id": "task1", "action": "action1"},
        {"id": "task2", "action": "action2", "dependencies": ["task1"]}
    ]
}

INVALID_CONFIG = {
    "tasks": [
        {"id": "task1"}  # Missing required "action" key
    ]
}

@pytest.fixture
def mock_config_file():
    return mock_open(read_data=json.dumps(VALID_CONFIG))

@pytest.fixture
def mock_invalid_config_file():
    return mock_open(read_data=json.dumps(INVALID_CONFIG))

def test_load_config_valid(mock_config_file):
    with patch("builtins.open", mock_config_file):
        with patch("os.path.exists", return_value=True):
            config = load_config("mock_config.json")
            assert config == VALID_CONFIG

def test_load_config_invalid(mock_invalid_config_file):
    with patch("builtins.open", mock_invalid_config_file):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(ValueError, match="Invalid configuration"):
                load_config("mock_invalid_config.json")

def test_execute_workflow():
    results = execute_workflow(VALID_CONFIG)
    assert results == {"task1": "Result of task1", "task2": "Result of task2"}
