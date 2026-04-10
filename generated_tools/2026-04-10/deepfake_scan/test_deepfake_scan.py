import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from deepfake_scan import analyze_media, save_heatmap

def mock_model(image):
    return 0.85, np.random.rand(*image.shape[:2])

def test_analyze_media_image():
    with patch('cv2.imread', return_value=np.ones((100, 100, 3), dtype=np.uint8)):
        confidence, heatmap = analyze_media('test.jpg', mock_model)
        assert 0 <= confidence <= 1
        assert heatmap.shape == (100, 100)

def test_analyze_media_invalid_file():
    with pytest.raises(ValueError, match="Invalid image file."):
        with patch('cv2.imread', return_value=None):
            analyze_media('invalid.jpg', mock_model)

def test_analyze_media_video():
    mock_capture = MagicMock()
    mock_capture.isOpened.return_value = True
    mock_capture.read.return_value = (True, np.ones((100, 100, 3), dtype=np.uint8))

    with patch('cv2.VideoCapture', return_value=mock_capture):
        confidence, heatmap = analyze_media('test.mp4', mock_model)
        assert 0 <= confidence <= 1
        assert heatmap.shape == (100, 100)

def test_save_heatmap(tmp_path):
    heatmap = np.random.rand(100, 100)
    output_path = tmp_path / 'heatmap.png'
    save_heatmap(heatmap, str(output_path))
    assert output_path.exists()