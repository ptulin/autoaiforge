import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from pathfinder_navigation_assist import load_point_cloud, detect_obstacles, generate_audio_feedback, play_audio_feedback

def test_load_point_cloud_valid_file():
    with patch("pathfinder_navigation_assist.os.path.exists", return_value=True):
        point_cloud = load_point_cloud("valid_file.pcd")
        assert point_cloud.shape == (100, 3)

def test_load_point_cloud_file_not_found():
    with patch("pathfinder_navigation_assist.os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_point_cloud("nonexistent_file.pcd")

def test_detect_obstacles():
    point_cloud = np.array([[0.5, 0.5, 0.5], [2, 2, 2], [0.3, 0.3, 0.3]])
    obstacles = detect_obstacles(point_cloud, threshold=1.0)
    assert len(obstacles) == 2

def test_generate_audio_feedback_no_obstacles():
    obstacles = np.array([])
    audio_signal = generate_audio_feedback(obstacles)
    assert len(audio_signal) == 44100
    assert np.all(audio_signal == 0)

def test_generate_audio_feedback_with_obstacles():
    obstacles = np.array([[0.5, 0.5, 0.5]])
    audio_signal = generate_audio_feedback(obstacles)
    assert len(audio_signal) == 44100
    assert not np.all(audio_signal == 0)

def test_play_audio_feedback():
    audio_signal = np.zeros(44100)
    with patch("pathfinder_navigation_assist.print") as mock_print:
        play_audio_feedback(audio_signal)
        mock_print.assert_called_once_with("Playing audio feedback...")