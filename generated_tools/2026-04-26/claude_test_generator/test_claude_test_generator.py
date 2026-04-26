import pytest
from unittest.mock import patch, MagicMock
from claude_test_generator import generate_tests_with_claude
import openai

def test_generate_tests_with_claude_success():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="def test_example():\n    assert True")]

    with patch('openai.Completion.create', return_value=mock_response):
        result = generate_tests_with_claude("fake-api-key", "def example(): pass")
        assert "def test_example()" in result

def test_generate_tests_with_claude_api_error():
    with patch('openai.Completion.create', side_effect=openai.error.OpenAIError("API Error")):
        with pytest.raises(RuntimeError, match="Error communicating with Claude AI: API Error"):
            generate_tests_with_claude("fake-api-key", "def example(): pass")

def test_main_cli(tmp_path):
    input_code = "def example():\n    return 42"
    input_file = tmp_path / "example.py"
    output_file = tmp_path / "test_example.py"

    input_file.write_text(input_code)

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="def test_example():\n    assert example() == 42")]

    with patch('openai.Completion.create', return_value=mock_response):
        from click.testing import CliRunner
        from claude_test_generator import main

        runner = CliRunner()
        result = runner.invoke(main, ["--input", str(input_file), "--output", str(output_file), "--api-key", "fake-api-key"])

        assert result.exit_code == 0
        assert output_file.read_text() == "def test_example():\n    assert example() == 42"
        assert "Test cases generated and saved to" in result.output
