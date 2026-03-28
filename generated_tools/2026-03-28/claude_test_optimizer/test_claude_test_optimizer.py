import pytest
from unittest.mock import patch, mock_open
from claude_test_optimizer import fetch_optimized_tests, read_file, write_file
import requests

def test_fetch_optimized_tests_success():
    mock_response = {"optimized_tests": "def test_example():\n    assert True"}
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response

        result = fetch_optimized_tests("fake_api_key", "def example(): pass")
        assert result == "def test_example():\n    assert True"

def test_fetch_optimized_tests_failure():
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("API error")

        with pytest.raises(RuntimeError, match="Failed to fetch optimized tests: API error"):
            fetch_optimized_tests("fake_api_key", "def example(): pass")

def test_read_file():
    mock_file_content = "def example(): pass"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("os.path.exists", return_value=True):
            result = read_file("fake_path.py")
            assert result == mock_file_content

def test_read_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="File not found: fake_path.py"):
            read_file("fake_path.py")

def test_write_file():
    with patch("builtins.open", mock_open()) as mock_file:
        write_file("fake_output.py", "def test_example():\n    assert True")
        mock_file.assert_called_once_with("fake_output.py", "w")
        mock_file().write.assert_called_once_with("def test_example():\n    assert True")