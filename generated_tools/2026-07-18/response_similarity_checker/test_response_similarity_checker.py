import pytest
from unittest.mock import patch
import numpy as np
from response_similarity_checker import evaluate_similarity

def test_evaluate_similarity_bleu():
    responses = ["The cat is on the mat.", "The dog is in the house."]
    references = ["The cat is on the mat.", "The dog is inside the house."]
    scores = evaluate_similarity(responses, references, metric='bleu')
    assert len(scores) == 2
    assert scores[0] == pytest.approx(1.0, rel=1e-2)  # Exact match
    assert scores[1] > 0.2  # Partial match (adjusted threshold)

def test_evaluate_similarity_cosine():
    responses = [np.array([1, 0, 0]), np.array([0, 1, 0])]
    references = [np.array([1, 0, 0]), np.array([0, 1, 0])]
    scores = evaluate_similarity(responses, references, metric='cosine')
    assert len(scores) == 2
    assert scores[0] == pytest.approx(1.0, rel=1e-2)  # Exact match
    assert scores[1] == pytest.approx(1.0, rel=1e-2)  # Exact match

def test_evaluate_similarity_invalid_metric():
    responses = ["The cat is on the mat."]
    references = ["The cat is on the mat."]
    with pytest.raises(ValueError, match="Supported metrics are 'cosine' and 'bleu'."):
        evaluate_similarity(responses, references, metric='invalid')

def test_evaluate_similarity_mismatched_lengths():
    responses = ["The cat is on the mat."]
    references = ["The cat is on the mat.", "Extra reference"]
    with pytest.raises(ValueError, match="The number of responses and references must be equal."):
        evaluate_similarity(responses, references, metric='bleu')

def test_evaluate_similarity_cosine_invalid_input():
    responses = ["string instead of vector"]
    references = [np.array([1, 0, 0])]
    with pytest.raises(ValueError, match="Cosine similarity requires vector inputs, not strings."):
        evaluate_similarity(responses, references, metric='cosine')