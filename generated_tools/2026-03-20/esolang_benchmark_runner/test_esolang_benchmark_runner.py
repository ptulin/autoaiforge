import pytest
import json
from unittest.mock import patch, MagicMock
from esolang_benchmark_runner import main
from click.testing import CliRunner

@pytest.fixture
def mock_openai():
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            'choices': [
                {'message': {'content': 'mocked_generated_code'}}
            ]
        }
        yield mock

def test_main_valid_json_output(mock_openai, tmp_path):
    runner = CliRunner()
    tasks_file = tmp_path / "tasks.json"
    output_file = tmp_path / "output.json"

    tasks = [
        {"prompt": "Translate to brainfuck", "expected_output": "mocked_generated_code"}
    ]
    tasks_file.write_text(json.dumps(tasks))

    result = runner.invoke(main, [
        '--model', 'gpt-4',
        '--language', 'brainfuck',
        '--tasks', str(tasks_file),
        '--output', str(output_file)
    ])

    assert result.exit_code == 0
    assert output_file.exists()

    with open(output_file, 'r') as f:
        output_data = json.load(f)
        assert len(output_data) == 1
        assert output_data[0]['accuracy'] == 1

def test_main_invalid_tasks_file():
    runner = CliRunner()
    result = runner.invoke(main, [
        '--model', 'gpt-4',
        '--language', 'brainfuck',
        '--tasks', 'nonexistent.json',
        '--output', 'output.json'
    ])

    assert result.exit_code != 0
    assert "Error" in result.output

def test_main_invalid_output_extension(mock_openai, tmp_path):
    runner = CliRunner()
    tasks_file = tmp_path / "tasks.json"
    tasks = [
        {"prompt": "Translate to brainfuck", "expected_output": "mocked_generated_code"}
    ]
    tasks_file.write_text(json.dumps(tasks))

    result = runner.invoke(main, [
        '--model', 'gpt-4',
        '--language', 'brainfuck',
        '--tasks', str(tasks_file),
        '--output', str(tmp_path / 'output.invalid')
    ])

    assert result.exit_code != 0
    assert "Error" in result.output
    assert "Output file must have a .json or .csv extension." in result.output
