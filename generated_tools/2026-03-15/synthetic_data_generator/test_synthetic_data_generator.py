import os
import pytest
from unittest.mock import patch, MagicMock
from synthetic_data_generator import generate_image_data, generate_text_data

def test_generate_image_data():
    with patch("PIL.Image.Image.save", MagicMock()):
        image_paths, labels = generate_image_data(num_samples=5, image_size=(64, 64), augment=False)
        assert len(image_paths) == 5
        assert len(labels) == 5
        assert all(isinstance(path, str) for path in image_paths)
        assert all(label.startswith("class_") for label in labels)

def test_generate_image_data_with_augmentation():
    with patch("PIL.Image.Image.save", MagicMock()):
        image_paths, labels = generate_image_data(num_samples=5, image_size=(64, 64), augment=True)
        assert len(image_paths) == 5
        assert len(labels) == 5
        assert all(isinstance(path, str) for path in image_paths)
        assert all(label.startswith("class_") for label in labels)

def test_generate_text_data():
    with patch("synthetic_data_generator.generate_text_data", return_value=(
        ["word1 word2 word3", "word4 word5 word1", "word2 word3 word4"],
        ["positive", "negative", "positive"]
    )):
        text_samples, labels = generate_text_data(num_samples=3, sentence_length=3, augment=False)
        assert len(text_samples) == 3
        assert len(labels) == 3
        assert all(isinstance(sentence, str) for sentence in text_samples)
        assert all(label in ["positive", "negative"] for label in labels)

def test_generate_text_data_with_augmentation():
    with patch("synthetic_data_generator.generate_text_data", return_value=(
        ["WORD1 WORD2 WORD3", "word4 word5 word1", "WORD2 WORD3 WORD4"],
        ["positive", "negative", "positive"]
    )):
        text_samples, labels = generate_text_data(num_samples=3, sentence_length=3, augment=True)
        assert len(text_samples) == 3
        assert len(labels) == 3
        assert all(isinstance(sentence, str) for sentence in text_samples)
        assert all(label in ["positive", "negative"] for label in labels)

def test_generate_image_data_output_dir():
    with patch("PIL.Image.Image.save", MagicMock()):
        output_dir = "test_output"
        generate_image_data(num_samples=3, image_size=(64, 64), augment=False, output_dir=output_dir)
        assert os.path.exists(output_dir)
        for file in os.listdir(output_dir):
            os.remove(os.path.join(output_dir, file))
        os.rmdir(output_dir)