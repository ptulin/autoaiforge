import pytest
from unittest.mock import patch, MagicMock
from claude_code_assistant import generate_boilerplate, refactor_code, code_completion

def test_generate_boilerplate():
    with patch('openai.Completion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text='def main():\n    print("Hello, World!")')])
        result = generate_boilerplate('flask_app')
        assert result == 'def main():\n    print("Hello, World!")'

def test_refactor_code(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("print('Hello, World!')")

    with patch('openai.Completion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text='def main():\n    print("Hello, World!")')])
        result = refactor_code(str(test_file))
        assert result == 'def main():\n    print("Hello, World!")'

def test_code_completion():
    with patch('openai.Completion.create') as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text='print("Hello, World!")')])
        result = code_completion('print("Hello')
        assert result == 'print("Hello, World!")'

def test_refactor_code_file_not_found():
    with pytest.raises(FileNotFoundError):
        refactor_code('non_existent_file.py')

def test_generate_boilerplate_error():
    with patch('openai.Completion.create', side_effect=Exception('API error')):
        with pytest.raises(RuntimeError):
            generate_boilerplate('flask_app')

def test_code_completion_error():
    with patch('openai.Completion.create', side_effect=Exception('API error')):
        with pytest.raises(RuntimeError):
            code_completion('print("Hello')
