import pytest
from unittest.mock import patch, MagicMock, mock_open
from stealth_browser_driver import setup_browser, execute_script

def test_setup_browser_chrome():
    with patch('stealth_browser_driver.webdriver.Chrome') as mock_chrome:
        mock_browser = MagicMock()
        mock_chrome.return_value = mock_browser
        browser = setup_browser("chrome")
        assert browser == mock_browser
        mock_chrome.assert_called_once()

def test_setup_browser_invalid():
    with pytest.raises(ValueError, match="Currently, only Chrome is supported."):
        setup_browser("firefox")

def test_execute_script_valid():
    mock_browser = MagicMock()
    script_content = "browser.get('https://example.com')"
    with patch("builtins.open", mock_open(read_data=script_content)) as mock_file, \
         patch("os.path.exists", return_value=True):
        execute_script(mock_browser, "test_script.py")
        mock_browser.get.assert_called_once_with('https://example.com')
        mock_file.assert_called_once_with("test_script.py", 'r')

def test_execute_script_missing_file():
    mock_browser = MagicMock()
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError, match="Interaction script not found"):
            execute_script(mock_browser, "non_existent_script.py")