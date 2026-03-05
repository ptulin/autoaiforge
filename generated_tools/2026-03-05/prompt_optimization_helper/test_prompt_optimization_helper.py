import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from prompt_optimization_helper import evaluate_prompts

@patch("openai.Completion.create")
def test_evaluate_prompts_success(mock_openai):
    mock_openai.return_value = {"choices": [{"text": "This is a test response."}]}

    base_prompt = "Explain AI"
    variations = ["in simple terms", "to a 5-year-old"]
    api_key = "test_key"

    result = evaluate_prompts(base_prompt, variations, api_key)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert result["Score"].iloc[0] > 0

@patch("openai.Completion.create")
def test_evaluate_prompts_error_handling(mock_openai):
    mock_openai.side_effect = Exception("API Error")

    base_prompt = "Explain AI"
    variations = ["in simple terms"]
    api_key = "test_key"

    result = evaluate_prompts(base_prompt, variations, api_key)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result["Score"].iloc[0] == 0
    assert result["Output"].iloc[0] == "Error"

@patch("openai.Completion.create")
def test_evaluate_prompts_empty_variations(mock_openai):
    base_prompt = "Explain AI"
    variations = []
    api_key = "test_key"

    result = evaluate_prompts(base_prompt, variations, api_key)

    assert isinstance(result, pd.DataFrame)
    assert result.empty
