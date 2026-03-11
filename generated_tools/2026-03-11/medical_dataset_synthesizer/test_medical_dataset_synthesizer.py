import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from medical_dataset_synthesizer import generate_synthetic_image, save_image, generate_dataset

def test_generate_synthetic_image():
    image_size = 64
    disease_intensity = 50
    image = generate_synthetic_image(image_size, disease_intensity)
    assert image.shape == (image_size, image_size)
    assert image.dtype == np.uint8
    assert image.min() >= 0 and image.max() <= 255

def test_save_image(tmp_path):
    image = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
    output_path = tmp_path / "test_image.png"
    save_image(image, output_path)
    assert os.path.exists(output_path)

def test_generate_dataset(tmp_path):
    output_dir = tmp_path / "dataset"
    num_images = 5
    image_size = 64
    disease_intensity = 50

    with patch("medical_dataset_synthesizer.save_image", wraps=save_image) as mock_save_image:
        generate_dataset(output_dir, num_images, image_size, disease_intensity)

        # Check if directory is created
        assert os.path.exists(output_dir)

        # Check if the correct number of images is generated
        generated_images = [f for f in os.listdir(output_dir) if f.endswith(".png")]
        assert len(generated_images) == num_images

        # Check if the annotations file is created
        annotation_file = os.path.join(output_dir, "annotations.txt")
        assert os.path.exists(annotation_file)

        # Check if save_image was called the correct number of times
        assert mock_save_image.call_count == num_images
