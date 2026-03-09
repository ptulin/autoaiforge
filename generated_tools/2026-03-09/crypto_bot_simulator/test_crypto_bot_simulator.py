import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from crypto_bot_simulator import load_data, mean_reversion_strategy

def test_load_data_valid():
    csv_data = """timestamp,price
2023-01-01 00:00:00,100
2023-01-01 01:00:00,101
2023-01-01 02:00:00,102
"""
    mock_file = mock_open(read_data=csv_data)
    with patch("builtins.open", mock_file):
        data = load_data("dummy.csv")
        assert not data.empty
        assert 'price' in data.columns
        assert 'timestamp' in data.columns

def test_load_data_invalid():
    csv_data = """time,value
2023-01-01 00:00:00,100
2023-01-01 01:00:00,101
"""
    mock_file = mock_open(read_data=csv_data)
    with patch("builtins.open", mock_file):
        with pytest.raises(ValueError, match="CSV must contain 'timestamp' and 'price' columns."):
            load_data("dummy.csv")

def test_load_data_empty():
    csv_data = """"""
    mock_file = mock_open(read_data=csv_data)
    with patch("builtins.open", mock_file):
        with pytest.raises(ValueError, match="Error loading data: File is empty or invalid."):
            load_data("dummy.csv")

def test_mean_reversion_strategy():
    data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=5, freq='H'),
        'price': [100, 101, 102, 103, 104]
    })
    result = mean_reversion_strategy(data, window=2, threshold=0.5)
    assert 'cumulative_returns' in result.columns
    assert len(result) == 5
    assert result['cumulative_returns'].iloc[-1] > 0