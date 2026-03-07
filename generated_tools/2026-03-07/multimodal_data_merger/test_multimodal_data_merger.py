import pytest
import os
import json
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from PIL import Image
from multimodal_data_merger import preprocess_text, preprocess_images, preprocess_audio, merge_data

def test_preprocess_text_csv():
    data = "id,text\n1,hello\n2,world"
    with open("test.csv", "w") as f:
        f.write(data)
    result = preprocess_text("test.csv")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    os.remove("test.csv")

def test_preprocess_images():
    os.makedirs("test_images", exist_ok=True)
    img = Image.new("RGB", (500, 500))
    img.save("test_images/test.jpg")

    result = preprocess_images("test_images", "processed_images")
    assert "test.jpg" in result
    assert os.path.exists(result["test.jpg"])

    os.remove("test_images/test.jpg")
    os.rmdir("test_images")
    os.remove(result["test.jpg"])
    os.rmdir("processed_images")

def test_preprocess_audio():
    os.makedirs("test_audio", exist_ok=True)
    with patch("librosa.load", return_value=(np.random.rand(22050), 22050)):
        with patch("numpy.save") as mock_save:
            result = preprocess_audio("test_audio", "processed_audio")
            assert len(result) == 0
            mock_save.assert_not_called()

    os.rmdir("test_audio")
    os.rmdir("processed_audio")

def test_merge_data():
    text_data = pd.DataFrame([{'id': '1', 'text': 'hello'}, {'id': '2', 'text': 'world'}])
    images_data = {'1': 'processed_images/1.jpg'}
    audio_data = {'2': 'processed_audio/2.npy'}

    result = merge_data(text_data, images_data, audio_data, 'id')
    assert len(result) == 2
    assert result[0]['image'] == 'processed_images/1.jpg'
    assert result[1]['audio'] == 'processed_audio/2.npy'