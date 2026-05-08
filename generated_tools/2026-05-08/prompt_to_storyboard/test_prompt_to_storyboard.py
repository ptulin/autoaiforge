import os
import pytest
from unittest.mock import patch, MagicMock
from prompt_to_storyboard import generate_storyboard

@pytest.fixture
def mock_openai_image_create():
    with patch('openai.Image.create') as mock_create:
        mock_response = MagicMock()
        mock_response.configure_mock(**{'data': [{'url': 'http://example.com/fake_image.png'}]})
        mock_create.return_value = mock_response
        yield mock_create

def test_generate_storyboard_creates_output_dir(mock_openai_image_create, tmp_path):
    prompt = "A spaceship lands on a mysterious planet"
    frames = 3
    style = "cyberpunk"
    output_dir = tmp_path / "storyboard"

    result_dir = generate_storyboard(prompt, frames, style, str(output_dir))

    assert os.path.exists(result_dir)
    assert len(os.listdir(result_dir)) == frames + 1  # Frames + descriptions.txt

def test_generate_storyboard_creates_images(mock_openai_image_create, tmp_path):
    prompt = "A spaceship lands on a mysterious planet"
    frames = 2
    style = "cyberpunk"
    output_dir = tmp_path / "storyboard"

    generate_storyboard(prompt, frames, style, str(output_dir))

    for i in range(1, frames + 1):
        assert os.path.exists(output_dir / f"frame_{i}.png")

def test_generate_storyboard_creates_description_file(mock_openai_image_create, tmp_path):
    prompt = "A spaceship lands on a mysterious planet"
    frames = 2
    style = "cyberpunk"
    output_dir = tmp_path / "storyboard"

    generate_storyboard(prompt, frames, style, str(output_dir))

    description_file = output_dir / "descriptions.txt"
    assert os.path.exists(description_file)
    with open(description_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == frames
        assert all([f"Frame {i + 1}:" in line for i, line in enumerate(lines)])