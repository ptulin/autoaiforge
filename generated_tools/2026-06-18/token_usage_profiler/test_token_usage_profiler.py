import pytest
from unittest.mock import patch, mock_open
from token_usage_profiler import analyze_prompt, generate_report

@patch("os.path.exists", return_value=True)
def test_analyze_prompt_valid_file(mock_exists):
    mock_content = "This is a test prompt. This is a test prompt."
    with patch("builtins.open", mock_open(read_data=mock_content)):
        with patch("tiktoken.get_encoding") as mock_get_encoding:
            mock_encoder = mock_get_encoding.return_value
            mock_encoder.encode.return_value = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
            analysis = analyze_prompt("mock_file.txt")
            assert analysis["total_tokens"] == 10
            assert len(analysis["high_frequency_tokens"]) > 0
            assert "Consider reducing the length of the prompt to decrease token usage." not in analysis["suggestions"]
            assert "High-frequency tokens detected. Consider rephrasing to reduce repetition." in analysis["suggestions"]

@patch("os.path.exists", return_value=True)
def test_analyze_prompt_empty_file(mock_exists):
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(ValueError, match="The input file is empty."):
            analyze_prompt("mock_file.txt")

def test_analyze_prompt_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="File not found: non_existent_file.txt"):
            analyze_prompt("non_existent_file.txt")

def test_generate_report():
    analysis = {
        "total_tokens": 10,
        "high_frequency_tokens": [(123, 5), (456, 3)],
        "suggestions": ["Consider reducing the length of the prompt to decrease token usage."]
    }
    report = generate_report(analysis)
    assert "Total Tokens" in report
    assert "123" in report
    assert "Consider reducing the length of the prompt to decrease token usage." in report
