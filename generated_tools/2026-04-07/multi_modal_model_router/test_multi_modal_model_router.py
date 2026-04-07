import pytest
from unittest.mock import patch, mock_open
from multi_modal_model_router import detect_content_type, process_text, process_image, process_audio

def test_detect_content_type():
    assert detect_content_type("example.jpg") == "image"
    assert detect_content_type("example.wav") == "audio"
    assert detect_content_type("example.txt") == "text"
    with pytest.raises(ValueError):
        detect_content_type("example.unknown")

@patch("builtins.open", new_callable=mock_open, read_data="Hello world!")
@patch("multi_modal_model_router.pipeline")
def test_process_text(mock_pipeline, mock_file):
    mock_pipeline.return_value = lambda text, max_length, num_return_sequences: [{'generated_text': 'Hello world! Generated.'}]
    result = process_text("example.txt")
    assert result == "Hello world! Generated."

@patch("multi_modal_model_router.Image.open")
@patch("multi_modal_model_router.pipeline")
def test_process_image(mock_pipeline, mock_image_open):
    mock_image_open.return_value = "mock_image"
    mock_pipeline.return_value = lambda image: [{'label': 'cat', 'score': 0.98}]
    result = process_image("example.jpg")
    assert result == "[{'label': 'cat', 'score': 0.98}]"

@patch("librosa.load")
@patch("librosa.get_duration")
def test_process_audio(mock_get_duration, mock_librosa_load):
    mock_librosa_load.return_value = ([0.1, 0.2, 0.3], 22050)
    mock_get_duration.return_value = 0.01
    result = process_audio("example.wav")
    assert result == "Audio file duration: 0.01 seconds"
