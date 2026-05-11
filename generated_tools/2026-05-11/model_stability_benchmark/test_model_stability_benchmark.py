import pytest
from unittest.mock import patch, MagicMock
from model_stability_benchmark import generate_responses, calculate_token_differences, calculate_semantic_similarity

def test_generate_responses():
    mock_api_key = "test_api_key"
    mock_prompt = "Test prompt"
    mock_iterations = 3

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(text="Response text")]

    with patch("openai.Completion.create", return_value=mock_response):
        responses = generate_responses(mock_api_key, mock_prompt, mock_iterations)
        assert len(responses) == mock_iterations
        assert all(response == "Response text" for response in responses)

def test_calculate_token_differences():
    responses = ["This is a test", "This is another test", "This test"]
    mean, std = calculate_token_differences(responses)
    assert mean > 0
    assert std >= 0

def test_calculate_semantic_similarity():
    responses = ["This is a test", "This is another test", "This test"]

    mock_embedding = MagicMock()
    mock_embedding.data = [{"embedding": [0.1, 0.2, 0.3]}, {"embedding": [0.1, 0.2, 0.3]}, {"embedding": [0.1, 0.2, 0.3]}]

    with patch("openai.Embedding.create", return_value=mock_embedding):
        mean, std = calculate_semantic_similarity(responses)
        assert mean == 1.0
        assert std == 0.0