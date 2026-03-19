import pytest
import json
from unittest.mock import patch, mock_open
from api_cost_calculator import tokenize_text, calculate_cost, main

def test_tokenize_text():
    text = "Hello world!"
    tokens = tokenize_text(text, "gpt-4")
    assert isinstance(tokens, list)
    assert len(tokens) > 0

def test_calculate_cost():
    tokens = [1, 2, 3, 4, 5]
    pricing = {"gpt-4": 0.03}
    cost = calculate_cost(tokens, "gpt-4", pricing)
    assert cost == pytest.approx(0.00015)

@patch("builtins.open", new_callable=mock_open, read_data="Hello world!")
@patch("sys.stdin.read", return_value="Hello world!")
@patch("api_cost_calculator.json.load", return_value={"gpt-4": 0.03})
def test_main(mock_json_load, mock_stdin, mock_open_file):
    with patch("sys.argv", ["api_cost_calculator.py", "--input", "-", "--models", "gpt-4", "--pricing", "pricing.json"]):
        main()
        mock_json_load.assert_called_once()
        mock_stdin.assert_called_once()
        mock_open_file.assert_called()
