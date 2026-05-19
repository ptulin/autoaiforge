import pytest
from unittest.mock import patch, mock_open
from agent_code_review import analyze_code, process_file, process_folder

@patch('openai.ChatCompletion.create')
def test_analyze_code(mock_openai):
    mock_openai.return_value = {
        'choices': [{'message': {'content': 'Mocked review comment'}}]
    }
    result = analyze_code("print('Hello, world!')", "fake_api_key")
    assert result == 'Mocked review comment'

@patch('builtins.open', new_callable=mock_open, read_data="print('Hello, world!')")
@patch('os.path.exists', return_value=True)
@patch('agent_code_review.analyze_code', return_value='Mocked review comment')
def test_process_file(mock_analyze_code, mock_exists, mock_file):
    result = process_file("test.py", "fake_api_key")
    assert result == 'Mocked review comment'

@patch('agent_code_review.process_file', return_value='Mocked review comment')
def test_process_folder(mock_process_file):
    with patch('os.path.exists', return_value=True):
        with patch('os.path.isdir', return_value=True):
            with patch('os.walk') as mock_walk:
                mock_walk.return_value = [("/test", ("subdir",), ("file1.py", "file2.py"))]
                results = process_folder("/test", "fake_api_key")
                assert len(results) == 2
                assert results["/test/file1.py"] == 'Mocked review comment'
                assert results["/test/file2.py"] == 'Mocked review comment'
