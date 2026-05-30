import pytest
from unittest.mock import patch, MagicMock
import torch
from llm_inference_profiler import profile_inference

def mock_model(*args, **kwargs):
    class MockModel:
        def __init__(self):
            self.device = 'cpu'

        def to(self, device):
            return self

        def __call__(self, *args, **kwargs):
            pass

    return MockModel()

def mock_tokenizer(*args, **kwargs):
    class MockTokenizer:
        def __call__(self, *args, **kwargs):
            return {"input_ids": torch.tensor([[1, 2, 3, 4, 5]])}

    return MockTokenizer()

@patch("llm_inference_profiler.AutoModelForCausalLM.from_pretrained", side_effect=mock_model)
@patch("llm_inference_profiler.AutoTokenizer.from_pretrained", side_effect=mock_tokenizer)
def test_profile_inference(mock_model_fn, mock_tokenizer_fn):
    # Test case 1: Valid inputs
    report = profile_inference(model_name="mock-model", batch_size=10, input_length=100, iterations=5, output_file=None)
    assert report is not None
    assert report["average_latency"] > 0
    assert report["throughput"] > 0

    # Test case 2: Edge case with batch_size=1
    report = profile_inference(model_name="mock-model", batch_size=1, input_length=50, iterations=3, output_file=None)
    assert report is not None
    assert report["average_latency"] > 0
    assert report["throughput"] > 0

    # Test case 3: Edge case with input_length=0
    report = profile_inference(model_name="mock-model", batch_size=5, input_length=0, iterations=2, output_file=None)
    assert report is not None
    assert report["average_latency"] > 0
    assert report["throughput"] > 0