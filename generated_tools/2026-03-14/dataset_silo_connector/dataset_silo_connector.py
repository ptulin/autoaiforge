import os
import io
import pandas as pd
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7

def decrypt_data(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Decrypts the given encrypted data using AES CBC mode.

    Args:
        encrypted_data (bytes): The encrypted data to decrypt.
        key (bytes): The decryption key.
        iv (bytes): The initialization vector.

    Returns:
        bytes: The decrypted data.
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove padding
    unpadder = PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data

def load_silo(encrypted_file_path: str, key_file_path: str, chunk_size: int = None):
    """
    Loads an encrypted dataset silo, decrypts it, and streams it as a Pandas DataFrame.

    Args:
        encrypted_file_path (str): Path to the encrypted dataset file.
        key_file_path (str): Path to the file containing the decryption key and IV.
        chunk_size (int, optional): Number of rows to load per chunk. If None, loads the entire dataset.

    Yields:
        pd.DataFrame: Decrypted data as a Pandas DataFrame.
    """
    if not os.path.exists(encrypted_file_path):
        raise FileNotFoundError(f"Encrypted file not found: {encrypted_file_path}")

    if not os.path.exists(key_file_path):
        raise FileNotFoundError(f"Key file not found: {key_file_path}")

    with open(key_file_path, 'rb') as key_file:
        key = key_file.read(32)  # AES key size: 256 bits (32 bytes)
        iv = key_file.read(16)   # AES block size: 128 bits (16 bytes)

    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = decrypt_data(encrypted_data, key, iv)

    decrypted_stream = io.BytesIO(decrypted_data)

    if chunk_size:
        for chunk in pd.read_csv(decrypted_stream, chunksize=chunk_size):
            yield chunk
    else:
        yield pd.read_csv(decrypted_stream)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Dataset Silo Connector")
    parser.add_argument("encrypted_file", help="Path to the encrypted dataset file.")
    parser.add_argument("key_file", help="Path to the decryption key file.")
    parser.add_argument("--chunk_size", type=int, default=None, help="Number of rows to load per chunk.")

    args = parser.parse_args()

    try:
        for df in load_silo(args.encrypted_file, args.key_file, args.chunk_size):
            print(df)
    except Exception as e:
        print(f"Error: {e}")