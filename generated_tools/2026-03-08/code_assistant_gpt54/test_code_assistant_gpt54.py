import pytest
from unittest.mock import patch, mock_open
import os
from code_assistant_gpt54 import analyze_codebase

def test_invalid_directory():
    with pytest.raises(ValueError):
        analyze_codebase("invalid_path", "fake_api_key")

@patch("os.path.isdir", return_value=True)
@patch("os.walk", return_value=[("/fake_dir", [], ["test.py"]), ("/fake_dir/subdir", [], ["sub_test.py"])] )
@patch("builtins.open", new_callable=mock_open, read_data="print('Hello World')")
@patch("openai.Completion.create")
def test_analyze_codebase(mock_openai, mock_open, mock_os_walk, mock_os_isdir):
    mock_openai.return_value = type('obj', (object,), {"choices": [{"text": "# Suggested improvements\n# Add error handling."}]})

    analyze_codebase("/fake_dir", "fake_api_key")

    mock_openai.assert_called()
    mock_open.assert_called()

def test_empty_directory():
    with patch("os.path.isdir", return_value=True), patch("os.walk", return_value=[]):
        analyze_codebase("/empty_dir", "fake_api_key")