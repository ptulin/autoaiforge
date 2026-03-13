import pytest
from unittest.mock import patch, mock_open
from ai_code_suggester import get_code_suggestions, analyze_file

def test_get_code_suggestions():
    mock_response = {"choices": [{"text": "def example_function():\n    pass"}]}

    with patch("openai.Completion.create", return_value=mock_response):
        result = get_code_suggestions("fake_api_key", "def test():\n    pass")
        assert result == "def example_function():\n    pass"

def test_analyze_file_no_file():
    with patch("os.path.exists", return_value=False):
        with patch("rich.console.Console.print") as mock_print:
            analyze_file("nonexistent.py", "fake_api_key")
            mock_print.assert_called_with("[red]Error: File 'nonexistent.py' does not exist.[/red]")

def test_analyze_file_with_suggestions():
    mock_response = {"choices": [{"text": "def example_function():\n    pass"}]}

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="def test():\n    pass")) as mock_file:
            with patch("openai.Completion.create", return_value=mock_response):
                with patch("rich.console.Console.print") as mock_print:
                    analyze_file("test.py", "fake_api_key", inline=False)
                    mock_print.assert_any_call("[cyan]Code Suggestions:[/cyan]")

    mock_file.assert_called_with("test.py", "r")

def test_analyze_file_inline_suggestions():
    mock_response = {"choices": [{"text": "def example_function():\n    pass"}]}

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="def test():\n    pass")) as mock_file:
            with patch("openai.Completion.create", return_value=mock_response):
                with patch("rich.console.Console.print") as mock_print:
                    analyze_file("test.py", "fake_api_key", inline=True)

                    mock_file().write.assert_called_with("\n# Suggestions from Claude AI:\n# def example_function():\n#     pass")
                    mock_print.assert_any_call("[green]Suggestions added inline to 'test.py'.[/green]")
