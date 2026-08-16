import pytest
from unittest.mock import patch, MagicMock
from model_pruner import load_model, prune_model, save_model

@pytest.fixture
def mock_model():
    return MagicMock()

def test_load_model_pt(mock_model):
    with patch('torch.load') as mock_load:
        mock_load.return_value = mock_model
        loaded_model = load_model('model.pt')
        assert loaded_model == mock_model

def test_prune_model(mock_model):
    pruned_model = prune_model(mock_model, 0.5, 'magnitude-based')
    assert pruned_model == mock_model

def test_save_model_torch(mock_model):
    with patch('torch.save') as mock_save:
        save_model(mock_model, 'output.pt')
        mock_save.assert_called_once()

def test_load_model_unsupported_format():
    with pytest.raises(ValueError):
        load_model('model.h5')