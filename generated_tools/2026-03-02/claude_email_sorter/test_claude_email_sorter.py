import pytest
import unittest.mock as mock
from claude_email_sorter import connect_to_imap, fetch_emails, parse_email, classify_email, save_to_csv

def test_connect_to_imap():
    with mock.patch("imaplib.IMAP4_SSL") as mock_imap:
        mock_imap.return_value.login.return_value = "OK"
        mail = connect_to_imap("imap.example.com", "user@example.com", "password")
        assert mail is not None

def test_fetch_emails():
    mock_mail = mock.Mock()
    mock_mail.select.return_value = ("OK", [b"1 2 3"])
    mock_mail.search.return_value = ("OK", [b"1 2 3"])
    email_ids = fetch_emails(mock_mail)
    assert email_ids == [b"1", b"2", b"3"]

def test_parse_email():
    mock_mail = mock.Mock()
    mock_mail.fetch.return_value = ("OK", [(None, b"Subject: Test\n\nBody")])
    subject, content = parse_email(mock_mail, b"1")
    assert subject == "Test"
    assert content == b"Body"

def test_classify_email():
    with mock.patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"category": "Urgent"}
        mock_post.return_value.raise_for_status.return_value = None
        category = classify_email("Test email content", "http://api.claude.ai", "fake_api_key")
        assert category == "Urgent"

def test_save_to_csv(tmp_path):
    test_file = tmp_path / "test_output.csv"
    email_categories = [("Subject 1", "Urgent"), ("Subject 2", "Follow-up")]
    save_to_csv(test_file, email_categories)
    with open(test_file, "r") as file:
        lines = file.readlines()
        assert lines[0].strip() == "Email Subject,Category"
        assert lines[1].strip() == "Subject 1,Urgent"
        assert lines[2].strip() == "Subject 2,Follow-up"