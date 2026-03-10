import pytest
from unittest.mock import patch, MagicMock
from gpt_secure_scripter import generate_script, validate_script, execute_script

def test_validate_script():
    safe_script = "echo 'Hello, World!'"
    dangerous_script = "rm -rf /"

    assert validate_script(safe_script, 'bash') is True
    assert validate_script(dangerous_script, 'bash') is False

@patch('gpt_secure_scripter.openai.Completion.create')
def test_generate_script(mock_openai):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="echo 'Hello, World!'")]
    mock_openai.return_value = mock_response

    instruction = "Write a script to print Hello, World!"
    script = generate_script(instruction, 'bash')

    assert script == "echo 'Hello, World!'"
    mock_openai.assert_called_once()

@patch('gpt_secure_scripter.sh.bash')
def test_execute_script(mock_bash):
    script = "echo 'Hello, World!'"

    # Test when user confirms execution
    with patch('builtins.input', return_value='yes'):
        execute_script(script, 'bash')
        mock_bash.assert_called_once_with('-c', script)

    mock_bash.reset_mock()

    # Test when user cancels execution
    with patch('builtins.input', return_value='no'):
        execute_script(script, 'bash')
        mock_bash.assert_not_called()