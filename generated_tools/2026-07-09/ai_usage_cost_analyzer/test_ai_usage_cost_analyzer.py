import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from ai_usage_cost_analyzer import load_pricing_model, load_usage_logs, calculate_costs

def test_load_pricing_model():
    mock_pricing_model = '{"api1": {"cost_per_call": 0.01}, "api2": {"cost_per_call": 0.02}}'
    with patch("builtins.open", mock_open(read_data=mock_pricing_model)):
        pricing_model = load_pricing_model("pricing_model.json")
        assert pricing_model == {"api1": {"cost_per_call": 0.01}, "api2": {"cost_per_call": 0.02}}

def test_load_usage_logs_json():
    mock_usage_logs = '[{"api_name": "api1", "usage_count": 100}, {"api_name": "api2", "usage_count": 200}]'
    with patch("builtins.open", mock_open(read_data=mock_usage_logs)):
        with patch("pandas.read_json") as mock_read_json:
            mock_read_json.return_value = pd.DataFrame([
                {"api_name": "api1", "usage_count": 100},
                {"api_name": "api2", "usage_count": 200}
            ])
            usage_logs = load_usage_logs("usage_logs.json")
            assert not usage_logs.empty
            assert list(usage_logs.columns) == ['api_name', 'usage_count']

def test_calculate_costs():
    usage_logs = pd.DataFrame([
        {"api_name": "api1", "usage_count": 100},
        {"api_name": "api2", "usage_count": 200}
    ])
    pricing_model = {"api1": {"cost_per_call": 0.01}, "api2": {"cost_per_call": 0.02}}
    result = calculate_costs(usage_logs, pricing_model)
    assert 'cost' in result.columns
    assert result['cost'].iloc[0] == 1.0
    assert result['cost'].iloc[1] == 4.0