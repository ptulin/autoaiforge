import pytest
from unittest.mock import patch, mock_open
from zero_day_diff_checker import analyze_diff

def test_analyze_diff_json():
    with patch("os.path.exists", return_value=True), \
         patch("os.walk", return_value=[("/old_version", [], ["file1.py"])]), \
         patch("builtins.open", mock_open(read_data="print('Hello')")):

        result = analyze_diff("/old_version", "/new_version", "json")
        assert "file1.py" in result
        assert "SAFE" in result

def test_analyze_diff_text():
    with patch("os.path.exists", return_value=True), \
         patch("os.walk", return_value=[("/old_version", [], ["file1.py"])]), \
         patch("builtins.open", mock_open(read_data="print('Hello')")):

        result = analyze_diff("/old_version", "/new_version", "text")
        assert "file1.py" in result
        assert "SAFE" in result

def test_analyze_diff_missing_path():
    with patch("os.path.exists", side_effect=lambda x: x == "/old_version"):
        with pytest.raises(FileNotFoundError):
            analyze_diff("/old_version", "/new_version")