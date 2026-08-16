import pytest
import tensorflow as tf
import torch
from unittest.mock import patch, MagicMock
from model_compressor import compress_model

@pytest.fixture
def mock_model():
    return tf.keras.models.Sequential([tf.keras.layers.Dense(10)])

def test_compress_model_quantization(mock_model):
    with patch('tensorflow.keras.models.load_model', return_value=mock_model):
        compressed_model = compress_model('input_model.h5', 0.5, 'output_model.h5', 'quantization')
        assert isinstance(compressed_model, tf.keras.Model)

def test_compress_model_knowledge_distillation(mock_model):
    with patch('tensorflow.keras.models.load_model', return_value=mock_model):
        compressed_model = compress_model('input_model.h5', 0.5, 'output_model.h5', 'knowledge_distillation')
        assert isinstance(compressed_model, tf.keras.Model)

def test_compress_model_weight_sharing(mock_model):
    with patch('tensorflow.keras.models.load_model', return_value=mock_model):
        compressed_model = compress_model('input_model.h5', 0.5, 'output_model.h5', 'weight_sharing')
        assert isinstance(compressed_model, tf.keras.Model)

def test_compress_model_unsupported_format():
    with patch('tensorflow.keras.models.load_model', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            compress_model('input_model.h5', 0.5, 'output_model.h5', 'quantization')

def test_compress_model_unsupported_algorithm(mock_model):
    with patch('tensorflow.keras.models.load_model', return_value=mock_model):
        with pytest.raises(ValueError):
            compress_model('input_model.h5', 0.5, 'output_model.h5', 'unsupported_algorithm')

def test_compress_model_unsupported_format_type():
    with pytest.raises(ValueError):
        compress_model('input_model.txt', 0.5, 'output_model.h5', 'quantization')