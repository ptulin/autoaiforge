import pytest
import json
import numpy as np
from unittest.mock import patch, MagicMock, mock_open
from media_manipulation_detector import detect_fake_media

def test_detect_fake_media_image():
    with patch("cv2.imread", return_value=np.zeros((100, 100, 3), dtype=np.uint8)) as mock_read:
        with patch("builtins.open", mock_open()) as mock_open_file:
            result = detect_fake_media("test.jpg", "output.json")
            assert result["file_type"] == "image"
            assert result["anomalies_detected"] == False
            mock_read.assert_called_once_with("test.jpg")
            mock_open_file.assert_called_once_with("output.json", "w")

def test_detect_fake_media_video():
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.side_effect = [(True, np.zeros((100, 100, 3), dtype=np.uint8)), (False, None)]

    with patch("cv2.VideoCapture", return_value=mock_cap) as mock_video_capture:
        with patch("builtins.open", mock_open()) as mock_open_file:
            result = detect_fake_media("test.mp4", "output.json")
            assert result["file_type"] == "video"
            assert result["anomalies_detected"] == False
            mock_video_capture.assert_called_once_with("test.mp4")
            mock_open_file.assert_called_once_with("output.json", "w")

def test_detect_fake_media_file_not_found():
    with patch("cv2.imread", return_value=None):
        with pytest.raises(FileNotFoundError):
            detect_fake_media("nonexistent.jpg", "output.json")

def test_detect_fake_media_video_file_not_found():
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = False

    with patch("cv2.VideoCapture", return_value=mock_cap):
        with pytest.raises(FileNotFoundError):
            detect_fake_media("nonexistent.mp4", "output.json")

def test_detect_fake_media_invalid_image():
    with patch("cv2.imread", return_value=np.zeros((100, 100), dtype=np.uint8)) as mock_read:
        with pytest.raises(RuntimeError, match="Invalid image format"):
            detect_fake_media("invalid.jpg", "output.json")

def test_detect_fake_media_invalid_video_frame():
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.side_effect = [(True, np.zeros((100, 100), dtype=np.uint8)), (False, None)]

    with patch("cv2.VideoCapture", return_value=mock_cap):
        with pytest.raises(RuntimeError, match="Invalid frame format"):
            detect_fake_media("invalid.mp4", "output.json")
