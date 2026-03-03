import pytest
from unittest.mock import patch, mock_open
from ai_code_reviewer import analyze_code

@patch('ai_code_reviewer.analyze_code')
def test_analyze_code(mock_analyze_code):
    mock_analyze_code.return_value = "### Code Review\n\n#### Style\n- Example style feedback."
    result = analyze_code("print('Hello World')")
    assert "### Code Review" in result
    assert "#### Style" in result

@patch('builtins.open', new_callable=mock_open, read_data="print('Hello World')")
@patch('os.path.isfile', return_value=True)
@patch('ai_code_reviewer.analyze_code', return_value="### Code Review\n\n#### Style\n- Example style feedback.")
def test_main_single_file(mock_analyze_code, mock_isfile, mock_open):
    from click.testing import CliRunner
    from ai_code_reviewer import main

    runner = CliRunner()
    result = runner.invoke(main, ['--files', 'test.py'])

    assert result.exit_code == 0
    assert "### Code Review" in result.output
    assert "#### Style" in result.output

@patch('builtins.open', new_callable=mock_open, read_data="print('Hello World')")
@patch('os.path.isfile', return_value=True)
@patch('ai_code_reviewer.analyze_code', return_value="### Code Review\n\n#### Style\n- Example style feedback.")
def test_main_output_file(mock_analyze_code, mock_isfile, mock_open):
    from click.testing import CliRunner
    from ai_code_reviewer import main

    runner = CliRunner()
    result = runner.invoke(main, ['--files', 'test.py', '--output', 'output.md'])

    assert result.exit_code == 0
    mock_open.assert_called_with('output.md', 'w')
    mock_open().write.assert_called_once_with("### Code Review\n\n#### Style\n- Example style feedback.")
