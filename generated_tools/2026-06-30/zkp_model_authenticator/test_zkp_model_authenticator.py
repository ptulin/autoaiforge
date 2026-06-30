import pytest
import os
import json
from unittest.mock import patch, mock_open
from zkp_model_authenticator import generate_proof, verify_proof
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import hashlib

def test_generate_proof(tmp_path):
    # Create temporary files for model and private key
    model_path = tmp_path / "model.pth"
    private_key_path = tmp_path / "private_key.pem"
    proof_path = tmp_path / "proof.json"

    model_content = b"dummy model content"
    with open(model_path, "wb") as f:
        f.write(model_content)

    key = RSA.generate(2048)
    private_key = key.export_key()
    with open(private_key_path, "wb") as f:
        f.write(private_key)

    # Generate proof
    proof_file = generate_proof(str(model_path), str(private_key_path), str(proof_path))

    # Verify proof file exists
    assert os.path.exists(proof_file)

    # Verify proof content
    with open(proof_file, "r") as f:
        proof_data = json.load(f)

    model_hash = hashlib.sha256(model_content).hexdigest()
    assert proof_data["model_hash"] == model_hash

    hash_obj = SHA256.new(model_hash.encode("utf-8"))
    signature = bytes.fromhex(proof_data["signature"])
    pkcs1_15.new(key).verify(hash_obj, signature)

def test_verify_proof_valid(tmp_path):
    # Create temporary files for model, keys, and proof
    model_path = tmp_path / "model.pth"
    private_key_path = tmp_path / "private_key.pem"
    public_key_path = tmp_path / "public_key.pem"
    proof_path = tmp_path / "proof.json"

    model_content = b"dummy model content"
    with open(model_path, "wb") as f:
        f.write(model_content)

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(private_key_path, "wb") as f:
        f.write(private_key)

    with open(public_key_path, "wb") as f:
        f.write(public_key)

    # Generate proof
    generate_proof(str(model_path), str(private_key_path), str(proof_path))

    # Verify proof
    assert verify_proof(str(model_path), str(public_key_path), str(proof_path))

def test_verify_proof_invalid_signature(tmp_path):
    # Create temporary files for model, keys, and proof
    model_path = tmp_path / "model.pth"
    private_key_path = tmp_path / "private_key.pem"
    public_key_path = tmp_path / "public_key.pem"
    proof_path = tmp_path / "proof.json"

    model_content = b"dummy model content"
    with open(model_path, "wb") as f:
        f.write(model_content)

    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(private_key_path, "wb") as f:
        f.write(private_key)

    with open(public_key_path, "wb") as f:
        f.write(public_key)

    # Generate proof
    generate_proof(str(model_path), str(private_key_path), str(proof_path))

    # Tamper with proof file
    with open(proof_path, "r") as f:
        proof_data = json.load(f)
    proof_data["model_hash"] = "tampered_hash"
    with open(proof_path, "w") as f:
        json.dump(proof_data, f)

    # Verify proof should fail
    assert not verify_proof(str(model_path), str(public_key_path), str(proof_path))