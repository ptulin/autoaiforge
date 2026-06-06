import pytest
import json
from unittest.mock import patch, mock_open
from ai_code_linter import analyze_code, load_config, process_file
from rich.console import Console

def test_analyze_code():
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': json.dumps([
                        {"line": 1, "issue": "Unused import", "recommendation": "Remove the unused import."}
                    ])
                }
            }
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        result = analyze_code("import os", {})
        assert len(result) == 1
        assert result[0]['issue'] == "Unused import"

def test_load_config():
    mock_config = '{"rule": "no-unused-vars"}'
    with patch("builtins.open", mock_open(read_data=mock_config)):
        with patch("os.path.exists", return_value=True):
            config = load_config("config.json")
            assert config["rule"] == "no-unused-vars"

def test_process_file():
    mock_file_content = "import os\nprint('Hello, World!')"
    mock_response = {
        'choices': [
            {
                'message': {
                    'content': json.dumps([
                        {"line": 1, "issue": "Unused import", "recommendation": "Remove the unused import."}
                    ])
                }
            }
        ]
    }

    console = Console()

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.exists", return_value=True):
            with patch('openai.ChatCompletion.create', return_value=mock_response):
                process_file("test.py", {}, console)
