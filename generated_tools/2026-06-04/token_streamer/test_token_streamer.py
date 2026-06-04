import pytest
from unittest.mock import patch, MagicMock, mock_open
from token_streamer import stream_tokens

def test_stream_tokens_basic():
    with patch("token_streamer.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("token_streamer.AutoModelForCausalLM.from_pretrained") as mock_model:

        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.encode.return_value = [1, 2, 3]
        mock_tokenizer.return_value.decode.return_value = "Test inputGenerated text"

        mock_model.return_value = MagicMock()
        mock_model.return_value.generate.return_value = [[1, 2, 3, 4, 5, 6]]

        stream_tokens("mock_model_path", "Test input", 0.1)

        mock_tokenizer.assert_called_once_with("mock_model_path")
        mock_model.assert_called_once_with("mock_model_path")

def test_stream_tokens_with_output_file():
    with patch("token_streamer.AutoTokenizer.from_pretrained") as mock_tokenizer, \
         patch("token_streamer.AutoModelForCausalLM.from_pretrained") as mock_model, \
         patch("builtins.open", mock_open()) as mock_file:

        mock_tokenizer.return_value = MagicMock()
        mock_tokenizer.return_value.encode.return_value = [1, 2, 3]
        mock_tokenizer.return_value.decode.return_value = "Test inputGenerated text"

        mock_model.return_value = MagicMock()
        mock_model.return_value.generate.return_value = [[1, 2, 3, 4, 5, 6]]

        stream_tokens("mock_model_path", "Test input", 0.1, output_file="output.txt")

        mock_file.assert_called_once_with("output.txt", "w")
        mock_file().write.assert_called_once_with("Generated text")

def test_stream_tokens_error_handling():
    with patch("token_streamer.AutoTokenizer.from_pretrained", side_effect=Exception("Mock error")) as mock_tokenizer:
        with pytest.raises(Exception, match="Mock error"):
            stream_tokens("mock_model_path", "Test input", 0.1)

        mock_tokenizer.assert_called_once_with("mock_model_path")