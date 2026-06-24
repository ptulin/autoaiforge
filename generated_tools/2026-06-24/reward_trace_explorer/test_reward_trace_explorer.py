import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from io import StringIO
from reward_trace_explorer import load_data, analyze_rewards, plot_rewards

def test_load_data_csv():
    csv_content = "step,reward\n1,10\n2,20\n3,30"
    with patch("pandas.read_csv", return_value=pd.read_csv(StringIO(csv_content))):
        data = load_data("test.csv")
    assert isinstance(data, pd.DataFrame)
    assert data.shape == (3, 2)

def test_load_data_json():
    json_content = '[{"step": 1, "reward": 10}, {"step": 2, "reward": 20}]'
    with patch("pandas.read_json", return_value=pd.read_json(StringIO(json_content))):
        data = load_data("test.json")
    assert isinstance(data, pd.DataFrame)
    assert data.shape == (2, 2)

def test_analyze_rewards():
    data = pd.DataFrame({"step": [1, 2, 3], "reward": [10, 20, 30]})
    summary = analyze_rewards(data)
    assert summary['total_rewards'] == 60
    assert summary['average_reward'] == 20
    assert summary['max_reward'] == 30
    assert summary['min_reward'] == 10
    assert summary['steps'] == 3

def test_plot_rewards():
    data = pd.DataFrame({"step": [1, 2, 3], "reward": [10, 20, 30]})
    output_file = "test_plot.png"
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        plot_rewards(data, output_file)
        mock_savefig.assert_called_once_with(output_file)