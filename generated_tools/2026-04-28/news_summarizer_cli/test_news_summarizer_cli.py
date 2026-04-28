import pytest
from unittest.mock import patch, Mock
from news_summarizer_cli import fetch_news, summarize_articles

def test_fetch_news():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"articles": [{"title": "Test Title", "description": "Test Description"}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        articles = fetch_news("fake_api_key", "technology", "us")
        assert len(articles) == 1
        assert articles[0]["title"] == "Test Title"

def test_summarize_articles():
    with patch("openai.Completion.create") as mock_openai:
        mock_response = Mock()
        mock_response.choices = [Mock(text="Summarized text.")]
        mock_openai.return_value = mock_response

        articles = [{"title": "Test Title", "description": "Test Description"}]
        summaries = summarize_articles(articles, 3, "fake_openai_key")
        assert len(summaries) == 1
        assert summaries[0] == "Summarized text."

def test_save_to_file(tmp_path):
    from news_summarizer_cli import save_to_file

    summaries = ["Summary 1", "Summary 2"]
    output_file = tmp_path / "summaries.txt"
    save_to_file(summaries, output_file)

    with open(output_file, "r") as f:
        content = f.read()
        assert "Summary 1" in content
        assert "Summary 2" in content
