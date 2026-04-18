import pytest
import json
from unittest.mock import patch, MagicMock
from claude_design_tester import validate_ui_design

def mock_webdriver_get(url):
    if "invalid" in url:
        raise Exception("Invalid URL")

def mock_webdriver_find_elements(by, value):
    if value == 'button':
        return [MagicMock(), MagicMock()]
    elif value == 'a':
        return [MagicMock()]
    return []

@patch('claude_design_tester.webdriver.Chrome')
def test_validate_ui_design_success(mock_chrome):
    mock_driver = MagicMock()
    mock_driver.get = mock_webdriver_get
    mock_driver.find_elements = mock_webdriver_find_elements
    mock_chrome.return_value = mock_driver

    report = validate_ui_design("http://example.com", "output.json")

    assert report["status"] == "success"
    assert report["button_count"] == 2
    assert report["link_count"] == 1

@patch('claude_design_tester.webdriver.Chrome')
def test_validate_ui_design_invalid_url(mock_chrome):
    mock_driver = MagicMock()
    mock_driver.get.side_effect = Exception("Invalid URL")
    mock_chrome.return_value = mock_driver

    report = validate_ui_design("http://invalid-url.com", "output.json")

    assert report["status"] == "error"
    assert "error_message" in report

@patch('claude_design_tester.webdriver.Chrome')
def test_validate_ui_design_local_file(mock_chrome):
    mock_driver = MagicMock()
    mock_driver.get = mock_webdriver_get
    mock_driver.find_elements = mock_webdriver_find_elements
    mock_chrome.return_value = mock_driver

    with patch('os.path.exists', return_value=True):
        report = validate_ui_design("test.html", "output.json")

    assert report["status"] == "success"
    assert report["button_count"] == 2
    assert report["link_count"] == 1