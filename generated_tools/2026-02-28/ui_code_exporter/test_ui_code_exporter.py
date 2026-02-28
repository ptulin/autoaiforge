import pytest
from unittest.mock import patch, mock_open
import os
from ui_code_exporter import parse_design_file, generate_code_with_ai, save_code

def test_parse_design_file_json():
    mock_json = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        result = parse_design_file("design.json")
        assert result == {"key": "value"}

def test_parse_design_file_svg():
    mock_svg = "<svg></svg>"
    with patch("builtins.open", mock_open(read_data=mock_svg)):
        result = parse_design_file("design.svg")
        assert result == "<svg></svg>"

def test_generate_code_with_ai():
    mock_response = {"choices": [{"text": "<div>Hello World</div>"}]}
    with patch("openai.Completion.create", return_value=mock_response):
        result = generate_code_with_ai("mock design data", "react")
        assert result == "<div>Hello World</div>"

def test_save_code():
    mock_code = "<div>Hello World</div>"
    output_dir = "test_output"
    framework = "react"
    with patch("os.makedirs") as mock_makedirs, patch("builtins.open", mock_open()) as mock_file:
        save_code(output_dir, mock_code, framework)
        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_file.assert_called_once_with(os.path.join(output_dir, "Component.jsx"), 'w')
        mock_file().write.assert_called_once_with(mock_code)