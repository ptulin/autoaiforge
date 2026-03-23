import pytest
import pandas as pd
from unittest.mock import patch
from ai_backtesting_toolkit import backtest

def mock_strategy(data):
    """Mock trading strategy for testing."""
    trades = data.copy()
    trades["action"] = "hold"
    trades.loc[trades.index[::10], "action"] = "buy"
    trades.loc[trades.index[5::10], "action"] = "sell"
    return trades

@patch("pandas.read_csv")
def test_backtest_success(mock_read_csv):
    # Mock data
    mock_data = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "price": [100, 105, 110]
    })
    mock_read_csv.return_value = mock_data

    # Run backtest
    metrics = backtest(mock_strategy, "mock_data.csv")

    # Assertions
    assert "ROI" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Final Balance" in metrics
    assert metrics["ROI"] >= 0

@patch("pandas.read_csv")
def test_backtest_empty_csv(mock_read_csv):
    # Mock empty data
    mock_read_csv.return_value = pd.DataFrame()

    # Run backtest and expect error
    with pytest.raises(ValueError, match="The input CSV file is empty."):
        backtest(mock_strategy, "mock_data.csv")

@patch("pandas.read_csv")
def test_backtest_missing_columns(mock_read_csv):
    # Mock data with missing columns
    mock_data = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "volume": [1000, 1050, 1100]
    })
    mock_read_csv.return_value = mock_data

    # Run backtest and expect error
    with pytest.raises(ValueError, match="CSV file must contain columns: date, price"):
        backtest(mock_strategy, "mock_data.csv")