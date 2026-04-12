import pytest
from unittest.mock import patch, mock_open
from code_review_ai import analyze_code, process_file, process_directory

@patch('code_review_ai.openai.Completion.create')
def test_analyze_code(mock_openai):
    mock_openai.return_value = {
        'choices': [{'text': 'Mocked analysis report.'}]
    }
    result = analyze_code("print('Hello, world!')")
    assert result == "Mocked analysis report."

@patch('builtins.open', new_callable=mock_open, read_data="print('Hello, world!')")
@patch('code_review_ai.analyze_code', return_value="Mocked analysis report.")
def test_process_file(mock_analyze_code, mock_file):
    with patch('os.path.isfile', return_value=True):
        result = process_file("test_script.py")
        assert result == "Mocked analysis report."

@patch('code_review_ai.process_file', return_value="Mocked analysis report.")
def test_process_directory(mock_process_file):
    with patch('os.path.isdir', return_value=True):
        with patch('os.walk', return_value=[("/test", ("subdir",), ("file1.py", "file2.py"))]):
            result = process_directory("/test")
            assert len(result) == 2
            assert result["/test/file1.py"] == "Mocked analysis report."
            assert result["/test/file2.py"] == "Mocked analysis report."
