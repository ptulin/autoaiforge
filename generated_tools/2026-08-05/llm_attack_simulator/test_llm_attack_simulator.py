import pytest
import numpy as np
import torch
from unittest.mock import patch
from llm_attack_simulator import simulate_adversarial_attack, simulate_data_poisoning_attack, evaluate_model_robustness


def test_simulate_adversarial_attack():
    model = torch.nn.Linear(10, 10)
    input_data = np.random.randn(10, 10)
    perturbed_input = simulate_adversarial_attack(model, input_data)
    assert perturbed_input.shape == input_data.shape


def test_simulate_data_poisoning_attack():
    model = torch.nn.Linear(10, 10)
    input_data = np.random.randn(10, 10)
    poisoned_input = simulate_data_poisoning_attack(model, input_data)
    assert poisoned_input.shape == input_data.shape

@patch('torch.load')
def test_evaluate_model_robustness(mock_load):
    model = torch.nn.Linear(10, 10)
    mock_load.return_value = model
    input_data = np.random.randn(10, 10)
    model_output = evaluate_model_robustness(model, input_data, 'adversarial', {'epsilon': 0.1})
    assert model_output.shape == (10, 10)