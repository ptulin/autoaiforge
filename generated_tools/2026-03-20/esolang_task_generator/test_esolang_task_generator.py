import pytest
from unittest.mock import patch
from esolang_task_generator import generate_task, validate_brainfuck_syntax

def test_generate_task_brainfuck():
    task = generate_task(language='brainfuck', complexity=10)
    assert isinstance(task, str)
    assert len(task) == 10
    assert validate_brainfuck_syntax(task)

def test_generate_task_invalid_language():
    with pytest.raises(ValueError, match="Unsupported language: invalid_lang"):
        generate_task(language='invalid_lang', complexity=5)

def test_generate_task_invalid_complexity():
    with pytest.raises(ValueError, match="Complexity must be a positive integer."):
        generate_task(language='brainfuck', complexity=0)

def test_validate_brainfuck_syntax_valid():
    valid_program = "++[>++<-]"
    assert validate_brainfuck_syntax(valid_program) is True

def test_validate_brainfuck_syntax_invalid():
    invalid_program = "++[>++<-"
    assert validate_brainfuck_syntax(invalid_program) is False