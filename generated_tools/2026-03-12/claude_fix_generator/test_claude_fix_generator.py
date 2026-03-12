import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from claude_fix_generator import ClaudeFixGenerator

@pytest.fixture
def mock_claude_fix_generator():
    generator = ClaudeFixGenerator(api_key="test_api_key")
    generator.client.create = MagicMock()  # Mock the create method of the client
    return generator

def test_scan_python_files(mock_claude_fix_generator, tmp_path):
    # Create mock Python files
    (tmp_path / "file1.py").write_text("print('Hello World')")
    (tmp_path / "file2.py").write_text("print('Test')")
    (tmp_path / "file.txt").write_text("Not a Python file")

    result = mock_claude_fix_generator.scan_python_files(tmp_path)
    assert len(result) == 2
    assert str(tmp_path / "file1.py") in result
    assert str(tmp_path / "file2.py") in result

def test_analyze_file(mock_claude_fix_generator, tmp_path):
    # Create a temporary Python file
    file_path = tmp_path / "test.py"
    file_path.write_text("print('Hello World')")

    # Mock the response from the client
    mock_response = {"choices": [{"message": {"content": "Mock analysis result"}}]}
    mock_claude_fix_generator.client.create.return_value = mock_response

    result = mock_claude_fix_generator.analyze_file(file_path)
    assert result == "Mock analysis result"

def test_generate_report(mock_claude_fix_generator, tmp_path):
    # Create mock Python files
    (tmp_path / "file1.py").write_text("print('Hello World')")
    (tmp_path / "file2.py").write_text("print('Test')")

    # Mock the response from the client
    mock_response = {"choices": [{"message": {"content": "Mock analysis result"}}]}
    mock_claude_fix_generator.client.create.return_value = mock_response

    report = mock_claude_fix_generator.generate_report(tmp_path)
    assert len(report) == 2
    assert report[str(tmp_path / "file1.py")] == "Mock analysis result"
    assert report[str(tmp_path / "file2.py")] == "Mock analysis result"