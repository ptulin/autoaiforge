import pytest
from unittest.mock import patch, MagicMock
from agent_health_monitor import monitor_agent, send_email_alert
import psutil

def test_monitor_agent_no_process():
    with patch('psutil.Process', side_effect=psutil.NoSuchProcess(pid=99999)):
        monitor_agent(99999)

def test_monitor_agent_metrics():
    mock_process = MagicMock()
    mock_process.cpu_percent.return_value = 50
    mock_process.memory_info.return_value = MagicMock(rss=1024 * 1024 * 500)

    with patch('psutil.Process', return_value=mock_process):
        monitor_agent(12345, duration=5)

    mock_process.cpu_percent.assert_called()
    mock_process.memory_info.assert_called()

def test_send_email_alert():
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        send_email_alert('test@example.com', 'Test Subject', 'Test Message')

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('your_username', 'your_password')
        mock_server.sendmail.assert_called_once_with(
            'monitor@example.com',
            'test@example.com',
            'Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\nSubject: Test Subject\nFrom: monitor@example.com\nTo: test@example.com\n\nTest Message'
        )
