import pytest
from unittest.mock import patch, MagicMock
from llm_code_assistant import llm_code_assistant
import os

def test_query():
    with patch('llm_code_assistant.openai.Completion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text='def sort_array(arr):\n    return sorted(arr)')])
        with patch('llm_code_assistant.os.getenv', return_value='fake_api_key'):
            result = llm_code_assistant(query='Write a Python function to sort an array')
            assert result == 'def sort_array(arr):\n    return sorted(arr)'

def test_file(tmp_path):
    with patch('llm_code_assistant.openai.Completion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text='def optimized_function():\n    pass')])
        test_file = tmp_path / "test_file.py"
        test_file.write_text('def test_function():\n    pass')

        with patch('llm_code_assistant.os.getenv', return_value='fake_api_key'):
            result = llm_code_assistant(file=str(test_file))
            assert result == 'def optimized_function():\n    pass'

def test_output_to_file(tmp_path):
    with patch('llm_code_assistant.openai.Completion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text='def sort_array(arr):\n    return sorted(arr)')])
        output_file = tmp_path / "output.py"

        with patch('llm_code_assistant.os.getenv', return_value='fake_api_key'):
            result = llm_code_assistant(query='Write a Python function to sort an array', output=str(output_file))
            assert result == 'def sort_array(arr):\n    return sorted(arr)'
            assert output_file.read_text() == 'def sort_array(arr):\n    return sorted(arr)'

def test_missing_api_key():
    with patch('llm_code_assistant.os.getenv', return_value=None):
        result = llm_code_assistant(query='Write a Python function to sort an array')
        assert result == "Error: OPENAI_API_KEY environment variable not set."

def test_missing_file():
    with patch('llm_code_assistant.os.getenv', return_value='fake_api_key'):
        result = llm_code_assistant(file='nonexistent_file.py')
        assert result == "Error: File not found."