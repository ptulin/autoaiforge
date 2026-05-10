import pytest
from unittest.mock import patch, MagicMock
import smart_glasses_ai_bridge
import pandas as pd
import os

def test_load_model():
    with patch('torch.hub.load', return_value=MagicMock()) as mock_load:
        model = smart_glasses_ai_bridge.load_model('yolov5s')
        mock_load.assert_called_once_with('ultralytics/yolov5', 'yolov5s', pretrained=True)
        assert model is not None

def test_process_frame():
    mock_model = MagicMock()
    mock_results = MagicMock()
    mock_results.pandas.return_value.xyxy = [pd.DataFrame([{'name': 'person', 'confidence': 0.9}])]
    mock_model.return_value = mock_results
    frame = MagicMock()

    detections = smart_glasses_ai_bridge.process_frame(frame, mock_model)
    assert not detections.empty
    assert 'name' in detections.columns
    assert 'confidence' in detections.columns

def test_text_to_speech():
    with patch('pyttsx3.init', return_value=MagicMock()) as mock_init:
        engine = mock_init.return_value
        smart_glasses_ai_bridge.text_to_speech("Test message")
        engine.say.assert_called_once_with("Test message")
        engine.runAndWait.assert_called_once()

def test_process_video():
    mock_model = MagicMock()
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.side_effect = [(True, MagicMock()), (False, None)]

    mock_detections = pd.DataFrame([{'name': 'person', 'confidence': 0.9}])

    with patch('cv2.VideoCapture', return_value=mock_cap) as mock_video_capture, \
         patch('smart_glasses_ai_bridge.load_model', return_value=mock_model), \
         patch('smart_glasses_ai_bridge.process_frame', return_value=mock_detections), \
         patch('smart_glasses_ai_bridge.text_to_speech') as mock_tts:

        # Set environment variable to mock display
        os.environ["TEST_ENV"] = "true"

        smart_glasses_ai_bridge.process_video('test_video.mp4', 'yolov5s')

        mock_video_capture.assert_called_once_with('test_video.mp4')
        mock_cap.isOpened.assert_called_once()
        mock_cap.read.assert_called()
        mock_tts.assert_called_once_with("Detected person with confidence 0.90")

        # Clean up environment variable
        del os.environ["TEST_ENV"]