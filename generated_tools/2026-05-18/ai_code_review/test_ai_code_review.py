import pytest
from unittest.mock import patch, MagicMock
from ai_code_review import analyze_code, read_code_from_file

def test_analyze_code_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="This is a test feedback.")]

    with patch('openai.Completion.create', return_value=mock_response):
        feedback = analyze_code("fake_api_key", "print('Hello, world!')")
        assert feedback == "This is a test feedback."

def test_analyze_code_error():
    with patch('openai.Completion.create', side_effect=Exception("API error")):
        feedback = analyze_code("fake_api_key", "print('Hello, world!')")
        assert feedback == "Error during analysis: API error"

def test_read_code_from_file(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("print('Hello, world!')")

    content = read_code_from_file(str(test_file))
    assert content == "print('Hello, world!')"

def test_read_code_from_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_code_from_file("non_existent_file.py")