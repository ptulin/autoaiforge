import pytest
from unittest.mock import patch, MagicMock
from llm_local_cache_manager import list_local_models, clean_unused_models, download_model

@patch("llm_local_cache_manager.Session")
def test_list_local_models(mock_session):
    mock_query = MagicMock()
    mock_model1 = MagicMock()
    mock_model1.name = "model1"
    mock_model1.version = "v1"
    mock_model1.path = "/path/to/model1"

    mock_model2 = MagicMock()
    mock_model2.name = "model2"
    mock_model2.version = "v2"
    mock_model2.path = "/path/to/model2"

    mock_query.all.return_value = [mock_model1, mock_model2]
    mock_session.return_value.query.return_value = mock_query

    models = list_local_models()
    assert models == [
        ("model1", "v1", "/path/to/model1"),
        ("model2", "v2", "/path/to/model2"),
    ]

@patch("llm_local_cache_manager.os.path.exists")
@patch("llm_local_cache_manager.Session")
def test_clean_unused_models(mock_session, mock_exists):
    mock_query = MagicMock()
    mock_model = MagicMock()
    mock_model.name = "model1"
    mock_model.version = "v1"
    mock_model.path = "/path/to/model1"
    mock_model.id = 1
    mock_query.all.return_value = [mock_model]
    mock_session.return_value.query.return_value = mock_query
    mock_exists.return_value = False

    removed = clean_unused_models()
    assert removed == ["model1"]

@patch("llm_local_cache_manager.snapshot_download")
@patch("llm_local_cache_manager.Session")
def test_download_model(mock_session, mock_snapshot_download):
    mock_snapshot_download.return_value = "/path/to/model"
    mock_session.return_value.add = MagicMock()
    mock_session.return_value.commit = MagicMock()

    result = download_model("model_name", "v1")
    assert result == "/path/to/model"
    mock_snapshot_download.assert_called_once_with(repo_id="model_name", revision="v1")
