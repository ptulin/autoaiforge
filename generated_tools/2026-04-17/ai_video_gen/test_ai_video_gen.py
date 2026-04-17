import pytest
from unittest.mock import patch, MagicMock
from ai_video_gen import generate_video
import os

def test_generate_video_success():
    with patch("ai_video_gen.pipeline") as mock_pipeline, \
         patch("ai_video_gen.imageio.mimwrite") as mock_mimwrite, \
         patch("os.path.exists", return_value=True):

        mock_pipeline.return_value = MagicMock(return_value=[b"frame1", b"frame2"])
        mock_mimwrite.return_value = None

        result = generate_video(
            image_path="test_image.jpg",
            text_description="A serene beach at sunset",
            duration=5,
            output_path="output.mp4",
            style="default"
        )

        assert result == "output.mp4"
        mock_pipeline.assert_called_once()
        mock_mimwrite.assert_called_once()

def test_generate_video_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            generate_video(
                image_path="non_existent_image.jpg",
                text_description="A serene beach at sunset",
                duration=5,
                output_path="output.mp4",
                style="default"
            )

def test_generate_video_invalid_duration():
    with patch("os.path.exists", return_value=True):
        with pytest.raises(ValueError):
            generate_video(
                image_path="test_image.jpg",
                text_description="A serene beach at sunset",
                duration=0,
                output_path="output.mp4",
                style="default"
            )