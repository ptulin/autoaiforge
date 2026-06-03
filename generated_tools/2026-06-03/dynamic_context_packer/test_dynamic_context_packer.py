import pytest
from unittest.mock import patch, mock_open
import dynamic_context_packer

def test_load_data():
    with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
        data = dynamic_context_packer.load_data(["test.json"])
        assert data == [{"key": "value"}]

def test_pack_context():
    data = [{"key": "value"}, ["item1", "item2"], "plain text"]
    packed = dynamic_context_packer.pack_context(data, max_tokens=50, rules="")
    assert "key: value" in packed
    assert "- item1" in packed
    assert "plain text" in packed

def test_save_output():
    with patch("builtins.open", mock_open()) as mocked_file:
        dynamic_context_packer.save_output("test output", "output.txt")
        mocked_file.assert_called_once_with("output.txt", "w")
        mocked_file().write.assert_called_once_with("test output")