import pytest
from unittest.mock import patch, MagicMock
from ai_audio_authenticator import extract_features, generate_spectrogram, analyze_audio
import numpy as np

def test_extract_features():
    mock_audio = np.random.random(22050)  # Generate random audio data
    with patch('librosa.load', return_value=(mock_audio, 22050)):
        features = extract_features('test_audio.wav')
        assert len(features) == 4
        assert all(isinstance(f, float) for f in features)

def test_generate_spectrogram():
    mock_audio = np.random.random(22050)  # Generate random audio data
    with patch('librosa.load', return_value=(mock_audio, 22050)), \
         patch('matplotlib.pyplot.savefig') as mock_savefig:
        generate_spectrogram('test_audio.wav', 'output.png')
        mock_savefig.assert_called_once_with('output.png')

def test_analyze_audio():
    with patch('ai_audio_authenticator.extract_features', return_value=[0.1, 0.2, 0.3, 0.4]), \
         patch('ai_audio_authenticator.generate_spectrogram') as mock_generate_spectrogram:
        confidence = analyze_audio('test_audio.wav', plot=True)
        assert 0 <= confidence <= 1
        mock_generate_spectrogram.assert_called_once_with('test_audio.wav', 'test_audio_spectrogram.png')
