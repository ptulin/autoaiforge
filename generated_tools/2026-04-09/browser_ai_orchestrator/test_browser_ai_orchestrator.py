import pytest
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from browser_ai_orchestrator import BrowserAI

def test_open_url():
    with patch("browser_ai_orchestrator.webdriver.Chrome") as mock_driver:
        mock_instance = MagicMock()
        mock_driver.return_value = mock_instance

        ai = BrowserAI()
        ai.open_url("https://example.com")

        mock_instance.get.assert_called_once_with("https://example.com")
        ai.quit()

def test_click_element():
    with patch("browser_ai_orchestrator.webdriver.Chrome") as mock_driver:
        mock_instance = MagicMock()
        mock_driver.return_value = mock_instance
        mock_element = MagicMock()
        mock_instance.find_element.return_value = mock_element

        ai = BrowserAI()
        ai.open_url("https://example.com")
        ai.click_element("#test")

        mock_instance.find_element.assert_called_once_with(By.CSS_SELECTOR, "#test")
        mock_element.click.assert_called_once()
        ai.quit()

def test_fill_form():
    with patch("browser_ai_orchestrator.webdriver.Chrome") as mock_driver:
        mock_instance = MagicMock()
        mock_driver.return_value = mock_instance
        mock_element = MagicMock()
        mock_instance.find_element.return_value = mock_element

        ai = BrowserAI()
        ai.open_url("https://example.com")
        ai.fill_form("#input", "test value")

        mock_instance.find_element.assert_called_once_with(By.CSS_SELECTOR, "#input")
        mock_element.clear.assert_called_once()
        mock_element.send_keys.assert_called_once_with("test value")
        ai.quit()
