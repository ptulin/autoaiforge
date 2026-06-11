import pytest
from unittest.mock import patch, mock_open
from parallel_execution_recommender import analyze_code_for_parallelization
import openai

def test_analyze_code_for_parallelization_valid_file():
    mock_script_content = "for i in range(100):\n    print(i)"
    mock_response = {"choices": [{"text": "Consider using multiprocessing for the loop."}]}

    with patch("builtins.open", mock_open(read_data=mock_script_content)), \
         patch("os.path.exists", return_value=True), \
         patch("openai.Completion.create", return_value=mock_response):
        result = analyze_code_for_parallelization("test_script.py", "fake_api_key")
        assert "Consider using multiprocessing for the loop." in result

def test_analyze_code_for_parallelization_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            analyze_code_for_parallelization("non_existent_file.py", "fake_api_key")

def test_analyze_code_for_parallelization_api_error():
    mock_script_content = "for i in range(100):\n    print(i)"

    with patch("builtins.open", mock_open(read_data=mock_script_content)), \
         patch("os.path.exists", return_value=True), \
         patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API error")):
        with pytest.raises(RuntimeError, match="Error communicating with OpenAI API: API error"):
            analyze_code_for_parallelization("test_script.py", "fake_api_key")

def test_analyze_code_for_parallelization_unexpected_response():
    mock_script_content = "for i in range(100):\n    print(i)"
    mock_response = {"unexpected_key": "unexpected_value"}  # Simulate unexpected response format

    with patch("builtins.open", mock_open(read_data=mock_script_content)), \
         patch("os.path.exists", return_value=True), \
         patch("openai.Completion.create", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Unexpected response format from OpenAI API."):
            analyze_code_for_parallelization("test_script.py", "fake_api_key")
