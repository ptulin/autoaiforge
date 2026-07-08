import pytest
from unittest.mock import patch, mock_open
from ai_privacy_audit import scan_file, detect_pii

def test_detect_pii():
    nlp_mock = patch("ai_privacy_audit.load_spacy_model").start()()
    nlp_mock.return_value.ents = []
    text = "Contact me at john.doe@example.com or call 123-456-7890."
    results = detect_pii(text, nlp_mock)
    assert len(results) == 2
    assert ("email", "john.doe@example.com") in results
    assert ("phone", "123-456-7890") in results

@patch("builtins.open", new_callable=mock_open, read_data="Contact me at john.doe@example.com.")
def test_scan_file(mock_file):
    nlp_mock = patch("ai_privacy_audit.load_spacy_model").start()()
    nlp_mock.return_value.ents = []
    results = scan_file("test.log", pii_check=True)
    assert len(results) == 1
    assert ("email", "john.doe@example.com") in results

@patch("builtins.open", side_effect=FileNotFoundError)
def test_scan_file_file_not_found(mock_file):
    with pytest.raises(FileNotFoundError):
        scan_file("nonexistent.log", pii_check=True)
