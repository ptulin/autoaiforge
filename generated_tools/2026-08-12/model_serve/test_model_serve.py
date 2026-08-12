import pytest
from unittest.mock import patch, MagicMock
from model_serve import load_model, serve_model

@patch('tensorflow.keras.models.load_model')
def test_load_model_tensorflow(mock_load_model):
    load_model('model.h5', 'tensorflow')
    mock_load_model.assert_called_once_with('model.h5')

@patch('torch.load')
def test_load_model_pytorch(mock_load):
    load_model('model.pth', 'pytorch')
    mock_load.assert_called_once_with('model.pth')

@patch('sklearn.ensemble.RandomForestClassifier')
def test_load_model_scikit_learn(mock_rf):
    load_model('model.pkl', 'scikit-learn')
    mock_rf.assert_called_once()

@patch('flask.Flask')
def test_serve_model(mock_flask):
    model = MagicMock()
    endpoint = '/predict'
    framework = 'tensorflow'
    app = serve_model(model, endpoint, framework)
    assert app is not None

@patch('flask.Flask')
def test_serve_model_pytorch(mock_flask):
    model = MagicMock()
    endpoint = '/predict_pytorch'
    framework = 'pytorch'
    app = serve_model(model, endpoint, framework)
    assert app is not None

@patch('flask.Flask')
def test_serve_model_scikit_learn(mock_flask):
    model = MagicMock()
    endpoint = '/predict_scikit_learn'
    framework = 'scikit-learn'
    app = serve_model(model, endpoint, framework)
    assert app is not None