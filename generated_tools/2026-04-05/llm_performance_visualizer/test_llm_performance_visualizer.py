import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from llm_performance_visualizer import load_dataset, evaluate_model, generate_visualizations

def test_load_dataset_csv():
    data = "text,label\nhello,positive\nworld,negative"
    with open('test.csv', 'w') as f:
        f.write(data)
    dataset = load_dataset('test.csv')
    assert len(dataset) == 2
    assert list(dataset.columns) == ['text', 'label']

def test_load_dataset_jsonl():
    data = '{"text": "hello", "label": "positive"}\n{"text": "world", "label": "negative"}'
    with open('test.jsonl', 'w') as f:
        f.write(data)
    dataset = load_dataset('test.jsonl')
    assert len(dataset) == 2
    assert list(dataset.columns) == ['text', 'label']

@patch('llm_performance_visualizer.pipeline')
def test_evaluate_model(mock_pipeline):
    mock_model = MagicMock()
    mock_model.return_value = [{'label': 'positive'}]
    mock_pipeline.return_value = mock_model

    dataset = pd.DataFrame({"text": ["hello"], "label": ["positive"]})
    evaluated_dataset = evaluate_model('gpt2', dataset, 'accuracy')
    assert len(evaluated_dataset) == 1
    assert evaluated_dataset['result'].iloc[0] == True

@patch('llm_performance_visualizer.plt.savefig')
def test_generate_visualizations(mock_savefig):
    dataset = pd.DataFrame({"text": ["hello", "world"], "label": ["positive", "negative"], "result": [1, 0]})
    heatmap_path, line_chart_path = generate_visualizations(dataset, 'accuracy', 'test_output')
    assert mock_savefig.call_count == 2
    assert heatmap_path == 'test_output/heatmap.png'
    assert line_chart_path == 'test_output/line_chart.png'