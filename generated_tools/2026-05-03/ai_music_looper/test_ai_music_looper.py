import pytest
from unittest.mock import patch, MagicMock
from ai_music_looper import analyze_music, preview_loops

def test_analyze_music():
    with patch("librosa.load") as mock_load, \
         patch("librosa.onset.onset_strength") as mock_onset_strength, \
         patch("librosa.beat.beat_track") as mock_beat_track, \
         patch("librosa.frames_to_time") as mock_frames_to_time:

        # Mocking the return values
        mock_load.return_value = (MagicMock(), 22050)
        mock_onset_strength.return_value = MagicMock()
        mock_beat_track.return_value = (120, [0, 1, 2, 3, 4])
        mock_frames_to_time.return_value = [0.0, 1.0, 2.0, 3.0, 4.0]

        # Call the function
        result = analyze_music("test.mp3")

        # Assert the results
        assert result == [(0.0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 4.0)]

def test_analyze_music_invalid_file():
    with patch("librosa.load", side_effect=Exception("File not found")):
        with pytest.raises(RuntimeError, match="Error analyzing music file: File not found"):
            analyze_music("invalid.mp3")

def test_preview_loops(capsys):
    loop_points = [(0.0, 1.0), (1.0, 2.0)]
    preview_loops("test.mp3", loop_points)

    captured = capsys.readouterr()
    assert "Previewing loops for file: test.mp3" in captured.out
    assert "Loop from 0.00s to 1.00s" in captured.out
    assert "Loop from 1.00s to 2.00s" in captured.out