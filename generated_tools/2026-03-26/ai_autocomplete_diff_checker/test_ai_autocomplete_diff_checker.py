import pytest
from unittest.mock import mock_open, patch
from ai_autocomplete_diff_checker import generate_diff

def test_generate_diff_success():
    original_content = "line1\nline2\nline3\n"
    suggested_content = "line1\nline2 modified\nline3\n"

    with patch("builtins.open", mock_open(read_data=original_content)) as mock_file:
        mock_file.side_effect = [
            mock_open(read_data=original_content).return_value,
            mock_open(read_data=suggested_content).return_value,
            mock_open().return_value
        ]

        diff = generate_diff("original.py", "suggested.py", "output.diff")

        assert "--- original.py" in diff
        assert "+++ suggested.py" in diff
        assert "-line2" in diff
        assert "+line2 modified" in diff

def test_generate_diff_file_not_found():
    with pytest.raises(FileNotFoundError):
        generate_diff("nonexistent_original.py", "nonexistent_suggested.py", "output.diff")

def test_generate_diff_empty_files():
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        mock_file.side_effect = [
            mock_open(read_data="").return_value,
            mock_open(read_data="").return_value,
            mock_open().return_value
        ]

        diff = generate_diff("empty_original.py", "empty_suggested.py", "output.diff")

        assert diff == ""