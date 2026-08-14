import pytest
from unittest.mock import patch
from llm_pipeline_optimizer import analyze_pipeline, optimize_pipeline
import json

@pytest.fixture
def config():
    return {'model_name': 'bert-base-uncased'}

@patch('llm_pipeline_optimizer.AutoModelForSequenceClassification')
@patch('llm_pipeline_optimizer.AutoTokenizer')
def test_analyze_pipeline(mock_tokenizer, mock_model, config):
    performance_report = analyze_pipeline(config)
    assert 'model_name' in performance_report
    assert 'num_parameters' in performance_report

@patch('llm_pipeline_optimizer.analyze_pipeline')
def test_optimize_pipeline(mock_analyze_pipeline, config):
    mock_analyze_pipeline.return_value = {'model_name': 'bert-base-uncased', 'num_parameters': 100}
    performance_report, optimization_suggestions = optimize_pipeline(config)
    assert 'model_name' in performance_report
    assert 'num_parameters' in performance_report
    assert 'batch_size' in optimization_suggestions
    assert 'sequence_length' in optimization_suggestions

def test_optimize_pipeline_empty_config():
    config = {}
    with pytest.raises(KeyError):
        optimize_pipeline(config)

def test_optimize_pipeline_invalid_config():
    config = {'model_name': None}
    with pytest.raises(TypeError):
        optimize_pipeline(config)

def test_analyze_pipeline_invalid_config():
    config = {'model_name': None}
    with pytest.raises(TypeError):
        analyze_pipeline(config)