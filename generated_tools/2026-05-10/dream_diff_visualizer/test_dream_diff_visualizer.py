import pytest
from unittest.mock import patch, mock_open
from dream_diff_visualizer import load_file, generate_diff, generate_html_diff

def test_load_file():
    mock_content = "This is a test file.\nWith multiple lines."
    with patch("builtins.open", mock_open(read_data=mock_content)):
        content = load_file("mock_file.txt")
        assert content == mock_content

def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_file("non_existent_file.txt")

def test_generate_diff():
    content1 = "Line 1\nLine 2\nLine 3"
    content2 = "Line 1\nLine 2 changed\nLine 3"
    diff_html = generate_diff(content1, content2)
    assert "Line&nbsp;2&nbsp;changed" in diff_html
    assert "Line&nbsp;2" in diff_html

def test_generate_html_diff():
    content1 = "Line 1\nLine 2\nLine 3"
    content2 = "Line 1\nLine 2 changed\nLine 3"
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("dream_diff_visualizer.load_file", side_effect=[content1, content2]):
            generate_html_diff("file1.txt", "file2.txt", "output.html")
            mocked_file.assert_called_once_with("output.html", "w", encoding="utf-8")
            handle = mocked_file()
            written_content = handle.write.call_args[0][0]
            assert "Line&nbsp;2&nbsp;changed" in written_content
            assert "Line&nbsp;2" in written_content
