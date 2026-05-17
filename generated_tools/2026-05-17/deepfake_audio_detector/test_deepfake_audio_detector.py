import pytest
from unittest.mock import patch, MagicMock
from deepfake_audio_detector import analyze_audio

def test_analyze_audio_valid_file():
    # Mock AudioSegment and torchaudio
    with patch("deepfake_audio_detector.AudioSegment.from_file") as mock_from_file:
        mock_audio = MagicMock()
        mock_audio.get_array_of_samples.return_value = [1, 2, 3, 4]
        mock_audio.frame_rate = 44100
        mock_audio.channels = 1
        mock_from_file.return_value = mock_audio

        with patch("deepfake_audio_detector.torchaudio.transforms.Resample") as mock_resample:
            mock_resample.return_value = lambda x: x

            confidence_score, likelihood = analyze_audio("test_audio.mp3")
            assert 0 <= confidence_score <= 100
            assert likelihood in ["Deepfake", "Authentic"]

def test_analyze_audio_file_not_found():
    with pytest.raises(RuntimeError):
        analyze_audio("non_existent_file.mp3")

def test_analyze_audio_invalid_channels():
    with patch("deepfake_audio_detector.AudioSegment.from_file") as mock_from_file:
        mock_audio = MagicMock()
        mock_audio.channels = 2  # Invalid number of channels
        mock_from_file.return_value = mock_audio

        with pytest.raises(RuntimeError):
            analyze_audio("test_audio.mp3")