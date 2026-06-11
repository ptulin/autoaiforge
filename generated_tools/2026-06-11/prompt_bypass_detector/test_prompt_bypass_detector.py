import pytest
from unittest.mock import patch, mock_open
import numpy as np
from prompt_bypass_detector import analyze_prompt

@pytest.fixture
def mock_model_and_vectorizer():
    class MockVectorizer:
        def transform(self, texts):
            return np.array([[0.1, 0.2], [0.3, 0.4]])

    class MockModel:
        def decision_function(self, features):
            return np.array([-0.5, 0.8])

        def predict(self, features):
            return np.array([-1, 1])

    vectorizer = MockVectorizer()
    model = MockModel()

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open()):
            with patch("pickle.load", side_effect=[model, vectorizer]):
                yield model, vectorizer

def test_analyze_prompt_safe(mock_model_and_vectorizer):
    result = analyze_prompt("This is a safe prompt.", "This is a safe response.")
    assert result == {
        "input_classification": "bypass",
        "response_classification": "safe",
        "input_anomaly_score": -0.5,
        "response_anomaly_score": 0.8
    }

def test_analyze_prompt_empty():
    result = analyze_prompt("", "")
    assert result == {"error": "Input prompt and model response cannot be empty."}

def test_analyze_prompt_missing_files():
    with patch("os.path.exists", return_value=False):
        result = analyze_prompt("Prompt", "Response")
        assert result == {"error": "Model or vectorizer files are missing."}

def test_analyze_prompt_model_load_error():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", side_effect=Exception("File read error")):
            result = analyze_prompt("Prompt", "Response")
            assert result == {"error": "Failed to load model or vectorizer: File read error"}

def test_analyze_prompt_vectorizer_transform_error():
    class MockVectorizerWithError:
        def transform(self, texts):
            raise Exception("Transform error")

    class MockModel:
        def decision_function(self, features):
            return np.array([-0.5, 0.8])

        def predict(self, features):
            return np.array([-1, 1])

    mock_model = MockModel()
    mock_vectorizer = MockVectorizerWithError()

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open()):
            with patch("pickle.load", side_effect=[mock_model, mock_vectorizer]):
                result = analyze_prompt("Prompt", "Response")
                assert result == {"error": "Failed to transform input: Transform error"}
