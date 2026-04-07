import pytest
from unittest.mock import patch, mock_open
from source_code_provenance_checker import read_source_code, fetch_public_repositories, compare_code_with_repositories

def test_read_source_code():
    mock_file_content = "print('Hello, World!')"
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        result = read_source_code("dummy_path.py")
        assert result == mock_file_content

def test_fetch_public_repositories():
    mock_response = [
        {"full_name": "repo1", "html_url": "https://github.com/repo1", "code_snippets": ["print('Hello, World!')"]}
    ]
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = lambda: None
        result = fetch_public_repositories()
        assert result == mock_response

def test_compare_code_with_repositories():
    source_code = "print('Hello, World!')"
    repositories = [
        {"full_name": "repo1", "html_url": "https://github.com/repo1", "code_snippets": ["print('Hello, World!')"]}
    ]

    matches = compare_code_with_repositories(source_code, repositories)
    assert len(matches) > 0
    assert matches[0]["repository"] == "repo1"
    assert matches[0]["snippet"] == "print('Hello, World!')"
    assert matches[0]["similarity"] == 1.0
