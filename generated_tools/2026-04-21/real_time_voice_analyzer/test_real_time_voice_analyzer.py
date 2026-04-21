import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from real_time_voice_analyzer import analyze_audio, process_audio_file

def test_analyze_audio():
    # Mock audio data
    audio_data = np.random.rand(16000)
    sample_rate = 16000
    threshold = 0.85

    # Mock torch model
    with patch("torch.nn.Sequential") as mock_model:
        mock_model.return_value = MagicMock()
        mock_model.return_value.__enter__.return_value = mock_model
        mock_model.return_value.return_value.item.return_value = 0.9

        confidence_score = analyze_audio(audio_data, sample_rate, threshold)

    assert 0 <= confidence_score <= 1

def test_process_audio_file_valid():
    file_path = "test_audio.wav"
    threshold = 0.85

    # Mock AudioSegment and analyze_audio
    with patch("real_time_voice_analyzer.AudioSegment.from_file") as mock_from_file, \
         patch("real_time_voice_analyzer.analyze_audio") as mock_analyze_audio:

        mock_from_file.return_value.get_array_of_samples.return_value = [0, 1, 2, 3]
        mock_from_file.return_value.frame_rate = 16000
        mock_analyze_audio.return_value = 0.9

        result = process_audio_file(file_path, threshold)

    assert result["file"] == file_path
    assert result["confidence_score"] == 0.9
    assert result["is_suspicious"] is True

def test_process_audio_file_invalid():
    file_path = "non_existent_file.wav"
    threshold = 0.85

    with patch("real_time_voice_analyzer.AudioSegment.from_file", side_effect=FileNotFoundError):
        result = process_audio_file(file_path, threshold)

    assert result["file"] == file_path
    assert "error" in result