import pytest
from unittest.mock import patch, MagicMock
from llm_agent_composer import compose_agents
import json
import sklearn

@pytest.fixture
def mock_agent_models():
    return ['model1.pth', 'model2.pth']

@pytest.fixture
def mock_composition_config():
    return {'weights': [0.5, 0.5]}

@patch('transformers.AutoModelForSequenceClassification.from_pretrained')
@patch('sklearn.ensemble.VotingClassifier')
def test_compose_agents(mock_voting_classifier, mock_from_pretrained, mock_agent_models, mock_composition_config):
    mock_from_pretrained.return_value = MagicMock()
    composed_agent = compose_agents(mock_agent_models, mock_composition_config)
    assert composed_agent is not None

@patch('transformers.AutoModelForSequenceClassification.from_pretrained')
@patch('sklearn.ensemble.VotingClassifier')
def test_compose_agents_empty_agent_models(mock_voting_classifier, mock_from_pretrained):
    mock_from_pretrained.return_value = MagicMock()
    composed_agent = compose_agents([], {'weights': [0.5, 0.5]})
    assert composed_agent is None

@patch('transformers.AutoModelForSequenceClassification.from_pretrained')
@patch('sklearn.ensemble.VotingClassifier')
def test_compose_agents_empty_composition_config(mock_voting_classifier, mock_from_pretrained):
    mock_from_pretrained.return_value = MagicMock()
    with pytest.raises(ValueError):
        compose_agents(['model1.pth'], {})

@patch('transformers.AutoModelForSequenceClassification.from_pretrained')
@patch('sklearn.ensemble.VotingClassifier')
def test_compose_agents_mismatched_agent_models_and_weights(mock_voting_classifier, mock_from_pretrained):
    mock_from_pretrained.return_value = MagicMock()
    with pytest.raises(ValueError):
        compose_agents(['model1.pth', 'model2.pth'], {'weights': [0.5]})