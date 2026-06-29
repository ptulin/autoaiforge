import pytest
from unittest.mock import patch, MagicMock, mock_open
import llm_edge_runner
import argparse

def test_load_model():
    with patch('llm_edge_runner.AutoTokenizer.from_pretrained') as mock_tokenizer, \
         patch('llm_edge_runner.AutoModelForCausalLM.from_pretrained') as mock_model:
        mock_tokenizer.return_value = MagicMock()
        mock_model.return_value = MagicMock()
        model, tokenizer = llm_edge_runner.load_model('test-model')
        assert model is not None
        assert tokenizer is not None

def test_check_resources():
    with patch('llm_edge_runner.psutil.virtual_memory') as mock_memory:
        mock_memory.return_value = MagicMock(available=1024 * 1024 * 1024)  # 1 GB
        available_memory = llm_edge_runner.check_resources()
        assert available_memory == pytest.approx(1024, rel=1e-2)

def test_load_fallback_response():
    with patch('builtins.open', mock_open(read_data='{"default": "Fallback response"}')):
        with patch('os.path.exists', return_value=True):
            fallback = llm_edge_runner.load_fallback_response('fallback.json')
            assert fallback['default'] == "Fallback response"

def test_run_model():
    mock_tokenizer = MagicMock()
    mock_model = MagicMock()
    mock_tokenizer.return_value = {'input_ids': MagicMock()}
    mock_model.generate.return_value = [MagicMock()]
    mock_tokenizer.decode.return_value = "Generated response"

    response = llm_edge_runner.run_model(mock_model, mock_tokenizer, "Hello")
    assert response == "Generated response"

def test_main_low_memory():
    with patch('llm_edge_runner.check_resources', return_value=400) as mock_resources, \
         patch('llm_edge_runner.load_fallback_response', return_value={"default": "Fallback response"}) as mock_fallback, \
         patch('builtins.print') as mock_print:
        with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(model='test-model', fallback='fallback.json', input='Hello')):
            llm_edge_runner.main()
            mock_print.assert_any_call("Low memory detected. Using fallback responses.")
            mock_print.assert_any_call("Fallback response")