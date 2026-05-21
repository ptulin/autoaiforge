import pytest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from ai_email_generator import generate_email, EmailRequest

def test_generate_email_success():
    api_key = "test_api_key"
    email_request = EmailRequest(tone="formal", purpose="follow-up", key_points="meeting recap, next steps")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="This is a generated email.")]

    with patch("openai.Completion.create", return_value=mock_response):
        result = generate_email(api_key, email_request)
        assert result == "This is a generated email."

def test_generate_email_failure():
    api_key = "test_api_key"
    email_request = EmailRequest(tone="formal", purpose="follow-up", key_points="meeting recap, next steps")

    with patch("openai.Completion.create", side_effect=Exception("API Error")):
        with pytest.raises(RuntimeError, match="Failed to generate email: API Error"):
            generate_email(api_key, email_request)

def test_email_request_validation():
    with pytest.raises(ValidationError):
        EmailRequest(tone="", purpose="follow-up", key_points="meeting recap, next steps")

    with pytest.raises(ValidationError):
        EmailRequest(tone="formal", purpose="", key_points="meeting recap, next steps")

    with pytest.raises(ValidationError):
        EmailRequest(tone="formal", purpose="follow-up", key_points="")

def test_email_request_valid():
    email_request = EmailRequest(tone="formal", purpose="follow-up", key_points="meeting recap, next steps")
    assert email_request.tone == "formal"
    assert email_request.purpose == "follow-up"
    assert email_request.key_points == "meeting recap, next steps"
