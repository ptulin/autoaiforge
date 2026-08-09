import pytest
from unittest.mock import patch, MagicMock
from intent_discovery import load_data, extract_intents, extract_keywords

@pytest.fixture
def mock_spacy():
    with patch('spacy.load') as mock_load:
        yield mock_load

@pytest.fixture
def mock_sklearn():
    with patch('sklearn.cluster.KMeans') as mock_kmeans:
        yield mock_kmeans

def test_load_data(tmp_path):
    input_file = tmp_path / 'queries.txt'
    with open(input_file, 'w') as f:
        f.write('query1\nquery2\nquery3')
    queries = load_data(input_file)
    assert queries == ['query1', 'query2', 'query3']

def test_load_data_empty_file(tmp_path):
    input_file = tmp_path / 'queries.txt'
    with open(input_file, 'w') as f:
        f.write('')
    queries = load_data(input_file)
    assert queries == []

def test_load_data_file_not_found(tmp_path):
    input_file = tmp_path / 'queries.txt'
    queries = load_data(input_file)
    assert queries == []

def test_extract_intents(mock_spacy, mock_sklearn):
    queries = ['query1', 'query2', 'query3']
    mock_spacy.return_value = MagicMock()
    mock_sklearn.return_value = MagicMock()
    intents = extract_intents(queries)
    assert isinstance(intents, dict)

def test_extract_intents_empty_queries(mock_spacy, mock_sklearn):
    queries = []
    mock_spacy.return_value = MagicMock()
    mock_sklearn.return_value = MagicMock()
    intents = extract_intents(queries)
    assert isinstance(intents, dict)
    assert intents == {}

def test_extract_keywords(mock_spacy):
    intents = {0: ['query1', 'query2'], 1: ['query3']}
    mock_spacy.return_value = MagicMock()
    keywords = extract_keywords(intents)
    assert isinstance(keywords, dict)