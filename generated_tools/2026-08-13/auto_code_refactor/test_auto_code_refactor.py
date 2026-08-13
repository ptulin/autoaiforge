import pytest
from unittest.mock import patch, MagicMock
from auto_code_refactor import refactor_code, main

@pytest.fixture
def test_code():
    return 'def test_function():\n    pass\n'

def test_refactor_code(test_code):
    refactored_code = refactor_code(test_code)
    assert refactored_code == test_code.rstrip()

@patch('pylint.lint.Run')
def test_main(mock_pylint, test_code, tmp_path):
    input_file = tmp_path / 'input.py'
    output_file = tmp_path / 'output.py'
    input_file.write_text(test_code)

    # Run main function
    main(str(input_file), str(output_file))

    # Check output file exists and has refactored code
    assert output_file.exists()
    assert output_file.read_text() == test_code.rstrip()

    # Check pylint was called
    mock_pylint.assert_called_once()

@patch('builtins.open')
def test_main_file_not_found(mock_open, test_code):
    mock_open.side_effect = FileNotFoundError('Mocked FileNotFoundError')
    with pytest.raises(FileNotFoundError):
        main('non_existent_file.py', 'output.py')

@patch('pylint.lint.Run')
def test_main_pylint_error(mock_pylint, test_code, tmp_path):
    input_file = tmp_path / 'input.py'
    output_file = tmp_path / 'output.py'
    input_file.write_text(test_code)
    mock_pylint.side_effect = Exception('Mocked pylint error')

    # Run main function
    main(str(input_file), str(output_file))

    # Check output file exists and has refactored code
    assert output_file.exists()
    assert output_file.read_text() == test_code.rstrip()

    # Check pylint was called
    mock_pylint.assert_called_once()
