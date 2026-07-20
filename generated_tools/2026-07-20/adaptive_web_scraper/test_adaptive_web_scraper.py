import pytest
from unittest.mock import patch, MagicMock
from adaptive_web_scraper import scrape_data, fetch_html_with_requests, fetch_html_with_selenium
import os
import json

def test_fetch_html_with_requests():
    with patch('adaptive_web_scraper.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = '<html><head><title>Test</title></head><body></body></html>'
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        html, response_time = fetch_html_with_requests('https://example.com', {})

        assert html == '<html><head><title>Test</title></head><body></body></html>'
        assert response_time is not None

def test_fetch_html_with_selenium():
    with patch('adaptive_web_scraper.webdriver.Chrome') as mock_chrome:
        mock_driver = MagicMock()
        mock_driver.page_source = '<html><head><title>Test</title></head><body></body></html>'
        mock_chrome.return_value = mock_driver

        html, response_time = fetch_html_with_selenium('https://example.com', 'chrome')

        assert html == '<html><head><title>Test</title></head><body></body></html>'
        assert response_time is not None

def test_scrape_data(tmp_path):
    output_file = tmp_path / "output.json"

    with patch('adaptive_web_scraper.fetch_html_with_requests') as mock_requests:
        mock_requests.return_value = ('<html><head><title>Test</title></head><body><h1>Header</h1><a href="https://link.com">Link</a></body></html>', 1)

        scrape_data('https://example.com', str(output_file), 'chrome')

        assert output_file.exists()
        with open(output_file, 'r') as f:
            data = json.load(f)
            assert data['title'] == 'Test'
            assert data['headings'] == ['Header']
            assert data['links'] == ['https://link.com']