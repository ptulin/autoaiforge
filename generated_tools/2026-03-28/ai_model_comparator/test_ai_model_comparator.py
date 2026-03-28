import pytest
from unittest.mock import patch, MagicMock
from ai_model_comparator import evaluate_model

def mock_pipeline(task, model):
    class MockPipeline:
        def __call__(self, input_text):
            return {'output': f'Mock output for {input_text}'}
    return MockPipeline()

@patch('ai_model_comparator.pipeline', side_effect=mock_pipeline)
@patch('builtins.open', new_callable=MagicMock)
@patch('json.load', side_effect=lambda f: [{'text': 'Sample text 1'}, {'text': 'Sample text 2'}])
def test_evaluate_model(mock_json_load, mock_open, mock_pipeline):
    result = evaluate_model('mock-model', 'summarization', 'mock_dataset.json')
    assert result['model'] == 'mock-model'
    assert result['task'] == 'summarization'
    assert result['avg_latency'] >= 0
    assert result['num_samples'] == 2

def test_evaluate_model_invalid_task():
    result = evaluate_model('mock-model', 'invalid-task', 'mock_dataset.json')
    assert 'error' in result
    assert 'Unsupported task' in result['error']

@patch('ai_model_comparator.pipeline', side_effect=mock_pipeline)
@patch('builtins.open', new_callable=MagicMock)
@patch('json.load', side_effect=lambda f: [{'text': 'Sample text 1'}, {'text': 'Sample text 2'}])
def test_evaluate_model_error_handling(mock_json_load, mock_open, mock_pipeline):
    mock_pipeline.side_effect = Exception("Pipeline error")
    result = evaluate_model('mock-model', 'summarization', 'mock_dataset.json')
    assert 'error' in result
    assert result['error'] == 'Pipeline error'
