import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from sandbox_action_visualizer import load_logs, filter_logs, generate_visualization
import matplotlib.pyplot as plt
import json

@pytest.fixture
def sample_json_logs():
    return [
        {"timestamp": "2023-01-01T12:00:00", "agent_id": "agent_1", "action": "move"},
        {"timestamp": "2023-01-01T12:01:00", "agent_id": "agent_2", "action": "jump"},
        {"timestamp": "2023-01-01T12:02:00", "agent_id": "agent_1", "action": "stop"}
    ]

@pytest.fixture
def sample_csv_logs():
    return """timestamp,agent_id,action
2023-01-01T12:00:00,agent_1,move
2023-01-01T12:01:00,agent_2,jump
2023-01-01T12:02:00,agent_1,stop
"""

def test_load_logs_json(sample_json_logs):
    with patch("builtins.open", mock_open(read_data=json.dumps(sample_json_logs))):
        with patch("os.path.exists", return_value=True):
            df = load_logs("dummy.json")
            assert not df.empty
            assert len(df) == 3
            assert list(df.columns) == ["timestamp", "agent_id", "action"]

def test_load_logs_csv(sample_csv_logs):
    with patch("builtins.open", mock_open(read_data=sample_csv_logs)):
        with patch("os.path.exists", return_value=True):
            with patch("pandas.read_csv", return_value=pd.read_csv(mock_open(read_data=sample_csv_logs)())):
                df = load_logs("dummy.csv")
                assert not df.empty
                assert len(df) == 3
                assert list(df.columns) == ["timestamp", "agent_id", "action"]

def test_filter_logs():
    data = pd.DataFrame([
        {"timestamp": "2023-01-01T12:00:00", "agent_id": "agent_1", "action": "move"},
        {"timestamp": "2023-01-01T12:01:00", "agent_id": "agent_2", "action": "jump"},
        {"timestamp": "2023-01-01T12:02:00", "agent_id": "agent_1", "action": "stop"}
    ])
    filtered = filter_logs(data, agent="agent_1")
    assert len(filtered) == 2
    assert all(filtered["agent_id"] == "agent_1")

def test_generate_visualization(sample_json_logs):
    df = pd.DataFrame(sample_json_logs)
    with patch.object(plt, "show") as mock_show:
        generate_visualization(df)
        mock_show.assert_called_once()

def test_generate_visualization_empty():
    df = pd.DataFrame()
    with pytest.raises(ValueError, match="No data to visualize after applying filters."):
        generate_visualization(df)