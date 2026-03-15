import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from ai_news_trend_analyzer import analyze_trends

def test_analyze_trends_valid_input():
    # Mock input data
    data = pd.DataFrame({
        'timestamp': ['2023-10-01', '2023-10-01', '2023-10-02'],
        'content': ['AI is great', 'GPT is amazing', 'AI ethics are important']
    })

    with patch('pandas.read_csv', return_value=data):
        results = analyze_trends('mock.csv', ['AI', 'GPT'])

    assert 'AI' in results
    assert 'GPT' in results
    assert len(results['AI']) == 2
    assert len(results['GPT']) == 1

def test_analyze_trends_missing_columns():
    # Mock input data with missing columns
    data = pd.DataFrame({
        'time': ['2023-10-01'],
        'text': ['AI is great']
    })

    with patch('pandas.read_csv', return_value=data):
        with pytest.raises(ValueError, match="Input file must contain 'timestamp' and 'content' columns."):
            analyze_trends('mock.csv', ['AI'])

def test_analyze_trends_empty_file():
    # Mock empty input data
    data = pd.DataFrame(columns=['timestamp', 'content'])

    with patch('pandas.read_csv', return_value=data):
        results = analyze_trends('mock.csv', ['AI'])

    assert 'AI' in results
    assert results['AI'].empty
