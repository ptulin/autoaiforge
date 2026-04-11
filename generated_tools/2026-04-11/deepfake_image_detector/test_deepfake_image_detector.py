import os
import pytest
from unittest.mock import patch, MagicMock
import torch
from deepfake_image_detector import analyze_image, process_images

def test_analyze_image():
    with patch("deepfake_image_detector.load_img", return_value=torch.zeros((3, 224, 224))), \
         patch("deepfake_image_detector.model", new_callable=MagicMock) as mock_model:
        mock_model.return_value = torch.tensor([[0.1, 0.9]])
        result = analyze_image("test_image.jpg")
        assert "deepfake_likelihood" in result
        assert 0 <= result["deepfake_likelihood"] <= 1

def test_process_images_single_file():
    with patch("os.path.isfile", return_value=True), \
         patch("deepfake_image_detector.analyze_image", return_value={"deepfake_likelihood": 0.8}):
        results = process_images("test_image.jpg")
        assert len(results) == 1
        assert results[0]["deepfake_likelihood"] == 0.8

def test_process_images_directory():
    with patch("os.path.isdir", return_value=True), \
         patch("os.listdir", return_value=["image1.jpg", "image2.png"]), \
         patch("os.path.isfile", side_effect=lambda x: x in ["test_directory/image1.jpg", "test_directory/image2.png"]), \
         patch("deepfake_image_detector.analyze_image", side_effect=[
             {"deepfake_likelihood": 0.7},
             {"deepfake_likelihood": 0.3}
         ]):
        results = process_images("test_directory")
        assert len(results) == 2
        assert results[0]["deepfake_likelihood"] == 0.7
        assert results[1]["deepfake_likelihood"] == 0.3
