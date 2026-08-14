import pytest
from unittest.mock import patch, MagicMock
from llm_pipeline_composer import compose_pipeline
import graphviz

@pytest.fixture
def mock_model():
    return 'mock_model'

@pytest.fixture
def mock_config():
    return {'steps': [{'name': 'step1'}, {'name': 'step2'}]}

def test_compose_pipeline(mock_model, mock_config):
    pipeline = compose_pipeline(mock_model, mock_config)
    assert isinstance(pipeline, graphviz.Digraph)

@patch('graphviz.Digraph')
def test_compose_pipeline_mock_graphviz(mock_graphviz, mock_model, mock_config):
    compose_pipeline(mock_model, mock_config)
    mock_graphviz.assert_called_once()

@patch('streamlit.text_input')
@patch('streamlit.text_area')
@patch('streamlit.button')
def test_main(mock_button, mock_text_area, mock_text_input):
    mock_text_input.return_value = 'mock_model'
    mock_text_area.return_value = "{{'steps': [{'name': 'step1'}, {{'name': 'step2'}}]}}"
    mock_button.return_value = True
    with patch('sys.argv', ['llm_pipeline_composer.py', '--edit', 'pipeline.json']):
        import llm_pipeline_composer
        llm_pipeline_composer.main()