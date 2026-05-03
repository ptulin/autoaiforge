import pytest
from unittest.mock import patch, MagicMock
from ai_script_enhancer import enhance_script
import os
import tempfile
import openai

def test_enhance_script_valid_input():
    """Test enhance_script with valid input."""
    script_content = "Character: Hello! How are you?"
    tone = "formal"
    mock_response = {
        'choices': [
            {'message': {'content': "Character: Greetings! How do you do?"}}
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(script_content.encode())
            temp_file.close()

            result = enhance_script(temp_file.name, tone)
            os.unlink(temp_file.name)

            assert result == "Character: Greetings! How do you do?"

def test_enhance_script_file_not_found():
    """Test enhance_script with a non-existent file."""
    tone = "formal"
    with pytest.raises(FileNotFoundError):
        enhance_script("non_existent_file.txt", tone)

def test_enhance_script_empty_file():
    """Test enhance_script with an empty file."""
    tone = "formal"
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.close()
        with pytest.raises(ValueError):
            enhance_script(temp_file.name, tone)
        os.unlink(temp_file.name)

def test_enhance_script_openai_error():
    """Test enhance_script when OpenAI API fails."""
    script_content = "Character: Hello! How are you?"
    tone = "formal"

    with patch('openai.ChatCompletion.create', side_effect=openai.error.OpenAIError("API Error")):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(script_content.encode())
            temp_file.close()

            with pytest.raises(RuntimeError, match="Failed to process the script: API Error"):
                enhance_script(temp_file.name, tone)

            os.unlink(temp_file.name)