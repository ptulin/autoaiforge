import pytest
from unittest.mock import patch, mock_open
from ai_trend_analyzer import load_input, extract_keywords, analyze_sentiment

def test_load_input_file():
    mock_data = '["AI is transforming the world.", "Machine learning is a subset of AI."]'
    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        with patch("os.path.exists", return_value=True):
            result = load_input("mock_file.json")
            assert result == ["AI is transforming the world.", "Machine learning is a subset of AI."]

def test_load_input_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_input("nonexistent_file.json")

def test_extract_keywords():
    articles = ["AI is transforming the world.", "Machine learning is a subset of AI."]
    with patch("spacy.load") as mock_spacy:
        mock_nlp = mock_spacy.return_value
        mock_doc = type("MockDoc", (object,), {
            "lemma_": "ai", "is_alpha": True, "is_stop": False
        })
        mock_nlp.return_value = [mock_doc, mock_doc]
        result = extract_keywords(articles)
        assert result["ai"] > 0

def test_analyze_sentiment():
    articles = ["AI is amazing!", "AI is scary."]
    with patch("nltk.sentiment.SentimentIntensityAnalyzer.polarity_scores", side_effect=[
        {"pos": 0.8, "neu": 0.2, "neg": 0.0},
        {"pos": 0.1, "neu": 0.3, "neg": 0.6},
    ]):
        result = analyze_sentiment(articles)
        assert result["positive"] == pytest.approx(0.45, 0.01)
        assert result["neutral"] == pytest.approx(0.25, 0.01)
        assert result["negative"] == pytest.approx(0.30, 0.01)