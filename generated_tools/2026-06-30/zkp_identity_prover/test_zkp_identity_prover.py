import pytest
import json
from unittest.mock import patch, mock_open
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from zkp_identity_prover import generate_zkp, verify_zkp

def test_generate_zkp():
    user_data = {"name": "Alice", "age": 30}
    private_key = RSA.generate(1024).export_key().decode()

    with patch("builtins.open", mock_open(read_data=private_key)) as mocked_file:
        with patch("os.path.exists", return_value=True):
            zkp = generate_zkp(user_data, "private_key.pem")
            assert "user_data" in zkp
            assert "signature" in zkp
            mocked_file.assert_called_once_with("private_key.pem", "r")

def test_verify_zkp_valid():
    user_data = {"name": "Alice", "age": 30}
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()

    user_data_str = json.dumps(user_data, sort_keys=True)
    hashed_data = SHA256.new(user_data_str.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(hashed_data).hex()

    zkp = {"user_data": user_data, "signature": signature}
    public_key_pem = public_key.export_key().decode()

    with patch("builtins.open", mock_open(read_data=public_key_pem)) as mocked_file:
        with patch("os.path.exists", return_value=True):
            assert verify_zkp(zkp, "public_key.pem") is True
            mocked_file.assert_called_once_with("public_key.pem", "r")

def test_verify_zkp_invalid():
    user_data = {"name": "Alice", "age": 30}
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()

    user_data_str = json.dumps(user_data, sort_keys=True)
    hashed_data = SHA256.new(user_data_str.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(hashed_data).hex()

    zkp = {"user_data": user_data, "signature": signature}
    public_key_pem = public_key.export_key().decode()

    # Modify the signature to make it invalid
    zkp["signature"] = "deadbeef"

    with patch("builtins.open", mock_open(read_data=public_key_pem)) as mocked_file:
        with patch("os.path.exists", return_value=True):
            assert verify_zkp(zkp, "public_key.pem") is False
            mocked_file.assert_called_once_with("public_key.pem", "r")
