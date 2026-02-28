import pytest
from unittest.mock import patch, mock_open
import smart_code_review

def test_review_code_valid_file():
    mock_api_key = "test-api-key"
    mock_code = "def add(a, b):\n    return a + b"

    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_code)):
            with patch("openai.Completion.create") as mock_openai:
                mock_openai.return_value.choices = [type("", (), {"text": "Looks good."})]
                result = smart_code_review.review_code("test.py", mock_api_key)

    assert "Looks good." in result

def test_review_code_syntax_error():
    mock_api_key = "test-api-key"
    mock_code = "def add(a, b):\n    return a + "

    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_code)):
            result = smart_code_review.review_code("test.py", mock_api_key)

    assert "Syntax Error" in result

def test_review_directory():
    mock_api_key = "test-api-key"
    mock_code = "def add(a, b):\n    return a + b"

    with patch("os.path.isdir", return_value=True):
        with patch("os.walk", return_value=[("/mock", [], ["test.py"])]):
            with patch("os.path.isfile", return_value=True):
                with patch("builtins.open", mock_open(read_data=mock_code)):
                    with patch("openai.Completion.create") as mock_openai:
                        mock_openai.return_value.choices = [type("", (), {"text": "Looks good."})]
                        result = smart_code_review.review_directory("/mock", mock_api_key)

    assert "test.py" in result
    assert "Looks good." in result["test.py"]