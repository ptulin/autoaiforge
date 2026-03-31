import pytest
from unittest.mock import patch, MagicMock
from image_misinformation_checker import check_image, detect_gan_artifacts, extract_metadata, analyze_metadata

def test_check_image_file_not_found():
    result = check_image("non_existent_file.jpg")
    assert result == {"error": "File not found"}

def test_check_image_invalid_file():
    with patch("os.path.isfile", return_value=True):
        with patch("image_misinformation_checker.MagicMock", return_value=None):
            result = check_image("invalid_file.jpg")
            assert result == {"error": "Invalid image file"}

def test_check_image_valid():
    with patch("os.path.isfile", return_value=True):
        with patch("image_misinformation_checker.MagicMock", return_value=MagicMock()):
            with patch("image_misinformation_checker.detect_gan_artifacts", return_value=False):
                with patch("image_misinformation_checker.extract_metadata", return_value={"MockKey": "MockValue"}):
                    with patch("image_misinformation_checker.analyze_metadata", return_value=False):
                        result = check_image("valid_image.jpg")
                        assert result == {
                            "gan_artifacts_detected": False,
                            "metadata_discrepancies": False,
                            "file_path": "valid_image.jpg"
                        }

def test_detect_gan_artifacts():
    image_mock = MagicMock()
    result = detect_gan_artifacts(image_mock)
    assert result is False

def test_extract_metadata():
    result = extract_metadata("valid_image.jpg")
    assert result == {"MockKey": "MockValue"}

def test_analyze_metadata():
    metadata = {"MockKey": "MockValue"}
    result = analyze_metadata(metadata)
    assert result is False