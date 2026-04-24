import pytest
from unittest.mock import patch, MagicMock
from claude_apify_connector import ClaudeApifyConnector

@pytest.fixture
def mock_apify_client():
    with patch("claude_apify_connector.ApifyClient") as MockApifyClient:
        mock_instance = MockApifyClient.return_value
        mock_instance.actor.return_value.call.return_value = {"defaultDatasetId": "test-dataset-id"}
        mock_instance.dataset.return_value.list_items.return_value.items = [{"key": "value"}]
        yield MockApifyClient

@pytest.fixture
def mock_requests_post():
    with patch("claude_apify_connector.requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"choices": [{"text": "Processed data"}]}
        mock_post.return_value.raise_for_status = MagicMock()
        yield mock_post

def test_fetch_apify_data_with_actor_id(mock_apify_client):
    connector = ClaudeApifyConnector("fake_apify_key", "fake_openai_key")
    data = connector.fetch_apify_data(actor_id="test-actor-id")

    assert data == [{"key": "value"}]
    mock_apify_client.return_value.actor.assert_called_once_with("test-actor-id")
    mock_apify_client.return_value.dataset.assert_called_once_with("test-dataset-id")

def test_fetch_apify_data_with_dataset_id(mock_apify_client):
    connector = ClaudeApifyConnector("fake_apify_key", "fake_openai_key")
    data = connector.fetch_apify_data(dataset_id="test-dataset-id")

    assert data == [{"key": "value"}]
    mock_apify_client.return_value.dataset.assert_called_once_with("test-dataset-id")

def test_send_to_claude(mock_requests_post):
    connector = ClaudeApifyConnector("fake_apify_key", "fake_openai_key")
    result = connector.send_to_claude([{"key": "value"}], "Summarize this data")

    assert result == "Processed data"
    mock_requests_post.assert_called_once()
