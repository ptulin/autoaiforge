import pytest
from unittest.mock import patch, MagicMock
from llm_checkpoint_converter import convert_checkpoint

def test_convert_checkpoint_pytorch_to_tensorflow():
    with patch('llm_checkpoint_converter.AutoConfig.from_pretrained') as mock_config, \
         patch('llm_checkpoint_converter.AutoModel.from_pretrained') as mock_model, \
         patch('llm_checkpoint_converter.tf.saved_model.save') as mock_tf_save, \
         patch('os.path.exists', return_value=True):

        mock_config.return_value = MagicMock(hidden_size=768)
        mock_model.return_value = MagicMock()

        input_file = 'dummy_model.pt'
        output_file = 'converted_model_tf'
        output_format = 'tensorflow'

        result = convert_checkpoint(input_file, output_format, output_file)

        mock_tf_save.assert_called_once()
        assert result == output_file

def test_convert_checkpoint_tensorflow_to_pytorch():
    with patch('llm_checkpoint_converter.AutoConfig.from_pretrained') as mock_config, \
         patch('llm_checkpoint_converter.tf.keras.models.load_model') as mock_tf_load, \
         patch('llm_checkpoint_converter.AutoModel.from_config') as mock_model, \
         patch('llm_checkpoint_converter.torch.save') as mock_torch_save, \
         patch('os.path.exists', return_value=True):

        mock_config.return_value = MagicMock()
        mock_tf_load.return_value = MagicMock()
        mock_model.return_value = MagicMock()

        input_file = 'dummy_model_tf'
        output_file = 'converted_model_pt'
        output_format = 'pytorch'

        result = convert_checkpoint(input_file, output_format, output_file)

        mock_torch_save.assert_called_once()
        assert result == output_file

def test_convert_checkpoint_invalid_format():
    with patch('os.path.exists', return_value=True):
        with pytest.raises(ValueError):
            convert_checkpoint('dummy_model.pt', 'invalid_format', 'output_file')

def test_convert_checkpoint_file_not_found():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            convert_checkpoint('non_existent_file.pt', 'pytorch', 'output_file')