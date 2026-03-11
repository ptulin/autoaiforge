import os
import pytest
import cv2
import numpy as np
from unittest.mock import patch, MagicMock
from radiology_image_preprocessor import normalize_image, resize_image, denoise_image, preprocess_image

def test_normalize_image():
    image = np.array([[0, 128, 255]], dtype=np.uint8)
    normalized = normalize_image(image)
    assert normalized.min() == 0.0
    assert normalized.max() == 1.0

def test_resize_image():
    image = np.ones((100, 100), dtype=np.uint8)
    resized = resize_image(image, 50, 50)
    assert resized.shape == (50, 50)

def test_denoise_image():
    image = np.random.rand(100, 100)
    denoised = denoise_image(image)
    assert denoised.shape == image.shape

@patch("cv2.imread", return_value=np.ones((100, 100), dtype=np.uint8))
@patch("cv2.imwrite")
def test_preprocess_image(mock_imwrite, mock_imread):
    preprocess_image("input_path", "output_path", 50, 50)
    mock_imread.assert_called_once_with("input_path", cv2.IMREAD_GRAYSCALE)
    mock_imwrite.assert_called_once()
    args, _ = mock_imwrite.call_args
    assert args[0] == "output_path"
    assert args[1].shape == (50, 50)