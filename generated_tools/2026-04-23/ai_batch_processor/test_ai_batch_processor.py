import pytest
import os
from unittest.mock import patch, mock_open
from ai_batch_processor import process_task, process_file, batch_process

def test_process_task():
    with patch('ai_batch_processor.pipeline') as mock_pipeline:
        mock_model = mock_pipeline.return_value
        mock_model.return_value = [{'generated_text': 'Generated text'}]
        result = process_task('gpt-neo', 'Input text')
        assert result == 'Generated text'

def test_process_file():
    with patch('ai_batch_processor.open', mock_open(read_data='Input text')):
        with patch('ai_batch_processor.pipeline') as mock_pipeline:
            mock_model = mock_pipeline.return_value
            mock_model.return_value = [{'generated_text': 'Generated text'}]
            result = process_file('test.txt', 'gpt-neo')
            assert result == 'Generated text'

def test_batch_process():
    input_dir = 'test_inputs'
    output_dir = 'test_outputs'
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(input_dir, 'file1.txt'), 'w') as f:
        f.write('Input text 1')
    with open(os.path.join(input_dir, 'file2.txt'), 'w') as f:
        f.write('Input text 2')

    with patch('ai_batch_processor.process_file') as mock_process_file:
        mock_process_file.side_effect = lambda file, model: f"Processed {file}"
        batch_process(input_dir, output_dir, 'gpt-neo', max_workers=2)

    assert os.path.exists(os.path.join(output_dir, 'file1.txt.out'))
    assert os.path.exists(os.path.join(output_dir, 'file2.txt.out'))

    with open(os.path.join(output_dir, 'file1.txt.out'), 'r') as f:
        assert f.read() == 'Processed test_inputs/file1.txt'
    with open(os.path.join(output_dir, 'file2.txt.out'), 'r') as f:
        assert f.read() == 'Processed test_inputs/file2.txt'