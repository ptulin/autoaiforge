import pytest
from unittest.mock import patch, MagicMock
from gpt_claude_debugger import analyze_traceback_with_gpt, analyze_traceback_with_claude

def test_analyze_traceback_with_gpt():
    mock_response = {
        'choices': [
            {'message': {'content': 'Mock GPT response for debugging.'}}
        ]
    }
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        result = analyze_traceback_with_gpt("Mock traceback", "mock-api-key")
        assert result == 'Mock GPT response for debugging.'

def test_analyze_traceback_with_gpt_error():
    with patch('openai.ChatCompletion.create', side_effect=Exception("API error")):
        result = analyze_traceback_with_gpt("Mock traceback", "mock-api-key")
        assert "Error communicating with GPT API" in result

def test_analyze_traceback_with_claude():
    mock_client = MagicMock()
    mock_client.completion.return_value = {'completion': 'Mock Claude response for debugging.'}
    with patch('anthropic.Client', return_value=mock_client):
        result = analyze_traceback_with_claude("Mock traceback", "mock-api-key")
        assert result == 'Mock Claude response for debugging.'

def test_analyze_traceback_with_claude_error():
    mock_client = MagicMock()
    mock_client.completion.side_effect = Exception("API error")
    with patch('anthropic.Client', return_value=mock_client):
        result = analyze_traceback_with_claude("Mock traceback", "mock-api-key")
        assert "Error communicating with Claude API" in result