import os
import pytest
from unittest.mock import patch, MagicMock
from synthetic_voice_dataset_auditor import process_dataset, analyze_file

def test_analyze_file_valid_audio():
    mock_model = MagicMock()
    mock_model.return_value = MagicMock()
    mock_model.return_value.numpy.return_value = [[0.8]]

    audio_data = [0.1, 0.2, 0.3]
    with patch("synthetic_voice_dataset_auditor.load_audio", return_value=(audio_data, 16000)):
        result = analyze_file("test.wav", mock_model, 0.5)
        assert result["file"] == "test.wav"
        assert result["error"] is None
        assert result["score"] == 0.8
        assert result["is_synthetic"] is True

def test_analyze_file_invalid_audio():
    mock_model = MagicMock()
    with patch("synthetic_voice_dataset_auditor.load_audio", return_value=(None, "Error loading file")):
        result = analyze_file("invalid.wav", mock_model, 0.5)
        assert result["file"] == "invalid.wav"
        assert result["error"] == "Error loading file"
        assert result["score"] is None
        assert result["is_synthetic"] is None

def test_process_dataset_no_files():
    with patch("os.listdir", return_value=[]):
        with patch("os.path.exists", return_value=True):
            with patch("tensorflow.keras.models.load_model", return_value=MagicMock()):
                with pytest.raises(ValueError, match="No audio files found in the directory."):
                    process_dataset("/fake_dir", "/fake_model", 0.5, "/fake_output.csv")