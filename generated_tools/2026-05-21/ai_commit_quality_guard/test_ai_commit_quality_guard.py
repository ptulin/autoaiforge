import pytest
from unittest.mock import patch, mock_open
from ai_commit_quality_guard import get_staged_files, review_code, load_config

def test_get_staged_files():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = 'file1.py\nfile2.py\nfile3.txt\n'
        mock_run.return_value.returncode = 0
        files = get_staged_files()
        assert files == ['file1.py', 'file2.py']

def test_review_code():
    with patch('openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = {
            'choices': [
                {'message': {'content': 'No issues found in the code.'}}
            ]
        }
        result = review_code("print('Hello, World!')", "fake_api_key")
        assert result == 'No issues found in the code.'

def test_load_config():
    mock_yaml_content = """
    rules:
      max_line_length: 80
    """
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        with patch("os.path.exists", return_value=True):
            config = load_config("fake_path.yaml")
            assert config == {'rules': {'max_line_length': 80}}

    with patch("os.path.exists", return_value=False):
        config = load_config("non_existent.yaml")
        assert config == {}

    with patch("builtins.open", mock_open(read_data="invalid_yaml: [")):
        with patch("os.path.exists", return_value=True):
            config = load_config("invalid.yaml")
            assert config == {}