import pytest
from unittest.mock import patch, mock_open
from auto_test_gen import generate_tests
import openai

def test_generate_tests_with_valid_code():
    mock_response = {"choices": [{"text": "def test_example():\n    assert True"}]}

    with patch("openai.Completion.create", return_value=mock_response):
        result = generate_tests("def example():\n    pass", openai_api_key="fake_key")
        assert "def test_example()" in result

def test_generate_tests_with_file_path():
    mock_response = {"choices": [{"text": "def test_example():\n    assert True"}]}

    with patch("openai.Completion.create", return_value=mock_response):
        with patch("builtins.open", mock_open(read_data="def example():\n    pass")) as mock_file:
            with patch("os.path.isfile", return_value=True):
                result = generate_tests("example.py", openai_api_key="fake_key")
                mock_file.assert_called_once_with("example.py", 'r')
                assert "def test_example()" in result

def test_generate_tests_with_missing_api_key():
    with pytest.raises(ValueError, match="OpenAI API key must be provided"):
        generate_tests("def example():\n    pass", openai_api_key=None)

def test_generate_tests_with_api_error():
    with patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API Error")):
        with patch("openai.api_key", "fake_key"):
            with pytest.raises(RuntimeError, match="Failed to generate tests using OpenAI API"):
                generate_tests("def example():\n    pass", openai_api_key="fake_key")

def test_generate_tests_with_invalid_file_path():
    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(ValueError, match="File not found: invalid_file.py"):
                generate_tests("invalid_file.py", openai_api_key="fake_key")
