import pytest
from unittest.mock import patch, mock_open
from PIL import Image
from multi_modal_code_assist import process_text, process_image

@patch('builtins.open', new_callable=mock_open, read_data='mock code content')
def test_process_text(mock_file):
    result = process_text('mock_file.py')
    assert result == 'Mocked debugging insights for code.'

@patch('multi_modal_code_assist.Image.open')
def test_process_image(mock_image_open):
    mock_image_open.return_value = Image.new('RGB', (100, 100))
    result = process_image('mock_image.png')
    assert result == 'Mocked analysis for image.'

@patch('builtins.open', new_callable=mock_open)
def test_process_text_error(mock_file):
    mock_file.side_effect = Exception("File error")
    result = process_text('mock_file.py')
    assert "Error processing text file" in result

@patch('multi_modal_code_assist.Image.open')
def test_process_image_error(mock_image_open):
    mock_image_open.side_effect = Exception("Invalid image")
    result = process_image('mock_image.png')
    assert "Error processing image file" in result
