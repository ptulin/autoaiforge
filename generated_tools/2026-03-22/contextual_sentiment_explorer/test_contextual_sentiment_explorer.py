import pytest
from unittest.mock import patch, MagicMock
from contextual_sentiment_explorer import analyze_sentiment, display_results

def test_analyze_sentiment():
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = [{'label': 'POSITIVE', 'score': 0.98}]

    with patch('contextual_sentiment_explorer.pipeline', return_value=mock_pipeline):
        with patch('contextual_sentiment_explorer.nltk.download') as mock_nltk_download:
            with patch('contextual_sentiment_explorer.sent_tokenize', return_value=["This is a great day."]):
                text = "This is a great day."
                results = analyze_sentiment(text)

    assert len(results) == 1
    assert results[0]['label'] == 'POSITIVE'
    assert results[0]['score'] == 0.98
    mock_nltk_download.assert_called_once_with('punkt', quiet=True)

def test_analyze_sentiment_multiple_sentences():
    mock_pipeline = MagicMock()
    mock_pipeline.side_effect = [
        [{'label': 'POSITIVE', 'score': 0.95}],
        [{'label': 'NEGATIVE', 'score': 0.85}]
    ]

    with patch('contextual_sentiment_explorer.pipeline', return_value=mock_pipeline):
        with patch('contextual_sentiment_explorer.nltk.download') as mock_nltk_download:
            with patch('contextual_sentiment_explorer.sent_tokenize', return_value=["I love this.", "But I hate that."]):
                text = "I love this. But I hate that."
                results = analyze_sentiment(text)

    assert len(results) == 2
    assert results[0]['label'] == 'POSITIVE'
    assert results[1]['label'] == 'NEGATIVE'
    mock_nltk_download.assert_called_once_with('punkt', quiet=True)

def test_display_results():
    results = [
        {"sentence": "I love this.", "label": "POSITIVE", "score": 0.95},
        {"sentence": "I hate that.", "label": "NEGATIVE", "score": 0.85}
    ]

    with patch('contextual_sentiment_explorer.Console') as mock_console:
        mock_table = MagicMock()
        mock_console.return_value = MagicMock()
        mock_console.return_value.print = MagicMock()

        display_results(results)

        assert mock_console.return_value.print.called
        assert mock_console.return_value.print.call_count == 1
