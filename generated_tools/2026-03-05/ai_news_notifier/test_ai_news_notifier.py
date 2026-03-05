import pytest
from unittest.mock import patch, Mock
from ai_news_notifier import fetch_news, send_email_notification, send_desktop_notification

def test_fetch_news():
    mock_response = Mock()
    mock_response.json.return_value = {
        'articles': [
            {'title': 'OpenAI launches new GPT model', 'url': 'http://example.com/1'},
            {'title': 'Another news', 'url': 'http://example.com/2'}
        ]
    }
    mock_response.raise_for_status = Mock()

    with patch('requests.get', return_value=mock_response):
        keywords = ['OpenAI']
        sources = ['http://example.com/news']
        articles = fetch_news(keywords, sources)
        assert len(articles) == 1
        assert articles[0]['title'] == 'OpenAI launches new GPT model'

def test_send_email_notification():
    email_config = {
        'smtp_server': 'smtp.example.com',
        'smtp_port': 587,
        'username': 'user@example.com',
        'password': 'password',
        'to': 'recipient@example.com'
    }
    articles = [{'title': 'OpenAI launches new GPT model', 'url': 'http://example.com/1'}]

    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.starttls = Mock()
        mock_smtp_instance.login = Mock()
        mock_smtp_instance.sendmail = Mock()
        mock_smtp_instance.__enter__.return_value = mock_smtp_instance

        send_email_notification(email_config, articles)

        mock_smtp.assert_called_once_with('smtp.example.com', 587)
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('user@example.com', 'password')
        mock_smtp_instance.sendmail.assert_called_once_with(
            'user@example.com',
            'recipient@example.com',
            'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: AI News Alert\nFrom: user@example.com\nTo: recipient@example.com\n\nOpenAI launches new GPT model\nhttp://example.com/1'
        )

def test_send_desktop_notification():
    articles = [{'title': 'OpenAI launches new GPT model', 'url': 'http://example.com/1'}]

    with patch('plyer.notification.notify') as mock_notify:
        send_desktop_notification(articles)
        mock_notify.assert_called_once_with(
            title='AI News Alert',
            message='OpenAI launches new GPT model',
            app_name='AI News Notifier'
        )