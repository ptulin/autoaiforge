import pytest
import requests
from unittest.mock import patch
from semantic_search_explorer import perform_search, display_results

def test_perform_search_success():
    mock_response = {
        "results": [
            {"title": "Result 1", "source": "Source 1", "relevance_score": 0.95},
            {"title": "Result 2", "source": "Source 2", "relevance_score": 0.89},
        ]
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        results = perform_search("test query", "fake_api_key", "https://api.example.com/search")
        assert len(results) == 2
        assert results[0]["title"] == "Result 1"
        assert results[1]["source"] == "Source 2"

def test_perform_search_failure():
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("API Error")

        with pytest.raises(RuntimeError, match="Failed to perform search: API Error"):
            perform_search("test query", "fake_api_key", "https://api.example.com/search")

def test_display_results(capsys):
    results = [
        {"title": "Result 1", "source": "Source 1", "relevance_score": 0.95},
        {"title": "Result 2", "source": "Source 2", "relevance_score": 0.89},
    ]

    display_results(results)

    captured = capsys.readouterr()
    assert "Semantic Search Results" in captured.out
    assert "Result 1" in captured.out
    assert "Source 2" in captured.out