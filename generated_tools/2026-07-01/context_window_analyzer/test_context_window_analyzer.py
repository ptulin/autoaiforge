import pytest
from unittest.mock import patch, mock_open, MagicMock
from context_window_analyzer import analyze_tokens, process_input_file

def mock_get_encoding(encoding_name):
    class MockTokenizer:
        def encode(self, text):
            return text.split()  # Simple tokenization by splitting on spaces

    return MockTokenizer()

def test_analyze_tokens():
    tokenizer = mock_get_encoding("cl100k_base")
    input_data = ["This is a test.", "Another test with more tokens."]
    token_counts, inefficiencies = analyze_tokens(input_data, tokenizer)

    assert len(token_counts) == 2
    assert token_counts == [4, 5]  # 4 tokens in first, 5 in second
    assert len(inefficiencies) == 0  # No inefficiencies in this case

def test_process_input_file_json():
    mock_json = '["This is a test.", "Another test."]'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            data = process_input_file("test.json")
            assert data == ["This is a test.", "Another test."]

def test_process_input_file_text():
    mock_text = "This is a test.\nAnother test."
    with patch("builtins.open", mock_open(read_data=mock_text)):
        with patch("os.path.exists", return_value=True):
            data = process_input_file("test.txt")
            assert data == ["This is a test.", "Another test."]

def test_process_input_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            process_input_file("nonexistent.txt")

def test_process_input_file_invalid_json():
    mock_json = '{"key": "value"}'  # Not a list
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("os.path.exists", return_value=True):
            with pytest.raises(ValueError):
                process_input_file("test.json")