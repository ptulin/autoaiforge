import pytest
import os
import hashlib
from unittest.mock import patch, mock_open
from ai_code_watermarker import embed_watermark, generate_watermark, process_file

def test_generate_watermark():
    identifier = "test_identifier"
    expected_hash = hashlib.sha256(identifier.encode()).hexdigest()
    assert generate_watermark(identifier) == expected_hash

def test_embed_watermark():
    content = "print('Hello, World!')"
    watermark = "test_watermark"
    result = embed_watermark(content, watermark)
    assert result.endswith(f"# Watermark: {watermark}")

def test_process_file():
    mock_content = "print('Hello, World!')"
    watermark = "test_watermark"
    output_dir = "mock_output"
    file_name = "mock_file.py"
    file_path = os.path.join(output_dir, file_name)

    with patch("builtins.open", mock_open(read_data=mock_content)) as mock_file:
        process_file(file_name, output_dir, watermark)

        mock_file.assert_called_with(file_path, 'w')
        mock_file().write.assert_called_once()
