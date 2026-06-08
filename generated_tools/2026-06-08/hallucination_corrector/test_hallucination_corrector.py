import pytest
from unittest.mock import patch
from hallucination_corrector import correct_hallucinations

def mock_wikipedia_page(title):
    class MockPage:
        def __init__(self, exists):
            self.exists = lambda: exists
            self.fullurl = "https://en.wikipedia.org/wiki/Valid_Article"

    if "valid" in title.lower():
        return MockPage(True)
    return MockPage(False)

@patch("wikipediaapi.Wikipedia.page", side_effect=mock_wikipedia_page)
def test_correct_hallucinations(mock_page):
    # Test case 1: Valid sentence
    text = "This is a valid sentence about a valid topic."
    result = correct_hallucinations(text)
    assert len(result["flagged_hallucinations"]) == 0
    assert len(result["suggested_corrections"]) == 1
    assert "https://en.wikipedia.org/wiki/Valid_Article" in result["suggested_corrections"][0]["suggestion"]

    # Test case 2: Invalid sentence
    text = "This is a hallucinated sentence."
    result = correct_hallucinations(text)
    assert len(result["flagged_hallucinations"]) == 1
    assert "No reliable information found" in result["suggested_corrections"][0]["suggestion"]

    # Test case 3: Empty input
    text = ""
    result = correct_hallucinations(text)
    assert result["original_text"] == ""
    assert len(result["flagged_hallucinations"]) == 0
    assert len(result["suggested_corrections"]) == 0