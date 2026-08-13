import pytest
import json
from unittest.mock import patch
from llm_accelerator_optimizer import analyze_model, identify_bottlenecks, optimize_model, generate_report

@pytest.fixture
def model_file(tmp_path):
    model = {'layers': [{'type': 'conv2d', 'kernel_size': 5}]}  # Define a simple model
    model_file = tmp_path / 'model.json'
    with open(model_file, 'w') as f:
        json.dump(model, f)
    return model_file

@pytest.fixture
def hardware_file(tmp_path):
    hardware = {'gpu': True}
    hardware_file = tmp_path / 'hardware.json'
    with open(hardware_file, 'w') as f:
        json.dump(hardware, f)
    return hardware_file

def test_analyze_model(model_file):
    model = analyze_model(model_file)
    assert model['layers'][0]['type'] == 'conv2d'

def test_identify_bottlenecks(model_file):
    model = analyze_model(model_file)
    bottlenecks = identify_bottlenecks(model)
    assert len(bottlenecks) == 1

def test_optimize_model(model_file, hardware_file):
    model = analyze_model(model_file)
    hardware = json.load(open(hardware_file, 'r'))
    optimized_model = optimize_model(model, hardware)
    assert optimized_model['layers'][0]['kernel_size'] == 3

@patch('llm_accelerator_optimizer.json.load')
def test_generate_report(mock_json_load, model_file, hardware_file):
    model = analyze_model(model_file)
    hardware = json.load(open(hardware_file, 'r'))
    optimized_model = optimize_model(model, hardware)
    report = generate_report(model, hardware, optimized_model)
    assert 'model' in report
    assert 'hardware' in report
    assert 'optimized_model' in report
