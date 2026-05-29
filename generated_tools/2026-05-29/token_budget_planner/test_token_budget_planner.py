import pytest
import json
from unittest.mock import patch, mock_open
from token_budget_planner import load_config, estimate_tokens, calculate_token_usage

def mock_encoding_for_model(model):
    """Mock function to simulate tiktoken.encoding_for_model."""
    class MockEncoder:
        def encode(self, prompt):
            return [ord(char) for char in prompt]

    return MockEncoder()

def test_load_config_valid():
    mock_data = '[{"name": "Step 1", "prompt": "Hello", "model": "gpt-3.5-turbo", "max_tokens": 100}]'
    with patch('builtins.open', mock_open(read_data=mock_data)):
        config = load_config('mock_config.json')
        assert len(config) == 1
        assert config[0]['name'] == 'Step 1'

def test_load_config_invalid_json():
    with patch('builtins.open', mock_open(read_data='invalid json')):
        with pytest.raises(ValueError, match="Invalid JSON format"):
            load_config('mock_config.json')

def test_estimate_tokens():
    with patch('token_budget_planner.encoding_for_model', side_effect=mock_encoding_for_model):
        tokens = estimate_tokens("Hello", "gpt-3.5-turbo")
        assert tokens == 5

def test_calculate_token_usage():
    mock_config = [
        {"name": "Step 1", "prompt": "Hello", "model": "gpt-3.5-turbo", "max_tokens": 10}
    ]
    with patch('token_budget_planner.encoding_for_model', side_effect=mock_encoding_for_model):
        results = calculate_token_usage(mock_config)
        assert len(results) == 1
        assert results[0]['tokens_used'] == 5
        assert results[0]['tokens_remaining'] == 5
        assert not results[0]['exceeded']