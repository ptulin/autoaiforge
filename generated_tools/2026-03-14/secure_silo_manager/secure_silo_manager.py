import os
import argparse
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from base64 import urlsafe_b64encode, urlsafe_b64decode
from getpass import getpass

class SecureSiloManager:
    def __init__(self):
        self.silos = {}

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    def _encrypt(self, data: bytes, password: str) -> bytes:
        salt = os.urandom(16)
        key = self._derive_key(password, salt)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return urlsafe_b64encode(salt + iv + encrypted_data)

    def _decrypt(self, encrypted_data: bytes, password: str) -> bytes:
        decoded_data = urlsafe_b64decode(encrypted_data)
        salt, iv, ciphertext = decoded_data[:16], decoded_data[16:32], decoded_data[32:]
        key = self._derive_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    def create_silo(self, name: str):
        if name in self.silos:
            raise ValueError("Silo already exists.")
        self.silos[name] = {}
        print(f"Silo '{name}' created successfully.")

    def add_to_silo(self, name: str, file_path: str, role: str):
        if name not in self.silos:
            raise ValueError("Silo does not exist.")
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found.")
        password = getpass("Enter encryption password: ")
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted_data = self._encrypt(data, password)
        self.silos[name][role] = encrypted_data
        print(f"File '{file_path}' added to silo '{name}' under role '{role}'.")

    def retrieve_from_silo(self, name: str, role: str, output_path: str):
        if name not in self.silos or role not in self.silos[name]:
            raise ValueError("Silo or role does not exist.")
        password = getpass("Enter decryption password: ")
        encrypted_data = self.silos[name][role]
        try:
            data = self._decrypt(encrypted_data, password)
        except Exception as e:
            raise ValueError("Decryption failed. Incorrect password or corrupted data.") from e
        with open(output_path, 'wb') as f:
            f.write(data)
        print(f"Data retrieved from silo '{name}' under role '{role}' and saved to '{output_path}'.")

    def delete_silo(self, name: str):
        if name not in self.silos:
            raise ValueError("Silo does not exist.")
        del self.silos[name]
        print(f"Silo '{name}' deleted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Secure Silo Manager: Manage encrypted data silos.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new silo.")
    create_parser.add_argument("--name", required=True, help="Name of the silo.")

    add_parser = subparsers.add_parser("add", help="Add a file to a silo.")
    add_parser.add_argument("--name", required=True, help="Name of the silo.")
    add_parser.add_argument("--file", required=True, help="Path to the file to add.")
    add_parser.add_argument("--role", required=True, help="Role under which to store the file.")

    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve a file from a silo.")
    retrieve_parser.add_argument("--name", required=True, help="Name of the silo.")
    retrieve_parser.add_argument("--role", required=True, help="Role of the file to retrieve.")
    retrieve_parser.add_argument("--output", required=True, help="Path to save the retrieved file.")

    delete_parser = subparsers.add_parser("delete", help="Delete a silo.")
    delete_parser.add_argument("--name", required=True, help="Name of the silo to delete.")

    args = parser.parse_args()
    manager = SecureSiloManager()

    if args.command == "create":
        manager.create_silo(args.name)
    elif args.command == "add":
        manager.add_to_silo(args.name, args.file, args.role)
    elif args.command == "retrieve":
        manager.retrieve_from_silo(args.name, args.role, args.output)
    elif args.command == "delete":
        manager.delete_silo(args.name)

if __name__ == "__main__":
    main()