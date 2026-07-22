import pytest
from unittest.mock import patch, mock_open, MagicMock
from ai_storyboard_generator import parse_script, generate_image, download_image, create_pdf

def test_parse_script():
    mock_script = "Scene 1: A sunny day at the park.\n\nScene 2: A dark and stormy night."
    with patch("builtins.open", mock_open(read_data=mock_script)):
        with patch("os.path.exists", return_value=True):
            scenes = parse_script("mock_script.txt")
            assert len(scenes) == 2
            assert scenes[0] == "Scene 1: A sunny day at the park."
            assert scenes[1] == "Scene 2: A dark and stormy night."

@patch("ai_storyboard_generator.openai.Image.create")
def test_generate_image(mock_openai):
    mock_openai.return_value = {"data": [{"url": "http://example.com/image.png"}]}
    image_url = generate_image("A sunny day", "watercolor")
    assert image_url == "http://example.com/image.png"

@patch("ai_storyboard_generator.urlretrieve")
def test_download_image(mock_urlretrieve):
    mock_urlretrieve.return_value = None
    try:
        download_image("http://example.com/image.png", "output.png")
    except Exception as e:
        pytest.fail(f"download_image raised an exception: {e}")

def test_create_pdf():
    mock_canvas = MagicMock()
    with patch("ai_storyboard_generator.canvas.Canvas", return_value=mock_canvas):
        with patch("os.path.exists", return_value=True):
            create_pdf("output.pdf", ["image1.png", "image2.png"], ["Scene 1", "Scene 2"])
            assert mock_canvas.drawImage.call_count == 2
            assert mock_canvas.drawString.call_count == 2
            assert mock_canvas.showPage.call_count == 2
            mock_canvas.save.assert_called_once()
