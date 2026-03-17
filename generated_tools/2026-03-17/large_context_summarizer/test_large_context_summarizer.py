import pytest
from unittest.mock import patch, MagicMock
from large_context_summarizer import recursive_summarize, load_input_file, save_output_file

def test_recursive_summarize():
    with patch("openai.ChatCompletion.create") as mock_openai:
        mock_openai.return_value = {"choices": [{"message": {"content": "Summary of chunk"}}]}

        text = "This is a test text that needs summarization. " * 50
        result = recursive_summarize(text, depth=2, granularity=5)

        assert "Summary of chunk" in result
        assert mock_openai.call_count > 0

def test_load_input_file_txt(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("This is a test file.")

    result = load_input_file(str(test_file))
    assert result == "This is a test file."

def test_load_input_file_json(tmp_path):
    test_file = tmp_path / "test.json"
    test_file.write_text('{"key": "value"}')

    result = load_input_file(str(test_file))
    assert result == '{"key": "value"}'

def test_save_output_file_txt(tmp_path):
    test_file = tmp_path / "output.txt"
    save_output_file("Test output", str(test_file))

    assert test_file.read_text() == "Test output"

def test_save_output_file_json(tmp_path):
    test_file = tmp_path / "output.json"
    save_output_file({"key": "value"}, str(test_file))

    assert test_file.read_text() == '{\n    "key": "value"\n}'