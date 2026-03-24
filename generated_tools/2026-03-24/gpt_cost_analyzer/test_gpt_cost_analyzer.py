import pytest
import json
from unittest.mock import patch, mock_open
from gpt_cost_analyzer import load_json, calculate_tokens_per_dollar, analyze_costs

def test_load_json_valid():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        data = load_json("mock_file.json")
        assert data == {"key": "value"}

def test_load_json_invalid():
    mock_data = 'invalid json'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with pytest.raises(ValueError, match="Invalid JSON format"):
            load_json("mock_file.json")

def test_calculate_tokens_per_dollar():
    pricing_data = {
        "gpt-4": {"price_per_1k_tokens": 0.03},
        "gpt-5": {"price_per_1k_tokens": 0.02}
    }
    tokens = 1000
    assert calculate_tokens_per_dollar(pricing_data, "gpt-4", tokens) == pytest.approx(33.33, 0.01)
    assert calculate_tokens_per_dollar(pricing_data, "gpt-5", tokens) == pytest.approx(50.0, 0.01)

def test_analyze_costs():
    prompts = ["Hello world", "How are you?"]
    models = ["gpt-4", "gpt-5"]
    pricing_data = {
        "gpt-4": {"price_per_1k_tokens": 0.03},
        "gpt-5": {"price_per_1k_tokens": 0.02}
    }
    results = analyze_costs(prompts, models, pricing_data)
    assert len(results) == 2
    assert results[0]['model'] == "gpt-4"
    assert results[1]['model'] == "gpt-5"
    assert 'tokens_per_dollar' in results[0]
    assert 'tokens_per_dollar' in results[1]

def test_analyze_costs_missing_model():
    prompts = ["Hello world"]
    models = ["gpt-6"]
    pricing_data = {
        "gpt-4": {"price_per_1k_tokens": 0.03},
        "gpt-5": {"price_per_1k_tokens": 0.02}
    }
    results = analyze_costs(prompts, models, pricing_data)
    assert len(results) == 1
    assert results[0]['model'] == "gpt-6"
    assert 'error' in results[0]