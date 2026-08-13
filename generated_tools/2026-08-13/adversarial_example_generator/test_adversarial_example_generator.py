import pytest
import torch
from unittest.mock import patch, MagicMock
from adversarial_example_generator import Net, pgd_attack, main

# Define test cases
@pytest.fixture
def model():
    return Net()

@pytest.fixture
def input_data():
    return torch.randn(10, 4)

def test_pgd_attack(model, input_data):
    # Test PGD attack function
    adversarial_example = pgd_attack(model, input_data)
    assert adversarial_example.shape == input_data.shape

@patch('torch.load')
@patch('torch.save')
def test_main(torch_save, torch_load, model, input_data):
    # Test main function
    torch_load.return_value = model
    main('model.pt', 'input.csv', 'pgd')
    assert torch_load.called
    assert torch_save.called

@patch('torch.load')
@patch('torch.save')
def test_main_save_adversarial_example(torch_save, torch_load, model, input_data):
    # Test saving adversarial example
    torch_load.return_value = model
    main('model.pt', 'input.csv', 'pgd')
    assert torch_save.called