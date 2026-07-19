import pytest
import json
from unittest.mock import patch, MagicMock
from ai_track_identifier import analyze_audio

def test_analyze_audio_valid_file():
    with patch("pydub.AudioSegment.from_file") as mock_from_file:
        mock_audio = MagicMock()
        mock_audio.get_array_of_samples.return_value = [0, 1, -1, 0, 1, -1]
        mock_audio.frame_rate = 44100
        mock_from_file.return_value = mock_audio

        result = analyze_audio("test.mp3")
        assert "confidence_score" in result
        assert "details" in result
        assert result["file"] == "test.mp3"

def test_analyze_audio_file_not_found():
    result = analyze_audio("nonexistent.mp3")
    assert "error" in result
    assert result["file"] == "nonexistent.mp3"

def test_analyze_audio_invalid_file():
    with patch("pydub.AudioSegment.from_file", side_effect=Exception("Invalid file format")):
        result = analyze_audio("invalid.mp3")
        assert "error" in result
        assert result["file"] == "invalid.mp3"
