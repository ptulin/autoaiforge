import pytest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from dataset_silo_connector import load_silo, decrypt_data
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend

def pad_data(data: bytes) -> bytes:
    """Helper function to pad data to AES block size."""
    padder = PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def test_decrypt_data():
    key = b'\x00' * 32
    iv = b'\x00' * 16
    plaintext_data = b'col1,col2\n1,2\n3,4\n'
    padded_data = pad_data(plaintext_data)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    decrypted_data = decrypt_data(encrypted_data, key, iv)
    assert decrypted_data == plaintext_data

def test_load_silo_entire_file():
    plaintext_data = b'col1,col2\n1,2\n3,4\n'
    padded_data = pad_data(plaintext_data)

    key = b'\x00' * 32
    iv = b'\x00' * 16

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    mock_key_file = mock_open(read_data=key + iv)
    mock_encrypted_file = mock_open(read_data=encrypted_data)

    with patch("builtins.open", mock_key_file) as mocked_key_file:
        mocked_key_file.side_effect = [mock_key_file.return_value, mock_encrypted_file.return_value]
        with patch("os.path.exists", return_value=True):
            result = list(load_silo("dummy.enc", "dummy.key"))
            assert len(result) == 1
            assert isinstance(result[0], pd.DataFrame)
            assert result[0].shape == (2, 2)
            assert list(result[0].columns) == ['col1', 'col2']

def test_load_silo_chunked():
    plaintext_data = b'col1,col2\n1,2\n3,4\n'
    padded_data = pad_data(plaintext_data)

    key = b'\x00' * 32
    iv = b'\x00' * 16

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    mock_key_file = mock_open(read_data=key + iv)
    mock_encrypted_file = mock_open(read_data=encrypted_data)

    with patch("builtins.open", mock_key_file) as mocked_key_file:
        mocked_key_file.side_effect = [mock_key_file.return_value, mock_encrypted_file.return_value]
        with patch("os.path.exists", return_value=True):
            result = list(load_silo("dummy.enc", "dummy.key", chunk_size=1))
            assert len(result) == 2
            assert all(isinstance(chunk, pd.DataFrame) for chunk in result)
            assert result[0].shape == (1, 2)
            assert result[1].shape == (1, 2)