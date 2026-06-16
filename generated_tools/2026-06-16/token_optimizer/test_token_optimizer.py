import pytest
from unittest.mock import patch, mock_open
from token_optimizer import analyze_token_usage, process_file, MockEncoding

def mock_word_tokenize(text):
    """Mock implementation of nltk.tokenize.word_tokenize."""
    return text.split()

@patch("token_optimizer.word_tokenize", side_effect=mock_word_tokenize)
def test_analyze_token_usage(mock_word_tokenize):
    encoding = MockEncoding()
    text = "This is a test sentence."
    result = analyze_token_usage(text, encoding)
    assert result['original_text'] == text
    assert result['token_count'] == len(text)  # Each character is a token in MockEncoding
    assert isinstance(result['suggestions'], list)

@patch("token_optimizer.word_tokenize", side_effect=mock_word_tokenize)
def test_process_file(mock_word_tokenize):
    encoding = MockEncoding()
    mock_file_content = "Line one\nLine two\n"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        results = process_file("dummy_path.txt", encoding)
        assert len(results) == 2
        assert results[0]['original_text'] == "Line one"
        assert results[1]['original_text'] == "Line two"

@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_open):
    encoding = MockEncoding()
    results = process_file("non_existent_file.txt", encoding)
    assert results == []