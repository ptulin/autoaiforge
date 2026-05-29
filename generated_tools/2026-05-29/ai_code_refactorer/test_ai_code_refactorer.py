import pytest
from unittest.mock import patch, mock_open
import ai_code_refactorer
import openai

def test_load_api_key():
    with patch("ai_code_refactorer.os.getenv", return_value="test_api_key"):
        assert ai_code_refactorer.load_api_key() == "test_api_key"

def test_load_api_key_missing():
    with patch("ai_code_refactorer.os.getenv", return_value=None):
        with pytest.raises(ValueError, match="OPENAI_API_KEY not found in environment variables."):
            ai_code_refactorer.load_api_key()

def test_refactor_code_file_not_found():
    with pytest.raises(FileNotFoundError, match="File not found: non_existent_file.py"):
        ai_code_refactorer.refactor_code("non_existent_file.py")

def test_refactor_code_empty_file():
    with patch("ai_code_refactorer.open", mock_open(read_data="")):
        with patch("ai_code_refactorer.os.path.isfile", return_value=True):
            with pytest.raises(ValueError, match="The file is empty."):
                ai_code_refactorer.refactor_code("empty_file.py")

def test_refactor_code_openai_error():
    with patch("ai_code_refactorer.openai.Completion.create", side_effect=openai.error.OpenAIError("API Error")):
        with patch("ai_code_refactorer.open", mock_open(read_data="print('Hello World')")):
            with patch("ai_code_refactorer.os.path.isfile", return_value=True):
                with patch("ai_code_refactorer.load_api_key", return_value="test_api_key"):
                    with pytest.raises(RuntimeError, match="Error communicating with OpenAI API: API Error"):
                        ai_code_refactorer.refactor_code("test_file.py")

def test_refactor_code_success():
    mock_response = {"choices": [{"text": "print('Refactored Code')"}]}
    with patch("ai_code_refactorer.openai.Completion.create", return_value=mock_response):
        with patch("ai_code_refactorer.open", mock_open(read_data="print('Hello World')")):
            with patch("ai_code_refactorer.os.path.isfile", return_value=True):
                with patch("ai_code_refactorer.load_api_key", return_value="test_api_key"):
                    result = ai_code_refactorer.refactor_code("test_file.py")
                    assert result == "print('Refactored Code')"
