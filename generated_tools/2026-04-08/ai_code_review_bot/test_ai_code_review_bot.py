import os
import pytest
from unittest.mock import patch, MagicMock
from ai_code_review_bot import analyze_code, process_path

@patch("ai_code_review_bot.ChatCompletion.create")
def test_analyze_code_success(mock_chat_completion):
    mock_chat_completion.return_value = {
        'choices': [{
            'message': {
                'content': 'This is a test suggestion.'
            }
        }]
    }

    with patch("os.getenv", return_value="fake_api_key"):
        result = analyze_code("print('Hello, world!')", "readability")
    assert result['success'] is True
    assert "This is a test suggestion." in result['suggestions']

@patch("ai_code_review_bot.ChatCompletion.create")
def test_analyze_code_failure(mock_chat_completion):
    mock_chat_completion.side_effect = Exception("API Error")

    with patch("os.getenv", return_value="fake_api_key"):
        result = analyze_code("print('Hello, world!')", "readability")
    assert result['success'] is False
    assert "API Error" in result['error']

@patch("ai_code_review_bot.analyze_code")
def test_process_path(mock_analyze_code):
    mock_analyze_code.return_value = {"success": True, "suggestions": "Test suggestion."}

    with patch("os.path.isfile", return_value=True):
        with patch("builtins.open", MagicMock(return_value=MagicMock(read=lambda: "print('Hello, world!')"))):
            results = process_path("test_file.py", "readability")

    assert len(results) == 1
    assert results[0]['file'] == "test_file.py"
    assert results[0]['result']['success'] is True
    assert "Test suggestion." in results[0]['result']['suggestions']
