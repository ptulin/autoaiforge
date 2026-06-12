import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from io import StringIO
from ai_cost_analyzer import load_data, analyze_usage, generate_report

def test_load_data_csv():
    mock_csv = "timestamp,tokens,cost\n2023-10-01,100,0.5\n2023-10-02,200,1.0"
    with patch("builtins.open", mock_open(read_data=mock_csv)) as mock_file:
        with patch("pandas.read_csv", return_value=pd.read_csv(StringIO(mock_csv))):
            data = load_data("test.csv")
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ['timestamp', 'tokens', 'cost']
    assert len(data) == 2

def test_load_data_json():
    mock_json = '[{"timestamp": "2023-10-01", "tokens": 100, "cost": 0.5}, {"timestamp": "2023-10-02", "tokens": 200, "cost": 1.0}]'
    with patch("builtins.open", mock_open(read_data=mock_json)) as mock_file:
        with patch("pandas.read_json", return_value=pd.read_json(StringIO(mock_json))):
            data = load_data("test.json")
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ['timestamp', 'tokens', 'cost']
    assert len(data) == 2

def test_analyze_usage():
    data = pd.DataFrame({
        'timestamp': ['2023-10-01', '2023-10-01', '2023-10-02'],
        'tokens': [100, 150, 200],
        'cost': [0.5, 0.75, 1.0]
    })
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    daily_stats = analyze_usage(data)
    assert 'tokens' in daily_stats.columns
    assert 'cost' in daily_stats.columns
    assert daily_stats.loc['2023-10-01', 'tokens'] == 250
    assert daily_stats.loc['2023-10-01', 'cost'] == 1.25

def test_generate_report():
    daily_stats = pd.DataFrame({
        'tokens': [250, 200],
        'cost': [1.25, 1.0]
    }, index=pd.to_datetime(['2023-10-01', '2023-10-02']))

    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        generate_report(daily_stats, "test_report.pdf")
        mock_savefig.assert_called_once_with("test_report.pdf")