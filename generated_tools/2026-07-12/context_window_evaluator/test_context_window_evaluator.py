import pytest
from unittest.mock import patch, mock_open
import tiktoken
from context_window_evaluator import analyze_prompt, analyze_file, generate_report
import json

def test_analyze_prompt():
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokenizer.max_token_count = 10
    prompt = "This is a test prompt."

    result = analyze_prompt(prompt, tokenizer)

    assert result["token_count"] > 0
    assert result["unique_tokens"] > 0
    assert 0 <= result["redundancy"] <= 1
    assert result["truncation_risk"] == False

def test_analyze_file():
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokenizer.max_token_count = 10
    file_content = "This is a test prompt.\nAnother test prompt."

    with patch("builtins.open", mock_open(read_data=file_content)):
        results = analyze_file("test.txt", tokenizer)

    assert len(results) == 2
    assert results[0]["token_count"] > 0
    assert results[1]["token_count"] > 0

def test_generate_report():
    analysis_results = [
        {"token_count": 5, "unique_tokens": 4, "redundancy": 0.2, "truncation_risk": False},
        {"token_count": 10, "unique_tokens": 8, "redundancy": 0.2, "truncation_risk": True}
    ]

    with patch("builtins.open", mock_open()) as mocked_file:
        generate_report(analysis_results, "output.json")

        mocked_file.assert_called_once_with("output.json", "w", encoding="utf-8")
        written_data = "".join(call.args[0] for call in mocked_file().write.call_args_list)
        written_data = json.loads(written_data)

        assert len(written_data) == 2
        assert written_data[0]["token_count"] == 5
        assert written_data[1]["truncation_risk"] == True