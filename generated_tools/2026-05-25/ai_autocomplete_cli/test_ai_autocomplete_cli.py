import pytest
from unittest.mock import patch, MagicMock
from ai_autocomplete_cli import fetch_completions

def test_fetch_completions_success():
    """Test fetch_completions with valid input."""
    mock_response = {
        'choices': [
            {'text': 'def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)'},
            {'text': 'def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)'},
            {'text': 'def factorial(n):\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result'}
        ]
    }

    with patch('openai.Completion.create', return_value=mock_response):
        completions = fetch_completions("def factorial(n):", "text-davinci-003")
        assert len(completions) == 3
        assert completions[0].startswith("def factorial")

def test_fetch_completions_error():
    """Test fetch_completions with API error."""
    with patch('openai.Completion.create', side_effect=Exception("API error")):
        with pytest.raises(RuntimeError, match="Error fetching completions: API error"):
            fetch_completions("def factorial(n):", "text-davinci-003")

def test_fetch_completions_empty_input():
    """Test fetch_completions with empty input."""
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = {'choices': []}
        completions = fetch_completions("", "text-davinci-003")
        assert completions == []
