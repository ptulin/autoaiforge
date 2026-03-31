import pytest
from unittest.mock import patch, MagicMock
from ai_code_optimizer import annotate_code

def mock_openai_response(*args, **kwargs):
    return MagicMock(choices=[MagicMock(text="Mocked GPT suggestion")])

def mock_anthropic_response(*args, **kwargs):
    return {"completion": "Mocked Claude suggestion"}

@patch('ai_code_optimizer.openai.Completion.create', side_effect=mock_openai_response)
@patch('ai_code_optimizer.anthropic.Client')
def test_annotate_code(mock_anthropic_client, mock_gpt):
    """Test annotate_code function with mocked API responses."""
    mock_claude_client = MagicMock()
    mock_claude_client.completion = MagicMock(side_effect=mock_anthropic_response)
    mock_anthropic_client.return_value = mock_claude_client

    code = "print('Hello, world!')"
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = code
        with patch('os.path.exists', return_value=True):
            result = annotate_code("dummy_path.py", "dummy_gpt_key", "dummy_claude_key")
            assert "Mocked GPT suggestion" in result
            assert "Mocked Claude suggestion" in result

def test_file_not_found():
    """Test annotate_code with a non-existent file."""
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            annotate_code("non_existent_file.py", "dummy_gpt_key", "dummy_claude_key")

@patch('ai_code_optimizer.openai.Completion.create', side_effect=mock_openai_response)
@patch('ai_code_optimizer.anthropic.Client')
def test_empty_file(mock_anthropic_client, mock_gpt):
    """Test annotate_code with an empty file."""
    mock_claude_client = MagicMock()
    mock_claude_client.completion = MagicMock(side_effect=mock_anthropic_response)
    mock_anthropic_client.return_value = mock_claude_client

    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = ""
        with patch('os.path.exists', return_value=True):
            result = annotate_code("dummy_path.py", "dummy_gpt_key", "dummy_claude_key")
            assert result == "The file is empty. No code to analyze."
