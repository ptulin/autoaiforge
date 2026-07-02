import pytest
from unittest.mock import patch, mock_open
from debugging_task_generator import inject_bug

def test_inject_syntax_error():
    code = "print('Hello, world!')"
    with patch("builtins.open", mock_open(read_data=code)):
        with patch("debugging_task_generator.format_str", side_effect=lambda x, mode: x):
            buggy_code = inject_bug("test_file.py", "syntax")
    assert "print(\"Unclosed string\")" in buggy_code

def test_inject_logic_error():
    code = "if x == 5: print('Equal')"
    with patch("builtins.open", mock_open(read_data=code)):
        with patch("debugging_task_generator.format_str", side_effect=lambda x, mode: x):
            buggy_code = inject_bug("test_file.py", "logic")
    assert "if x != 5:" in buggy_code

def test_inject_runtime_error():
    code = "x = 10"
    with patch("builtins.open", mock_open(read_data=code)):
        with patch("debugging_task_generator.format_str", side_effect=lambda x, mode: x):
            buggy_code = inject_bug("test_file.py", "runtime")
    assert "result = 1 / 0" in buggy_code