import pytest
from unittest.mock import patch, MagicMock
import openai
from auto_snippet_generator import generate_code_snippet

def test_generate_code_snippet_success():
    """Test successful generation of a code snippet."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="def example():\n    pass")]

    with patch("openai.Completion.create", return_value=mock_response), \
         patch("os.getenv", return_value="fake_api_key"):
        result = generate_code_snippet("create a function", None)
        assert result == "def example():\n    pass"

def test_generate_code_snippet_with_framework():
    """Test generation of a code snippet with a specific framework."""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="import pandas as pd\n\ndef read_csv():\n    pass")]

    with patch("openai.Completion.create", return_value=mock_response), \
         patch("os.getenv", return_value="fake_api_key"):
        result = generate_code_snippet("read a CSV", "pandas")
        assert result == "import pandas as pd\n\ndef read_csv():\n    pass"

def test_generate_code_snippet_api_key_missing():
    """Test behavior when OPENAI_API_KEY is missing."""
    with patch("os.getenv", return_value=None):
        with pytest.raises(ValueError, match="OPENAI_API_KEY environment variable is not set."):
            generate_code_snippet("create a function", None)

def test_generate_code_snippet_api_error():
    """Test behavior when OpenAI API raises an error."""
    with patch("openai.Completion.create", side_effect=openai.error.OpenAIError("API error")), \
         patch("os.getenv", return_value="fake_api_key"):
        with pytest.raises(RuntimeError, match="Error communicating with OpenAI API: API error"):
            generate_code_snippet("create a function", None)
