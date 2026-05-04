import pytest
from unittest.mock import patch, MagicMock
from email_ai_sorter import connect_to_email, fetch_unread_emails, parse_email, classify_email, process_emails

def test_connect_to_email():
    with patch("imaplib.IMAP4_SSL") as mock_imap:
        mock_mail = MagicMock()
        mock_imap.return_value = mock_mail
        mock_mail.login.return_value = "OK"
        mail = connect_to_email("imap.test.com", "test@example.com", "password")
        assert mail is not None
        mock_imap.assert_called_once_with("imap.test.com")
        mock_mail.login.assert_called_once_with("test@example.com", "password")

def test_fetch_unread_emails():
    mock_mail = MagicMock()
    mock_mail.search.return_value = ("OK", [b"1 2 3"])
    email_ids = fetch_unread_emails(mock_mail)
    assert email_ids == [b"1", b"2", b"3"]
    mock_mail.search.assert_called_once_with(None, 'UNSEEN')

def test_parse_email():
    mock_mail = MagicMock()
    mock_mail.fetch.return_value = ("OK", [(None, b"Subject: Test\r\n\r\nBody")])
    subject, body = parse_email(mock_mail, b"1")
    assert subject == "Test"
    assert body == "Body"
    mock_mail.fetch.assert_called_once_with(b"1", '(RFC822)')

def test_classify_email():
    with patch("openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = MagicMock(choices=[MagicMock(message={"content": "work"})])
        category = classify_email("test_api_key", "Test Subject", "Test Body")
        assert category == "work"
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Classify the following email into categories (e.g., 'work', 'personal', 'urgent').\nSubject: Test Subject\nBody: Test Body\n"}]
        )

def test_process_emails():
    with patch("email_ai_sorter.connect_to_email") as mock_connect, \
         patch("email_ai_sorter.fetch_unread_emails") as mock_fetch, \
         patch("email_ai_sorter.parse_email") as mock_parse, \
         patch("email_ai_sorter.classify_email") as mock_classify:

        mock_mail = MagicMock()
        mock_connect.return_value = mock_mail
        mock_fetch.return_value = [b"1"]
        mock_parse.return_value = ("Test Subject", "Test Body")
        mock_classify.return_value = "work"

        processed_emails = process_emails("imap.test.com", "test@example.com", "password", "test_api_key")
        assert len(processed_emails) == 1
        assert processed_emails[0]["subject"] == "Test Subject"
        assert processed_emails[0]["category"] == "work"
        mock_connect.assert_called_once_with("imap.test.com", "test@example.com", "password")
        mock_fetch.assert_called_once_with(mock_mail)
        mock_parse.assert_called_once_with(mock_mail, b"1")
        mock_classify.assert_called_once_with("test_api_key", "Test Subject", "Test Body")