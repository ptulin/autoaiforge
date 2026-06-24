import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from agent_decision_tracer import load_decision_logs, validate_decision_logs, generate_execution_graph

def test_load_decision_logs_file():
    mock_data = '[{"step": 1, "decision": "start", "reasoning": "initialization"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        logs = load_decision_logs("mock_file.json")
        assert logs == json.loads(mock_data)

def test_load_decision_logs_stdin():
    mock_data = '[{"step": 1, "decision": "start", "reasoning": "initialization"}]'
    mock_stdin = MagicMock()
    mock_stdin.read.return_value = mock_data
    with patch("sys.stdin", mock_stdin):
        logs = load_decision_logs("-")
        assert logs == json.loads(mock_data)

def test_validate_decision_logs_valid():
    logs = [{"step": 1, "decision": "start", "reasoning": "initialization"}]
    validate_decision_logs(logs)  # Should not raise an exception

def test_validate_decision_logs_invalid():
    logs = [{"step": 1, "decision": "start"}]  # Missing 'reasoning'
    with pytest.raises(ValueError):
        validate_decision_logs(logs)

def test_generate_execution_graph():
    logs = [
        {"step": 1, "decision": "start", "reasoning": "initialization"},
        {"step": 2, "decision": "move", "reasoning": "next step", "previous_step": 1}
    ]
    with patch("graphviz.Digraph.render") as mock_render:
        generate_execution_graph(logs, "output_graph.png")
        mock_render.assert_called_once_with("output_graph", cleanup=True)