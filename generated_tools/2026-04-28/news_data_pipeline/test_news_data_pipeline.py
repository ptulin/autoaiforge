import pytest
from unittest.mock import patch, MagicMock
from news_data_pipeline import NewsPipeline

@pytest.fixture
def mock_pipeline():
    pipeline = NewsPipeline(api_keys={"newsapi": "test_api_key"})
    pipeline.summarizer = MagicMock(return_value=[{"summary_text": "Short summary"}])
    return pipeline

@patch("news_data_pipeline.requests.get")
def test_fetch_news(mock_get, mock_pipeline):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "articles": [
            {"title": "Test Article", "description": "Test Description", "content": "Test Content", "url": "http://example.com", "publishedAt": "2023-01-01"}
        ]
    }

    articles = mock_pipeline.fetch_news(topic="AI")
    assert len(articles) == 1
    assert articles[0]["title"] == "Test Article"

def test_summarize(mock_pipeline):
    summary = mock_pipeline.summarize("Long content here.")
    assert summary == "Short summary"

def test_clean_data(mock_pipeline):
    raw_articles = [
        {"title": "Test Article", "description": "Test Description", "content": "Test Content", "url": "http://example.com", "publishedAt": "2023-01-01"}
    ]
    cleaned_data = mock_pipeline.clean_data(raw_articles)
    assert not cleaned_data.empty
    assert cleaned_data.iloc[0]["title"] == "Test Article"

@patch("news_data_pipeline.requests.get")
def test_fetch_and_summarize(mock_get, mock_pipeline):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "articles": [
            {"title": "Test Article", "description": "Test Description", "content": "Test Content", "url": "http://example.com", "publishedAt": "2023-01-01"}
        ]
    }
    result = mock_pipeline.fetch_and_summarize(topic="AI")
    assert len(result) == 1
    assert "summary" in result[0]
    assert result[0]["summary"] == "Short summary"