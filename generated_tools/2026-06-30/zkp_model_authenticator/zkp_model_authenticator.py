import os
import hashlib
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_proof(model_path, private_key_path, proof_path="proof.json"):
    """
    Generates a zero-knowledge proof for the given model file.

    Args:
        model_path (str): Path to the AI model file.
        private_key_path (str): Path to the private key file.
        proof_path (str): Path to save the generated proof file.

    Returns:
        str: Path to the generated proof file.

    Raises:
        FileNotFoundError: If the model file or private key file does not exist.
        ValueError: If there is an error in proof generation.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found.")

    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"Private key file '{private_key_path}' not found.")

    # Compute the hash of the model file
    hasher = hashlib.sha256()
    with open(model_path, "rb") as model_file:
        while chunk := model_file.read(8192):
            hasher.update(chunk)
    model_hash = hasher.hexdigest()

    # Load the private key
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = RSA.import_key(key_file.read())
    except ValueError as e:
        raise ValueError("Invalid private key.") from e

    # Sign the hash
    try:
        hash_obj = SHA256.new(model_hash.encode("utf-8"))
        signature = pkcs1_15.new(private_key).sign(hash_obj)
    except (ValueError, TypeError) as e:
        raise ValueError("Error signing the hash.") from e

    # Save the proof
    proof_data = {
        "model_hash": model_hash,
        "signature": signature.hex()
    }

    with open(proof_path, "w") as proof_file:
        json.dump(proof_data, proof_file)

    return proof_path

def verify_proof(model_path, public_key_path, proof_path):
    """
    Verifies the zero-knowledge proof for the given model file.

    Args:
        model_path (str): Path to the AI model file.
        public_key_path (str): Path to the public key file.
        proof_path (str): Path to the proof file.

    Returns:
        bool: True if the proof is valid, False otherwise.

    Raises:
        FileNotFoundError: If the model file, public key file, or proof file does not exist.
        ValueError: If there is an error in proof verification.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found.")

    if not os.path.exists(public_key_path):
        raise FileNotFoundError(f"Public key file '{public_key_path}' not found.")

    if not os.path.exists(proof_path):
        raise FileNotFoundError(f"Proof file '{proof_path}' not found.")

    # Compute the hash of the model file
    hasher = hashlib.sha256()
    with open(model_path, "rb") as model_file:
        while chunk := model_file.read(8192):
            hasher.update(chunk)
    model_hash = hasher.hexdigest()

    # Load the public key
    try:
        with open(public_key_path, "rb") as key_file:
            public_key = RSA.import_key(key_file.read())
    except ValueError as e:
        raise ValueError("Invalid public key.") from e

    # Load the proof
    try:
        with open(proof_path, "r") as proof_file:
            proof_data = json.load(proof_file)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid proof file format.") from e

    if proof_data.get("model_hash") != model_hash:
        return False

    # Verify the signature
    try:
        hash_obj = SHA256.new(model_hash.encode("utf-8"))
        signature = bytes.fromhex(proof_data["signature"])
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        return True
    except (ValueError, TypeError):
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZKP Model Authenticator")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate", help="Generate a zero-knowledge proof for a model.")
    generate_parser.add_argument("model_path", help="Path to the AI model file.")
    generate_parser.add_argument("private_key_path", help="Path to the private key file.")
    generate_parser.add_argument("--proof_path", default="proof.json", help="Path to save the generated proof file.")

    verify_parser = subparsers.add_parser("verify", help="Verify a zero-knowledge proof for a model.")
    verify_parser.add_argument("model_path", help="Path to the AI model file.")
    verify_parser.add_argument("public_key_path", help="Path to the public key file.")
    verify_parser.add_argument("proof_path", help="Path to the proof file.")

    args = parser.parse_args()

    if args.command == "generate":
        proof_file = generate_proof(args.model_path, args.private_key_path, args.proof_path)
        print(f"Proof generated and saved to {proof_file}")
    elif args.command == "verify":
        is_valid = verify_proof(args.model_path, args.public_key_path, args.proof_path)
        if is_valid:
            print("Proof is valid.")
        else:
            print("Proof is invalid.")