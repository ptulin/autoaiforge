import os
import pytest
from unittest.mock import patch, mock_open
from batch_text_summarizer import summarize_text, process_files

def test_summarize_text():
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = {"choices": [{"text": "This is a summary."}]}
        result = summarize_text("fake_api_key", "This is a test text.")
        assert result == "This is a summary."

def test_process_files(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    file_path = input_dir / "test.txt"
    file_path.write_text("This is a test text.")

    with patch("batch_text_summarizer.summarize_text", return_value="This is a summary."):
        process_files(str(input_dir), str(output_dir), "fake_api_key", 100)

    output_file = output_dir / "summary_test.txt"
    assert output_file.exists()
    assert output_file.read_text() == "This is a summary."

def test_process_files_empty_file(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    file_path = input_dir / "empty.txt"
    file_path.write_text("")

    with patch("batch_text_summarizer.summarize_text") as mock_summarize:
        process_files(str(input_dir), str(output_dir), "fake_api_key", 100)
        mock_summarize.assert_not_called()

    output_file = output_dir / "summary_empty.txt"
    assert not output_file.exists()