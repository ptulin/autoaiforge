import pytest
from unittest.mock import patch, MagicMock
from task_prompt_optimizer import optimize_prompt

def mock_openai_completion_create(*args, **kwargs):
    """Mock function for openai.Completion.create."""
    class MockResponse:
        def __init__(self, text):
            self.choices = [MagicMock(text=text)]

    prompt = kwargs.get("prompt", "")
    if "Optimize this prompt" in prompt:
        return MockResponse("Optimized " + prompt.split(":", 1)[1].strip())
    return MockResponse(prompt)

@patch("openai.Completion.create", side_effect=mock_openai_completion_create)
def test_optimize_prompt_single_iteration(mock_create):
    api_key = "test_key"
    input_prompt = "Write a Python script to sort a list"
    iterations = 1

    result = optimize_prompt(api_key, input_prompt, iterations)

    assert result == "Optimized Write a Python script to sort a list"
    mock_create.assert_called_once()

@patch("openai.Completion.create", side_effect=mock_openai_completion_create)
def test_optimize_prompt_multiple_iterations(mock_create):
    api_key = "test_key"
    input_prompt = "Write a Python script to sort a list"
    iterations = 3

    result = optimize_prompt(api_key, input_prompt, iterations)

    assert result == "Optimized Optimized Optimized Write a Python script to sort a list"
    assert mock_create.call_count == 3

@patch("openai.Completion.create", side_effect=mock_openai_completion_create)
def test_optimize_prompt_early_stop(mock_create):
    api_key = "test_key"
    input_prompt = "Write a Python script to sort a list"
    iterations = 5

    # Simulate no further optimization after the first iteration
    def side_effect(*args, **kwargs):
        return MagicMock(choices=[MagicMock(text=input_prompt)])

    mock_create.side_effect = side_effect

    result = optimize_prompt(api_key, input_prompt, iterations)

    assert result == input_prompt
    mock_create.assert_called_once()