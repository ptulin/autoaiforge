import pytest
from unittest.mock import patch, mock_open
from ai_code_review_assistant import analyze_code_with_ai, process_file, analyze_directory

def test_analyze_code_with_ai():
    with patch('openai.Completion.create') as mock_openai:
        mock_openai.return_value = {'choices': [{'text': 'Mocked AI feedback'}]}
        result = analyze_code_with_ai("print('Hello, world!')", "example.py")
        assert result == 'Mocked AI feedback'

def test_process_file():
    mock_file_content = "print('Hello, world!')"
    with patch('builtins.open', mock_open(read_data=mock_file_content)):
        with patch('os.path.isfile', return_value=True):
            with patch('openai.Completion.create') as mock_openai:
                mock_openai.return_value = {'choices': [{'text': 'Mocked AI feedback'}]}
                feedback, highlighted_code = process_file("example.py")
                assert "Mocked AI feedback" in feedback
                assert "print('Hello, world!')" in highlighted_code.replace('\x1b', '').replace('[36m', '').replace('[39;49;00m', '').replace('[33m', '').replace('[37m', '')

def test_analyze_directory():
    mock_file_content = "print('Hello, world!')"
    with patch('os.path.isdir', return_value=True):
        with patch('os.walk', return_value=[("/mock_dir", [], ["example.py"])]):
            with patch('builtins.open', mock_open(read_data=mock_file_content)):
                with patch('os.path.isfile', return_value=True):
                    with patch('openai.Completion.create') as mock_openai:
                        mock_openai.return_value = {'choices': [{'text': 'Mocked AI feedback'}]}
                        results = analyze_directory("/mock_dir")
                        assert len(results) == 1
                        assert results[0][0] == "/mock_dir/example.py"
                        assert "Mocked AI feedback" in results[0][1]
                        assert "print('Hello, world!')" in results[0][2].replace('\x1b', '').replace('[36m', '').replace('[39;49;00m', '').replace('[33m', '').replace('[37m', '')
