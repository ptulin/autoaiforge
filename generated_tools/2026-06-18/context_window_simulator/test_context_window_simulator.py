import pytest
from unittest.mock import patch, mock_open
from context_window_simulator import simulate_context_window, main
from rich.text import Text
import argparse

def test_simulate_context_window_retains_within_limit():
    prompt = "This is a test prompt."
    window_size = 10  # Arbitrary large number to ensure no truncation

    result = simulate_context_window(prompt, window_size)

    assert isinstance(result, Text)
    assert "[TRUNCATED]" not in result.plain

def test_simulate_context_window_truncates():
    prompt = "This is a test prompt that will be truncated."
    window_size = 5  # Small window size to force truncation

    result = simulate_context_window(prompt, window_size)

    assert isinstance(result, Text)
    assert "[TRUNCATED]" in result.plain

def test_main_handles_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("builtins.print") as mock_print:
            with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(input="nonexistent.txt", window=10)):
                main()
                mock_print.assert_any_call("Error: File 'nonexistent.txt' not found.")

def test_main_handles_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        with patch("builtins.print") as mock_print:
            with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(input="empty.txt", window=10)):
                main()
                mock_print.assert_any_call("Error: The input file is empty.")

def test_main_valid_input():
    prompt = "This is a valid prompt."
    with patch("builtins.open", mock_open(read_data=prompt)):
        with patch("rich.console.Console.print") as mock_print:
            with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(input="valid.txt", window=10)):
                main()
                assert mock_print.call_count == 1
