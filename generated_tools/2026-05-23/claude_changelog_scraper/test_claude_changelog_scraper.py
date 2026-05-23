import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from claude_changelog_scraper import fetch_updates, parse_updates
import requests

def test_fetch_updates_success():
    with patch('claude_changelog_scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        result = fetch_updates('https://example.com')
        assert result == '<html></html>'

def test_fetch_updates_failure():
    with patch('claude_changelog_scraper.requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException("Network error")

        with pytest.raises(RuntimeError, match="Error fetching updates"):
            fetch_updates('https://example.com')

def test_parse_updates():
    html_content = '''
    <html>
        <body>
            <div class="update">
                <h2>Update 1</h2>
                <time>2023-10-01</time>
                <p>Improved performance and bug fixes.</p>
            </div>
            <div class="update">
                <h2>Update 2</h2>
                <time>2023-09-15</time>
                <p>New API features added.</p>
            </div>
        </body>
    </html>
    '''
    keywords = ['performance']
    date_range = (datetime(2023, 9, 1), datetime(2023, 10, 1))

    result = parse_updates(html_content, keywords, date_range)
    assert len(result) == 1
    assert result[0]['title'] == 'Update 1'
    assert result[0]['date'] == '2023-10-01'
    assert result[0]['description'] == 'Improved performance and bug fixes.'