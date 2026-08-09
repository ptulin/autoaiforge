import pytest
import json
from unittest.mock import patch
from dialogue_flow_optimizer import load_dialogue_flow, visualize_dialogue_flow, optimize_dialogue_flow, calculate_conversational_metrics

@pytest.fixture
def dialogue_flow_data():
    return {'nodes': [{'id': 'A', 'label': 'Node A'}, {'id': 'B', 'label': 'Node B'}], 'edges': [{'source': 'A', 'target': 'B'}]}

def test_load_dialogue_flow(dialogue_flow_data, tmp_path):
    file_path = tmp_path / 'dialogue_flow.json'
    with open(file_path, 'w') as file:
        json.dump(dialogue_flow_data, file)
    loaded_flow = load_dialogue_flow(file_path)
    assert loaded_flow == dialogue_flow_data

@patch('matplotlib.pyplot.show')
def test_visualize_dialogue_flow(mock_show, dialogue_flow_data):
    visualize_dialogue_flow(dialogue_flow_data)
    mock_show.assert_called_once()

def test_optimize_dialogue_flow(dialogue_flow_data):
    optimized_flow = optimize_dialogue_flow(dialogue_flow_data)
    assert len(optimized_flow['nodes']) == 1
    assert len(optimized_flow['edges']) == 1

def test_calculate_conversational_metrics(dialogue_flow_data):
    metrics = calculate_conversational_metrics(dialogue_flow_data)
    assert metrics['nodes'] == 2
    assert metrics['edges'] == 1