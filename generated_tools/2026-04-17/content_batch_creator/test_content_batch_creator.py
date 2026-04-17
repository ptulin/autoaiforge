import pytest
import os
import pandas as pd
from unittest.mock import patch, MagicMock
from content_batch_creator import process_csv

def mock_generate_image(prompt, output_path):
    with open(output_path, 'w') as f:
        f.write("Mock image content")

def mock_generate_video(prompt, duration, output_path):
    with open(output_path, 'w') as f:
        f.write("Mock video content")

@patch('content_batch_creator.generate_image', side_effect=mock_generate_image)
@patch('content_batch_creator.generate_video', side_effect=mock_generate_video)
def test_process_csv(mock_image, mock_video, tmp_path):
    input_csv = tmp_path / "input.csv"
    output_folder = tmp_path / "output"

    data = {
        'text_prompt': ["A beautiful sunset", "A futuristic city"],
        'video_duration': [5, 10]
    }
    df = pd.DataFrame(data)
    df.to_csv(input_csv, index=False)

    process_csv(input_csv, output_folder)

    assert os.path.exists(output_folder / "image_0.png")
    assert os.path.exists(output_folder / "video_0.mp4")
    assert os.path.exists(output_folder / "image_1.png")
    assert os.path.exists(output_folder / "video_1.mp4")

@patch('content_batch_creator.generate_image', side_effect=mock_generate_image)
@patch('content_batch_creator.generate_video', side_effect=mock_generate_video)
def test_empty_csv(mock_image, mock_video, tmp_path):
    input_csv = tmp_path / "input.csv"
    output_folder = tmp_path / "output"

    df = pd.DataFrame()
    df.to_csv(input_csv, index=False)

    process_csv(input_csv, output_folder)

    assert os.path.exists(output_folder)  # Folder should still be created
    assert len(os.listdir(output_folder)) == 0  # No files should be generated

@patch('content_batch_creator.generate_image', side_effect=mock_generate_image)
@patch('content_batch_creator.generate_video', side_effect=mock_generate_video)
def test_missing_columns(mock_image, mock_video, tmp_path):
    input_csv = tmp_path / "input.csv"
    output_folder = tmp_path / "output"

    data = {
        'wrong_column': ["A beautiful sunset"]
    }
    df = pd.DataFrame(data)
    df.to_csv(input_csv, index=False)

    with pytest.raises(KeyError, match="Input CSV must contain the following columns: {'text_prompt', 'video_duration'}"):
        process_csv(input_csv, output_folder)
