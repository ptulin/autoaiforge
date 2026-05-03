import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
from ai_video_captioner import extract_audio, transcribe_audio, translate_text, save_captions

def test_extract_audio():
    with patch('ffmpeg.input') as mock_input, patch('ffmpeg.output') as mock_output:
        mock_run = MagicMock()
        mock_output.return_value.run = mock_run
        mock_input.return_value.output = mock_output
        extract_audio("input.mp4", "output.wav")
        mock_input.assert_called_once_with("input.mp4")
        mock_output.assert_called_once_with("output.wav", ac=1, ar='16000')
        mock_run.assert_called_once_with(overwrite_output=True)

def test_transcribe_audio():
    with patch('builtins.open', mock_open(read_data=b"audio data")) as mock_file, \
         patch('openai.Audio.transcribe') as mock_transcribe:
        mock_transcribe.return_value = {'text': 'Hello world'}
        result = transcribe_audio("output.wav")
        assert result == 'Hello world'
        mock_transcribe.assert_called_once()
        args, kwargs = mock_transcribe.call_args
        assert args[0] == "whisper-1"
        assert args[1].read() == b"audio data"

def test_translate_text():
    with patch('openai.Completion.create') as mock_create:
        mock_create.return_value = {'choices': [{'text': 'Hola mundo'}]}
        result = translate_text("Hello world", ["es"])
        assert result == {"es": "Hola mundo"}
        mock_create.assert_called_once_with(
            engine="text-davinci-003",
            prompt="Translate the following text to es: Hello world",
            max_tokens=1000
        )

def test_save_captions():
    captions = ["Hello world", "Hola mundo"]
    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        save_captions(captions, "output.srt", "srt")
        mock_file.assert_called_once_with("output.srt", 'w', encoding='utf-8')
        mock_file().write.assert_any_call("1\n00:00:01,000 --> 00:00:02,000\nHello world\n\n")
        mock_file().write.assert_any_call("2\n00:00:02,000 --> 00:00:03,000\nHola mundo\n\n")
