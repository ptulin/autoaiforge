import pytest
from unittest.mock import patch
from llm_input_optimizer import optimize_prompt, count_tokens, estimate_cost

def test_count_tokens():
    assert count_tokens("Test prompt", "gpt-4") == 2
    assert count_tokens("This is a longer test prompt", "gpt-4") == 6
    assert count_tokens("", "gpt-4") == 0

def test_estimate_cost():
    assert estimate_cost(1000, "gpt-4") == 0.03
    assert estimate_cost(500, "claude-v1") == 0.01
    with pytest.raises(ValueError):
        estimate_cost(1000, "unsupported-model")

def test_optimize_prompt():
    with patch("llm_input_optimizer.count_tokens", return_value=50):
        with patch("llm_input_optimizer.estimate_cost", return_value=0.0015):
            result = optimize_prompt("Test prompt", "gpt-4")
            assert len(result) == 1
            assert result[0]["token_count"] == 50
            assert result[0]["estimated_cost"] == 0.0015
            assert "suggestions" in result[0]

    with patch("llm_input_optimizer.count_tokens", return_value=1500):
        with patch("llm_input_optimizer.estimate_cost", return_value=0.045):
            result = optimize_prompt(["Prompt 1", "Prompt 2"], "gpt-4")
            assert len(result) == 2
            assert result[0]["token_count"] == 1500
            assert result[1]["token_count"] == 1500

    with pytest.raises(ValueError):
        optimize_prompt(12345, "gpt-4")