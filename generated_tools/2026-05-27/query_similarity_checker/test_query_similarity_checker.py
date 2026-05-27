import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from query_similarity_checker import calculate_similarity, read_queries_from_file

def test_calculate_similarity():
    mock_model = MagicMock()
    mock_model.encode.return_value = [[0.1, 0.2], [0.3, 0.4]]
    mock_util = MagicMock()
    mock_util.pytorch_cos_sim.return_value.cpu.return_value.numpy.return_value = [[1.0, 0.8], [0.8, 1.0]]

    with patch('query_similarity_checker.MagicMock', return_value=mock_model):
        with patch('query_similarity_checker.MagicMock', mock_util):
            queries = ["query1", "query2"]
            result = calculate_similarity(queries)
            assert isinstance(result, pd.DataFrame)
            assert result.shape == (2, 2)
            assert result.index.tolist() == queries
            assert result.columns.tolist() == queries
            assert result.loc["query1", "query2"] == 0.8

def test_read_queries_from_file(tmp_path):
    test_file = tmp_path / "queries.txt"
    test_file.write_text("query1\nquery2\nquery3\n")
    result = read_queries_from_file(str(test_file))
    assert result == ["query1", "query2", "query3"]

def test_read_queries_from_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_queries_from_file("non_existent_file.txt")
