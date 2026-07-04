import pytest
from unittest.mock import patch, mock_open
import llm_cost_estimator

def test_load_pricing_config():
    mock_yaml = "openai:\n  cost_per_token: 0.0001"
    with patch("builtins.open", mock_open(read_data=mock_yaml)):
        config = llm_cost_estimator.load_pricing_config("pricing.yaml")
        assert config == {"openai": {"cost_per_token": 0.0001}}

def test_count_tokens():
    with patch("tiktoken.encoding_for_model") as mock_encoding:
        mock_encoding.return_value.encode.return_value = [1, 2, 3, 4, 5]
        tokens = llm_cost_estimator.count_tokens("Hello world!", "openai")
        assert tokens == 5

def test_estimate_cost():
    prompts = ["Hello world!", "How are you?"]
    pricing_config = {"openai": {"cost_per_token": 0.0001}}
    with patch("llm_cost_estimator.count_tokens", side_effect=[5, 3]):
        total_tokens, total_cost = llm_cost_estimator.estimate_cost(prompts, "openai", pricing_config)
        assert total_tokens == 8
        assert total_cost == pytest.approx(0.0008)
