import pytest
from unittest.mock import patch, mock_open
from secure_silo_manager import SecureSiloManager

def test_create_silo():
    manager = SecureSiloManager()
    manager.create_silo("test_silo")
    assert "test_silo" in manager.silos

def test_add_to_silo():
    manager = SecureSiloManager()
    manager.create_silo("test_silo")
    mock_data = b"test data"
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("secure_silo_manager.getpass", return_value="password"):
                manager.add_to_silo("test_silo", "test_file.txt", "admin")
    assert "admin" in manager.silos["test_silo"]

def test_retrieve_from_silo():
    manager = SecureSiloManager()
    manager.create_silo("test_silo")
    mock_data = b"test data"
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_data)):
            with patch("secure_silo_manager.getpass", return_value="password"):
                manager.add_to_silo("test_silo", "test_file.txt", "admin")
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("secure_silo_manager.getpass", return_value="password"):
            manager.retrieve_from_silo("test_silo", "admin", "output.txt")
            mocked_file().write.assert_called_once_with(mock_data)

def test_add_to_nonexistent_silo():
    manager = SecureSiloManager()
    with pytest.raises(ValueError, match="Silo does not exist."):
        manager.add_to_silo("nonexistent_silo", "test_file.txt", "admin")

def test_retrieve_from_nonexistent_silo():
    manager = SecureSiloManager()
    with pytest.raises(ValueError, match="Silo or role does not exist."):
        manager.retrieve_from_silo("nonexistent_silo", "admin", "output.txt")