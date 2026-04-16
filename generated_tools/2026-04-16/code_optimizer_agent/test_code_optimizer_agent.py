import pytest
from unittest.mock import patch, mock_open
from code_optimizer_agent import optimize_code

def test_optimize_code_valid_file():
    mock_file_content = "print('Hello, World!')"
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': "Optimized code and suggestions here."
                }
            }
        ]
    }

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.isfile", return_value=True):
            with patch("openai.ChatCompletion.create", return_value=mock_response):
                optimized_code, suggestions = optimize_code("test.py", "fake_api_key")
                assert "print(\"Hello, World!\")" in optimized_code  # Adjusted to match Black's formatting
                assert "Optimized code and suggestions here." in suggestions

def test_optimize_code_file_not_found():
    with patch("os.path.isfile", return_value=False):
        with pytest.raises(FileNotFoundError):
            optimize_code("nonexistent.py", "fake_api_key")

def test_optimize_code_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        with patch("os.path.isfile", return_value=True):
            with pytest.raises(ValueError):
                optimize_code("empty.py", "fake_api_key")
