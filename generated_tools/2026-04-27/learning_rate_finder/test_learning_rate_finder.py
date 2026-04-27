import pytest
from unittest.mock import patch, MagicMock
import torch
from learning_rate_finder import load_dataset, prepare_data, learning_rate_range_test

def test_load_dataset():
    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value = iter(['{"text": "example", "label": 0}\n'])
        dataset = load_dataset('dummy_path.jsonl')
        assert len(dataset) == 1
        assert dataset[0]['text'] == 'example'
        assert dataset[0]['label'] == 0

    with pytest.raises(FileNotFoundError):
        load_dataset('non_existent.jsonl')

    with patch('builtins.open', new_callable=MagicMock) as mock_open:
        mock_open.return_value.__enter__.return_value = iter(['invalid json'])
        with pytest.raises(ValueError):
            load_dataset('dummy_path.jsonl')

def test_prepare_data():
    tokenizer_mock = MagicMock()
    tokenizer_mock.return_value = {'input_ids': [[1, 2, 3]], 'attention_mask': [[1, 1, 1]]}
    dataset = [{'text': 'example', 'label': 0}]
    tokenizer_mock.side_effect = lambda texts, truncation, padding, max_length: {
        'input_ids': [[1, 2, 3]],
        'attention_mask': [[1, 1, 1]]
    }
    result = prepare_data(dataset, tokenizer_mock)
    assert len(result) == 1
    assert 'input_ids' in result[0]
    assert 'attention_mask' in result[0]
    assert 'labels' in result[0]

def test_learning_rate_range_test():
    with patch('learning_rate_finder.AutoTokenizer.from_pretrained') as tokenizer_mock, \
         patch('learning_rate_finder.AutoModelForSequenceClassification.from_pretrained') as model_mock, \
         patch('learning_rate_finder.load_dataset') as load_dataset_mock, \
         patch('learning_rate_finder.prepare_data') as prepare_data_mock, \
         patch('learning_rate_finder.DataLoader') as dataloader_mock, \
         patch('matplotlib.pyplot.savefig') as savefig_mock:

        load_dataset_mock.return_value = [{'text': 'example', 'label': 0}]
        tokenizer_mock.return_value = MagicMock()
        model_instance_mock = MagicMock()
        model_instance_mock.parameters.return_value = [torch.tensor([1.0], requires_grad=True)]
        model_instance_mock.return_value = MagicMock()
        model_instance_mock.return_value.loss = MagicMock()
        model_instance_mock.return_value.loss.item.return_value = 0.5
        model_mock.return_value = model_instance_mock
        prepare_data_mock.return_value = [{'input_ids': torch.tensor([1, 2, 3]), 'attention_mask': torch.tensor([1, 1, 1]), 'labels': torch.tensor([0])}]
        dataloader_mock.return_value = iter([{
            'input_ids': torch.tensor([[1, 2, 3]]),
            'attention_mask': torch.tensor([[1, 1, 1]]),
            'labels': torch.tensor([0])
        }])

        learning_rate_range_test('dummy_model', 'dummy_dataset.jsonl', 1e-5, 1e-1, 'dummy_plot.png')

        savefig_mock.assert_called_once_with('dummy_plot.png')
