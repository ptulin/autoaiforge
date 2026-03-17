import pytest
from unittest.mock import patch, mock_open
from agent_communication_visualizer import parse_logs, generate_graph
import os

def test_parse_logs_valid():
    mock_data = "agent1,agent2\nagent2,agent3\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = parse_logs("mock_log.log")
        assert result == [("agent1", "agent2"), ("agent2", "agent3")]

def test_parse_logs_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_logs("nonexistent.log")

def test_parse_logs_invalid_format():
    mock_data = "agent1-agent2\nagent3\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(ValueError, match="Invalid log format"):
            parse_logs("mock_log.log")

def test_generate_graph():
    communication_flows = [("agent1", "agent2"), ("agent2", "agent3")]
    output_file = "test_graph.png"

    generate_graph(communication_flows, output_file)

    assert os.path.exists(output_file)
    os.remove(output_file)