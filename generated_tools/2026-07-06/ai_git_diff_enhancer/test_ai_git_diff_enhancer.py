import pytest
from unittest.mock import patch, MagicMock
from ai_git_diff_enhancer import generate_ai_explanation, get_git_diff

def test_generate_ai_explanation():
    mock_response = MagicMock()
    mock_response.__getitem__.return_value = [{'text': 'This is a mock explanation.'}]
    with patch('openai.Completion.create', return_value=mock_response):
        explanation = generate_ai_explanation("mock diff")
        assert explanation == "This is a mock explanation."

def test_get_git_diff_from_file(tmp_path):
    diff_file = tmp_path / "diff.txt"
    diff_file.write_text("mock diff content")

    diff_text = get_git_diff(diff_file=str(diff_file))
    assert diff_text == "mock diff content"

def test_get_git_diff_file_not_found():
    with pytest.raises(FileNotFoundError):
        get_git_diff(diff_file="non_existent_file.txt")

def test_get_git_diff_invalid_input():
    diff_text = get_git_diff()
    assert diff_text.startswith("Error")
