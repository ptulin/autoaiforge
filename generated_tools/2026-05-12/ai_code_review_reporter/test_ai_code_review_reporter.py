import pytest
from unittest.mock import patch, mock_open
from ai_code_review_reporter import fetch_ai_review, generate_report, main
import argparse
import sys

def test_fetch_ai_review():
    mock_response = {
        'choices': [
            {'message': {'content': 'This is a mock review feedback.'}}
        ]
    }

    with patch('openai.ChatCompletion.create', return_value=mock_response):
        feedback = fetch_ai_review("print('Hello, world!')", "fake_api_key")
        assert feedback == 'This is a mock review feedback.'

def test_generate_report_markdown():
    feedback = "This is a test feedback."
    report = generate_report(feedback, 'markdown')
    assert "# AI Code Review Report" in report
    assert feedback in report

def test_generate_report_html():
    feedback = "This is a test feedback."
    report = generate_report(feedback, 'html')
    assert "<h1>AI Code Review Report</h1>" in report
    assert feedback in report

def test_main_file_not_found():
    with patch('builtins.print') as mock_print:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(file='nonexistent.py', output='report.md', format='markdown', api_key='fake_api_key')):
            with patch('os.path.isfile', return_value=False):
                with pytest.raises(SystemExit) as excinfo:
                    main()
                assert excinfo.value.code == 1
                mock_print.assert_called_with("Error: File nonexistent.py does not exist.", file=sys.stderr)

def test_main_empty_file():
    with patch('builtins.print') as mock_print:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(file='empty.py', output='report.md', format='markdown', api_key='fake_api_key')):
            with patch('os.path.isfile', return_value=True):
                with patch('builtins.open', mock_open(read_data="")):
                    with pytest.raises(SystemExit) as excinfo:
                        main()
                    assert excinfo.value.code == 1
                    mock_print.assert_called_with("Error: The file is empty.", file=sys.stderr)
