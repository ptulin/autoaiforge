import pytest
from unittest.mock import patch, mock_open
from image_metadata_auditor import audit_metadata

def test_audit_metadata_valid_image():
    mock_exif_data = {
        'Image Make': 'Canon',
        'Image Model': 'EOS 80D',
        'EXIF DateTimeOriginal': '2023:10:01 12:00:00',
        'EXIF DateTimeDigitized': '2023:10:01 12:00:00'
    }

    with patch('os.path.isfile', return_value=True):
        with patch('builtins.open', mock_open(read_data=b"fake_image_data")) as mock_file:
            with patch('exifread.process_file', return_value=mock_exif_data):
                result = audit_metadata('test_image.jpg')

    assert result['metadata'] == mock_exif_data
    assert result['anomalies'] == []

def test_audit_metadata_missing_file():
    with patch('os.path.isfile', return_value=False):
        with pytest.raises(FileNotFoundError):
            audit_metadata('non_existent_image.jpg')

def test_audit_metadata_anomalies_detected():
    mock_exif_data = {
        'Image Software': 'AI Generated Tool',
        'EXIF DateTimeOriginal': '2023:10:01 12:00:00',
        'EXIF DateTimeDigitized': '2023:10:01 13:00:00',
        'Image Make': 'Canon',
        'Image Model': 'EOS 80D'
    }

    with patch('os.path.isfile', return_value=True):
        with patch('builtins.open', mock_open(read_data=b"fake_image_data")) as mock_file:
            with patch('exifread.process_file', return_value=mock_exif_data):
                result = audit_metadata('test_image.jpg')

    assert result['metadata'] == mock_exif_data
    assert len(result['anomalies']) == 2
    assert any("Potential AI or editing software detected" in anomaly for anomaly in result['anomalies'])
    assert any("Mismatch between original and digitized timestamps." in anomaly for anomaly in result['anomalies'])