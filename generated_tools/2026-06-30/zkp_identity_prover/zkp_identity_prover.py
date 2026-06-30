import argparse
import json
import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def generate_zkp(user_data, private_key_path):
    """
    Generate a zero-knowledge proof (ZKP) for user identity data.

    Args:
        user_data (dict): The user attributes to include in the proof.
        private_key_path (str): Path to the private key for signing.

    Returns:
        dict: The generated ZKP in JSON format.
    """
    if not os.path.exists(private_key_path):
        raise FileNotFoundError("Private key file not found.")

    with open(private_key_path, "r") as key_file:
        private_key = RSA.import_key(key_file.read())

    user_data_str = json.dumps(user_data, sort_keys=True)
    hashed_data = SHA256.new(user_data_str.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(hashed_data)

    return {
        "user_data": user_data,
        "signature": signature.hex()
    }

def verify_zkp(zkp, public_key_path):
    """
    Verify a zero-knowledge proof (ZKP).

    Args:
        zkp (dict): The ZKP to verify.
        public_key_path (str): Path to the public key for verification.

    Returns:
        bool: True if the proof is valid, False otherwise.
    """
    if not os.path.exists(public_key_path):
        raise FileNotFoundError("Public key file not found.")

    with open(public_key_path, "r") as key_file:
        public_key = RSA.import_key(key_file.read())

    user_data_str = json.dumps(zkp["user_data"], sort_keys=True)
    hashed_data = SHA256.new(user_data_str.encode('utf-8'))
    signature = bytes.fromhex(zkp["signature"])

    try:
        pkcs1_15.new(public_key).verify(hashed_data, signature)
        return True
    except (ValueError, TypeError):
        return False

def main():
    parser = argparse.ArgumentParser(description="ZKP Identity Prover")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Generate a ZKP")
    generate_parser.add_argument("--input", required=True, help="Path to JSON file with user data.")
    generate_parser.add_argument("--key", required=True, help="Path to private key file.")

    verify_parser = subparsers.add_parser("verify", help="Verify a ZKP")
    verify_parser.add_argument("--zkp", required=True, help="Path to JSON file with ZKP.")
    verify_parser.add_argument("--key", required=True, help="Path to public key file.")

    args = parser.parse_args()

    if args.command == "generate":
        if not os.path.exists(args.input):
            print("Error: Input file not found.")
            return

        with open(args.input, "r") as input_file:
            user_data = json.load(input_file)

        try:
            zkp = generate_zkp(user_data, args.key)
            print(json.dumps(zkp, indent=4))
        except Exception as e:
            print(f"Error: {e}")

    elif args.command == "verify":
        if not os.path.exists(args.zkp):
            print("Error: ZKP file not found.")
            return

        with open(args.zkp, "r") as zkp_file:
            zkp = json.load(zkp_file)

        try:
            is_valid = verify_zkp(zkp, args.key)
            if is_valid:
                print("ZKP is valid.")
            else:
                print("ZKP is invalid.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
