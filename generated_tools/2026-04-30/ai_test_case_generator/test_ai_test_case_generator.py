import pytest
from unittest.mock import patch, mock_open
from ai_test_case_generator import generate_test_cases

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [
            {
                "text": """def test_sample():
    assert 1 + 1 == 2"""
            }
        ]
    }

def test_generate_test_cases_file_not_found():
    with pytest.raises(FileNotFoundError):
        generate_test_cases("fake_api_key", "non_existent_file.py")

@patch("builtins.open", new_callable=mock_open, read_data="def sample_function():\n    return 42")
@patch("os.path.exists", return_value=True)
@patch("openai.Completion.create")
def test_generate_test_cases_success(mock_openai, mock_exists, mock_file, mock_openai_response):
    mock_openai.return_value = mock_openai_response
    result = generate_test_cases("fake_api_key", "sample.py")
    assert "def test_sample()" in result
    assert "assert 1 + 1 == 2" in result

@patch("builtins.open", new_callable=mock_open, read_data="def sample_function():\n    return 42")
@patch("os.path.exists", return_value=True)
@patch("openai.Completion.create", side_effect=Exception("API Error"))
def test_generate_test_cases_api_error(mock_openai, mock_exists, mock_file):
    with pytest.raises(RuntimeError, match="Failed to generate test cases: API Error"):
        generate_test_cases("fake_api_key", "sample.py")
