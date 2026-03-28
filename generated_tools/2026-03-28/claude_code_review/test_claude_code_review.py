import pytest
from unittest.mock import patch, mock_open
from claude_code_review import perform_code_review, display_feedback
import requests

def test_perform_code_review_success():
    mock_response = {
        "issues": [
            {"issue": "Unused variable.", "suggestion": "Remove unused variable."},
            {"issue": "Function too complex.", "suggestion": "Refactor to simplify."}
        ]
    }

    with patch("builtins.open", mock_open(read_data="print('Hello, World!')")) as mock_file:
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = mock_response

            feedback = perform_code_review("test.py", "fake_api_key")
            assert feedback == mock_response
            mock_file.assert_called_once_with("test.py", "r")

def test_perform_code_review_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        feedback = perform_code_review("nonexistent.py", "fake_api_key")
        assert feedback == {"error": "File not found. Please provide a valid file path."}

def test_perform_code_review_network_error():
    with patch("builtins.open", mock_open(read_data="print('Hello, World!')")):
        with patch("requests.post", side_effect=requests.exceptions.RequestException("Network error")):
            feedback = perform_code_review("test.py", "fake_api_key")
            assert feedback == {"error": "Network error: Network error"}

def test_display_feedback_error():
    feedback = {"error": "An error occurred."}

    with patch("rich.console.Console.print") as mock_print:
        display_feedback(feedback)
        mock_print.assert_called_with("[bold red]Error:[/bold red] An error occurred.")

def test_display_feedback_success():
    feedback = {
        "issues": [
            {"issue": "Unused variable.", "suggestion": "Remove unused variable."},
            {"issue": "Function too complex.", "suggestion": "Refactor to simplify."}
        ]
    }

    with patch("rich.console.Console.print") as mock_print:
        display_feedback(feedback)
        assert mock_print.call_count == 1
