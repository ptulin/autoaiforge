import pytest
from unittest.mock import patch, MagicMock
from recursive_prompt_optimizer import simulate_recursive_chain, measure_token_efficiency, optimize_prompt
from nltk.tokenize import word_tokenize

@pytest.fixture(autouse=True)
def nltk_downloads():
    import nltk
    nltk.download("punkt")

def test_simulate_recursive_chain():
    mock_response = {"choices": [{"text": "Response text"}]}

    with patch("openai.Completion.create", return_value=mock_response):
        prompt_template = "What is the result of {input}?"
        task_config = {"input": "2 + 2"}
        result = simulate_recursive_chain(prompt_template, task_config, max_depth=2)

    assert len(result["results"]) == 2
    assert result["results"][0]["response"] == "Response text"

def test_measure_token_efficiency():
    with patch("tiktoken.encoding_for_model") as mock_encoding:
        mock_encoder = MagicMock()
        mock_encoder.encode.return_value = [1, 2, 3, 4]
        mock_encoding.return_value = mock_encoder
        prompt = "This is a test prompt."
        token_count = measure_token_efficiency(prompt)

    assert token_count == 4

def test_optimize_prompt():
    prompt_template = "What is the result of {input}? This is a test prompt."
    task_config = {"input": "2 + 2"}

    with patch("tiktoken.encoding_for_model") as mock_encoding:
        mock_encoder = MagicMock()
        mock_encoder.encode.side_effect = lambda x: list(range(len(word_tokenize(x))))
        mock_encoding.return_value = mock_encoder
        result = optimize_prompt(prompt_template, task_config, max_iterations=2)

    assert "optimized_prompt" in result
    assert "token_usage" in result
    assert result["token_usage"] > 0