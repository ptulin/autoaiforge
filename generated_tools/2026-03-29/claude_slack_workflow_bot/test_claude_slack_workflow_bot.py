import pytest
from unittest.mock import patch, MagicMock
from slack_sdk.errors import SlackApiError
from claude_slack_workflow_bot import create_slack_workflow

def test_create_slack_workflow_success():
    slack_token = "test-slack-token"
    trigger_channel = "#general"
    prompt = "Summarize this conversation"

    mock_slack_client = MagicMock()
    mock_slack_client.conversations_list.return_value = {
        "channels": [
            {"id": "C12345", "name": "general"},
            {"id": "C67890", "name": "random"}
        ]
    }

    with patch("claude_slack_workflow_bot.WebClient", return_value=mock_slack_client):
        workflow = create_slack_workflow(slack_token, trigger_channel, prompt)

    assert workflow["name"] == "Claude Workflow"
    assert workflow["trigger_channel"] == trigger_channel
    assert workflow["prompt"] == prompt

def test_create_slack_workflow_channel_not_found():
    slack_token = "test-slack-token"
    trigger_channel = "#nonexistent"
    prompt = "Summarize this conversation"

    mock_slack_client = MagicMock()
    mock_slack_client.conversations_list.return_value = {
        "channels": [
            {"id": "C12345", "name": "general"},
            {"id": "C67890", "name": "random"}
        ]
    }

    with patch("claude_slack_workflow_bot.WebClient", return_value=mock_slack_client):
        with pytest.raises(RuntimeError, match="Channel '#nonexistent' not found."):
            create_slack_workflow(slack_token, trigger_channel, prompt)

def test_create_slack_workflow_slack_api_error():
    slack_token = "test-slack-token"
    trigger_channel = "#general"
    prompt = "Summarize this conversation"

    mock_slack_client = MagicMock()
    mock_slack_client.conversations_list.side_effect = SlackApiError("invalid_auth", response={"error": "invalid_auth"})

    with patch("claude_slack_workflow_bot.WebClient", return_value=mock_slack_client):
        with pytest.raises(RuntimeError, match="Slack API error: invalid_auth"):
            create_slack_workflow(slack_token, trigger_channel, prompt)