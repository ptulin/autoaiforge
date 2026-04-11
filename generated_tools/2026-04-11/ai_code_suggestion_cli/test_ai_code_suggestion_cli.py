import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from ai_code_suggestion_cli import ai_code_suggestion_cli
import openai

@pytest.fixture
def mock_openai_response():
    return MagicMock(
        choices=[
            MagicMock(text='def factorial(n):\n    if n == 0: return 1\n    return n * factorial(n-1)')
        ]
    )

def test_ai_code_suggestion_cli_success(mock_openai_response):
    runner = CliRunner()
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_api_key'}):
        with patch('openai.Completion.create', return_value=mock_openai_response):
            result = runner.invoke(ai_code_suggestion_cli, ['--language', 'python', '--snippet', 'def factorial(n):', '--comment', 'Write code to calculate factorial recursively'])
            assert result.exit_code == 0
            assert 'Generated Code:' in result.output
            assert 'def factorial(n):' in result.output

def test_ai_code_suggestion_cli_missing_api_key():
    runner = CliRunner()
    with patch.dict('os.environ', {}, clear=True):
        result = runner.invoke(ai_code_suggestion_cli, ['--language', 'python', '--snippet', 'def factorial(n):'])
        assert result.exit_code == 0
        assert 'Error: OPENAI_API_KEY environment variable is not set.' in result.output

def test_ai_code_suggestion_cli_openai_error():
    runner = CliRunner()
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_api_key'}):
        with patch('openai.Completion.create', side_effect=openai.error.OpenAIError('API error')):
            result = runner.invoke(ai_code_suggestion_cli, ['--language', 'python', '--snippet', 'def factorial(n):'])
            assert result.exit_code == 0
            assert 'Error: API error' in result.output

def test_ai_code_suggestion_cli_unexpected_error():
    runner = CliRunner()
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_api_key'}):
        with patch('openai.Completion.create', side_effect=Exception('Unexpected error occurred')):
            result = runner.invoke(ai_code_suggestion_cli, ['--language', 'python', '--snippet', 'def factorial(n):'])
            assert result.exit_code == 0
            assert 'Unexpected error: Unexpected error occurred' in result.output
