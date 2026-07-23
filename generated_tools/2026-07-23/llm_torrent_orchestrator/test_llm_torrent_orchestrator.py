import pytest
from unittest.mock import patch, MagicMock
import os
from llm_torrent_orchestrator import create_torrent, download_torrent

def test_create_torrent(tmp_path):
    file_path = tmp_path / "test_model.bin"
    file_path.write_text("dummy data")

    trackers = ["http://tracker1.com/announce", "http://tracker2.com/announce"]

    torrent_file = create_torrent(str(file_path), trackers)

    assert os.path.exists(torrent_file)
    assert torrent_file.endswith(".torrent")

def test_create_torrent_missing_file():
    with pytest.raises(FileNotFoundError):
        create_torrent("non_existent_file.bin", ["http://tracker.com/announce"])

@patch("llm_torrent_orchestrator.lt.session", autospec=True)
@patch("llm_torrent_orchestrator.lt.torrent_info", autospec=True)
@patch("llm_torrent_orchestrator.lt.sleep", autospec=True)
def test_download_torrent(mock_sleep, mock_torrent_info, mock_session, tmp_path):
    torrent_file = tmp_path / "test.torrent"
    torrent_file.write_text("dummy torrent data")

    mock_info = MagicMock()
    mock_info.name.return_value = "mock_file_name"
    mock_torrent_info.return_value = mock_info

    mock_handle = MagicMock()
    mock_handle.is_seed.side_effect = [False, False, True]

    mock_session.return_value.add_torrent.return_value = mock_handle

    download_torrent(str(torrent_file))

    mock_session.assert_called_once()
    mock_handle.is_seed.assert_called()
    mock_session.return_value.add_torrent.assert_called_once()
    mock_torrent_info.assert_called_once_with(str(torrent_file))