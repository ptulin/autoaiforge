import pytest
import json
from unittest.mock import patch, mock_open
from decision_diff_checker import load_json_file, generate_diff, display_diff
from rich.console import Console
from rich.text import Text

def test_load_json_file():
    mock_data = {"key": "value"}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = load_json_file("mock_file.json")
        assert result == mock_data

def test_load_json_file_not_found():
    with pytest.raises(ValueError, match="File not found: missing_file.json"):
        load_json_file("missing_file.json")

def test_load_json_file_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(ValueError, match="Invalid JSON format in file: invalid_file.json"):
            load_json_file("invalid_file.json")

def test_generate_diff():
    old_data = {"key1": "value1", "key2": "value2"}
    new_data = {"key1": "value1", "key2": "value3"}
    diff = generate_diff(old_data, new_data)
    diff_text = "\n".join(diff)
    assert "-    \"key2\": \"value2\"" in diff_text
    assert "+    \"key2\": \"value3\"" in diff_text

def test_display_diff():
    diff = ["- old line", "+ new line", " unchanged line"]
    console = Console()
    with patch.object(console, "print") as mock_print:
        with patch("decision_diff_checker.Console", return_value=console):
            display_diff(diff)
            mock_print.assert_any_call(Text("- old line", style="red"))
            mock_print.assert_any_call(Text("+ new line", style="green"))
            mock_print.assert_any_call(Text(" unchanged line"))
