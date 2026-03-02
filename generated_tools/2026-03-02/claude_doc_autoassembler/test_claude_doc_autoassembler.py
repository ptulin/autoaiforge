import pytest
from unittest.mock import patch, mock_open, MagicMock
from claude_doc_autoassembler import load_input_data, load_template, generate_content, refine_with_claude

def test_load_input_data_json():
    mock_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("pathlib.Path.exists", return_value=True):
            data = load_input_data("test.json")
            assert data == {"key": "value"}

def test_load_input_data_csv():
    mock_data = "key,value\nname,John"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("pathlib.Path.exists", return_value=True):
            data = load_input_data("test.csv")
            assert data == [{"key": "name", "value": "John"}]

def test_refine_with_claude():
    mock_response = {"completion": "Refined content"}
    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200, json=lambda: mock_response)
        result = refine_with_claude("Initial content", "fake_api_key")
        assert result == "Refined content"

def test_generate_content():
    template_str = "Hello {{ name }}!"
    with patch("builtins.open", mock_open(read_data=template_str)):
        with patch("pathlib.Path.exists", return_value=True):
            template = load_template("template.txt")
            content = generate_content(template, {"name": "John"})
            assert content == "Hello John!"