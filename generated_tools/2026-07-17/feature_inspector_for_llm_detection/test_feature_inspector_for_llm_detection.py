import pytest
from unittest.mock import patch, mock_open
from feature_inspector_for_llm_detection import extract_features, visualize_features
import argparse

def test_extract_features():
    text = "This is a test. This is only a test."
    features = extract_features(text)
    assert features["num_sentences"] == 2
    assert features["num_words"] == 11  # Corrected word count
    assert features["avg_sentence_length"] == 5.5
    assert "test" in features["word_frequency"]

def test_extract_features_empty_text():
    with pytest.raises(ValueError):
        extract_features("")

@patch("builtins.open", new_callable=mock_open, read_data="This is a test. This is only a test.")
def test_main(mock_file):
    with patch("feature_inspector_for_llm_detection.visualize_features") as mock_visualize:
        with patch("argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(input="test.txt", output=None)):
            from feature_inspector_for_llm_detection import main
            main()
            mock_visualize.assert_called()
