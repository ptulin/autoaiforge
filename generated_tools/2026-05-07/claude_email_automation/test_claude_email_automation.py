import pytest
from unittest.mock import patch, MagicMock
from claude_email_automation import analyze_email_content

def test_analyze_email_content_response():
    email_content = "Hello, can we schedule a meeting next week?"
    mode = "response"
    mock_openai_response = MagicMock()
    mock_openai_response.choices = [MagicMock(text="Sure, I am available next week.")]

    with patch("openai.Completion.create", return_value=mock_openai_response):
        result = analyze_email_content(email_content, mode)
        assert "Sure, I am available next week." in result

def test_analyze_email_content_summary():
    email_content = "Subject: Meeting\n\nWe need to discuss the project updates and deadlines."
    mode = "summary"
    mock_openai_response = MagicMock()
    mock_openai_response.choices = [MagicMock(text="Discuss project updates and deadlines.")]

    with patch("openai.Completion.create", return_value=mock_openai_response):
        result = analyze_email_content(email_content, mode)
        assert "Discuss project updates and deadlines." in result

def test_analyze_email_content_action_items():
    email_content = "Please complete the report by Friday and schedule a call with the client."
    mode = "action_items"
    mock_openai_response = MagicMock()
    mock_openai_response.choices = [MagicMock(text="1. Complete the report by Friday.\n2. Schedule a call with the client.")]

    with patch("openai.Completion.create", return_value=mock_openai_response):
        result = analyze_email_content(email_content, mode)
        assert "1. Complete the report by Friday." in result
        assert "2. Schedule a call with the client." in result

def test_analyze_email_content_empty_email():
    email_content = ""
    mode = "response"
    with pytest.raises(ValueError, match="Email content is empty."):
        analyze_email_content(email_content, mode)

def test_analyze_email_content_invalid_mode():
    email_content = "Hello, can we schedule a meeting next week?"
    mode = "invalid_mode"
    with pytest.raises(ValueError, match="Invalid mode. Choose from 'response', 'summary', or 'action_items'."):
        analyze_email_content(email_content, mode)

def test_analyze_email_content_api_error():
    email_content = "Hello, can we schedule a meeting next week?"
    mode = "response"
    with patch("openai.Completion.create", side_effect=Exception("API error")):
        with pytest.raises(RuntimeError, match="Error communicating with OpenAI API: API error"):
            analyze_email_content(email_content, mode)