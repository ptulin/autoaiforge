import pytest
import pandas as pd
from unittest.mock import patch
from ai_cost_forecaster import load_data, preprocess_data, forecast_linear_regression, forecast_arima

def test_load_data_csv():
    data = pd.DataFrame({'date': ['2023-01-01', '2023-01-02'], 'cost': [100, 200]})
    with patch('pandas.read_csv', return_value=data):
        result = load_data('test.csv')
        assert not result.empty
        assert list(result.columns) == ['date', 'cost']

def test_preprocess_data():
    data = pd.DataFrame({'date': ['2023-01-01', '2023-01-02'], 'cost': [100, 200]})
    result = preprocess_data(data)
    assert pd.api.types.is_datetime64_any_dtype(result['date'])
    assert list(result['cost']) == [100, 200]

def test_forecast_linear_regression():
    data = pd.DataFrame({'date': pd.to_datetime(['2023-01-01', '2023-01-02']), 'cost': [100, 200]})
    data = preprocess_data(data)
    forecast_days, forecast_values = forecast_linear_regression(data, 2)
    assert len(forecast_days) == 2
    assert len(forecast_values) == 2
    assert forecast_values[0] > 0