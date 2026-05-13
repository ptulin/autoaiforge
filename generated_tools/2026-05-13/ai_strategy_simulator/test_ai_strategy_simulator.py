import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from ai_strategy_simulator import load_data, apply_strategy, evaluate_performance

def test_load_data_valid_file(tmp_path):
    csv_content = """Date,Price
2023-01-01,100
2023-01-02,101
2023-01-03,102
"""
    file_path = tmp_path / "market_data.csv"
    file_path.write_text(csv_content)

    data = load_data(file_path)
    assert not data.empty
    assert 'Date' in data.columns
    assert 'Price' in data.columns

def test_load_data_invalid_file():
    with pytest.raises(ValueError, match="Error loading data"):
        load_data("non_existent_file.csv")

def test_apply_strategy():
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=3),
        'Price': [100, 101, 102]
    })
    result = apply_strategy(data, 'linear_regression', 'buy_low_sell_high')
    assert 'Predicted' in result.columns
    assert 'Signal' in result.columns

def test_evaluate_performance():
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=3),
        'Price': [100, 101, 102],
        'Signal': [1, 0, 1]
    })
    cumulative_strategy_return, cumulative_market_return = evaluate_performance(data)
    assert len(cumulative_strategy_return) == len(data)
    assert len(cumulative_market_return) == len(data)
