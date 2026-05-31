import pytest
from unittest.mock import patch, MagicMock, mock_open
from content_guard import classify_text, main
import sys

def test_classify_text():
    mock_classifier = MagicMock()
    mock_classifier.return_value = [
        {'label': 'TOXIC', 'score': 0.8},
        {'label': 'NON_TOXIC', 'score': 0.2}
    ]

    text = "This is a toxic comment."
    flagged = classify_text(text, mock_classifier)

    assert len(flagged) == 1
    assert flagged[0]['label'] == 'TOXIC'
    assert flagged[0]['score'] == 0.8

@patch('content_guard.pipeline')
def test_main_with_file(mock_pipeline):
    mock_classifier = MagicMock()
    mock_classifier.return_value = [
        {'label': 'TOXIC', 'score': 0.8}
    ]
    mock_pipeline.return_value = mock_classifier

    with patch('builtins.open', mock_open(read_data="This is a toxic comment.")) as mock_file:
        with patch.object(sys, 'argv', ['content_guard.py', '--input', 'input.txt', '--output', 'output.json']):
            main()
        mock_file.assert_called_with('output.json', 'w')

@patch('content_guard.pipeline')
def test_main_with_no_input(mock_pipeline):
    mock_pipeline.return_value = MagicMock()
    with patch.object(sys, 'argv', ['content_guard.py']):
        with pytest.raises(SystemExit):
            main()

@patch('content_guard.pipeline')
def test_main_with_invalid_input_file(mock_pipeline):
    mock_pipeline.return_value = MagicMock()
    with patch.object(sys, 'argv', ['content_guard.py', '--input', 'nonexistent.txt']):
        with pytest.raises(SystemExit):
            main()
