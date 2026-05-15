import pytest
from unittest.mock import patch, Mock
import os
import pandas as pd
import json
from claude_batch_automator import process_data

def test_process_data_csv(tmp_path):
    input_file = tmp_path / "test.csv"
    output_file = tmp_path / "output.csv"

    # Create a mock input CSV file
    input_file.write_text("text\nHello World\nPython Testing\n")

    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200, json=lambda: {"result": "processed"})

        process_data(str(input_file), "summarize", str(output_file))

    # Verify output
    assert output_file.exists()
    df = pd.read_csv(output_file)
    assert len(df) == 2
    assert "result" in df.columns

def test_process_data_json(tmp_path):
    input_file = tmp_path / "test.json"
    output_file = tmp_path / "output.json"

    # Create a mock input JSON file
    input_file.write_text(json.dumps([{"text": "Hello World"}, {"text": "Python Testing"}]))

    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200, json=lambda: {"result": "processed"})

        process_data(str(input_file), "summarize", str(output_file))

    # Verify output
    assert output_file.exists()
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert len(data) == 2
    assert "result" in data[0]

def test_process_data_txt(tmp_path):
    input_file = tmp_path / "test.txt"
    output_file = tmp_path / "output.txt"

    # Create a mock input TXT file
    input_file.write_text("Hello World\nPython Testing\n")

    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200, json=lambda: {"result": "processed"})

        process_data(str(input_file), "summarize", str(output_file))

    # Verify output
    assert output_file.exists()
    with open(output_file, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2
    assert "result" in json.loads(lines[0])