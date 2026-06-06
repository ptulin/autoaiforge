import pytest
from unittest.mock import patch, mock_open
from ai_code_completion_cli import get_code_completion, read_input_file
import openai

def test_get_code_completion_success():
    mock_response = {
        'choices': [{'text': 'def hello_world():\n    print("Hello, world!")'}]
    }

    with patch('openai.Completion.create', return_value=mock_response):
        result = get_code_completion("fake-api-key", "def hello_world():\n", max_tokens=50)
        assert result == 'def hello_world():\n    print("Hello, world!")'

def test_get_code_completion_api_error():
    with patch('openai.Completion.create', side_effect=openai.error.OpenAIError("API error")):
        with pytest.raises(RuntimeError, match="Error communicating with OpenAI API: API error"):
            get_code_completion("fake-api-key", "def hello_world():\n", max_tokens=50)

def test_read_input_file_success():
    mock_file_content = "def hello_world():\n    print('Hello, world!')"
    with patch('os.path.exists', return_value=True):
        with patch('builtins.open', mock_open(read_data=mock_file_content)):
            result = read_input_file("fake_file.py")
            assert result == mock_file_content

def test_read_input_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError, match="The file 'nonexistent_file.py' does not exist."):
            read_input_file("nonexistent_file.py")
