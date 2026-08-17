import pytest
from unittest.mock import patch, MagicMock
from ai_code_summarizer import summarize_code

@patch('transformers.AutoModelForSeq2SeqLM.from_pretrained')
@patch('transformers.AutoTokenizer.from_pretrained')
def test_summarize_code(mock_tokenizer, mock_model):
    mock_model.return_value = MagicMock()
    mock_tokenizer.return_value = MagicMock()
    mock_model.return_value.generate.return_value = [[1]]
    mock_tokenizer.return_value.decode.return_value = 'Summary'
    code = 'def add(a, b): return a + b'
    summary = summarize_code(code)
    assert summary == 'Summary'

@patch('ast.parse')
def test_summarize_code_ast_parse_error(mock_parse):
    mock_parse.side_effect = SyntaxError('Invalid syntax')
    code = 'def add(a, b): return a + b'
    summary = summarize_code(code)
    assert 'Invalid syntax' in summary

@patch('transformers.AutoModelForSeq2SeqLM.from_pretrained')
@patch('transformers.AutoTokenizer.from_pretrained')
def test_summarize_code_model_error(mock_tokenizer, mock_model):
    mock_model.return_value = MagicMock()
    mock_tokenizer.return_value = MagicMock()
    mock_model.return_value.generate.side_effect = Exception('Model error')
    code = 'def add(a, b): return a + b'
    summary = summarize_code(code)
    assert 'Model error' in summary