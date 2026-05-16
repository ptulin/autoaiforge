import pytest
import json
from unittest.mock import patch, MagicMock
from claude_auto_responder import load_config, generate_response, fetch_unread_emails

def test_load_config_valid():
    config_data = {
        "gmail_credentials_file": "credentials.json",
        "scenarios": [
            {"keyword": "refund", "response_template": "Hello, regarding your refund: {{customer_message}}"}
        ],
        "anthropic_api_key": "test_api_key"
    }
    with patch("builtins.open", new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(config_data)
        config = load_config("config.json")
        assert config.gmail_credentials_file == "credentials.json"
        assert len(config.scenarios) == 1
        assert config.scenarios[0].keyword == "refund"
        assert config.scenarios[0].response_template == "Hello, regarding your refund: {{customer_message}}"

def test_generate_response():
    with patch("claude_auto_responder.Anthropic") as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.completions.create.return_value = MagicMock(completion="AI Response")

        response = generate_response("test_api_key", "Test prompt")
        assert response == "AI Response"

def test_fetch_unread_emails():
    mock_service = MagicMock()
    mock_service.users().messages().list().execute.return_value = {"messages": [{"id": "123"}, {"id": "456"}]}

    messages = fetch_unread_emails(mock_service)
    assert len(messages) == 2
    assert messages[0]['id'] == "123"
    assert messages[1]['id'] == "456"
