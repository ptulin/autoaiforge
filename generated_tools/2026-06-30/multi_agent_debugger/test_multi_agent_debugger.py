import pytest
import json
from unittest.mock import patch, mock_open
from multi_agent_debugger import MultiAgentDebugger

def test_parse_input_valid_file():
    mock_data = json.dumps([
        {"timestamp": "2023-10-01T12:00:00Z", "agent": "Agent1", "event": "TaskStart", "details": "Task A"},
        {"timestamp": "2023-10-01T12:01:00Z", "agent": "Agent2", "event": "TaskEnd", "details": "Task B"}
    ])

    with patch("builtins.open", mock_open(read_data=mock_data)):
        debugger = MultiAgentDebugger(input_source="mock_file.json", level="info")
        events = debugger.parse_input()

    assert len(events) == 2
    assert events[0]["agent"] == "Agent1"
    assert events[1]["event"] == "TaskEnd"

def test_parse_input_file_not_found():
    debugger = MultiAgentDebugger(input_source="non_existent.json", level="info")

    with patch("builtins.open", side_effect=FileNotFoundError):
        events = debugger.parse_input()

    assert events == []

def test_parse_input_invalid_json():
    invalid_json = "{invalid_json: true"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        debugger = MultiAgentDebugger(input_source="mock_file.json", level="info")
        events = debugger.parse_input()

    assert events == []