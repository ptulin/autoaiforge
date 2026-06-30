# ZKP Identity Prover

## Overview
This Python CLI tool allows developers to generate and verify zero-knowledge proofs (ZKPs) for user identity verification in AI applications. It enables secure user authentication without revealing sensitive information, enhancing privacy in AI-driven systems.

## Features
- **Generate ZKP**: Create a zero-knowledge proof for user identity data using an RSA private key.
- **Verify ZKP**: Verify the authenticity of a zero-knowledge proof using an RSA public key.

## Requirements
- Python 3.7+
- `pycryptodome`
- `pytest` (for running tests)

## Installation
1. Install Python 3.7 or higher.
2. Install the required dependencies:
   ```bash
   pip install pycryptodome pytest
   ```

## Usage

### Generate a ZKP
To generate a zero-knowledge proof for user data:
```bash
python zkp_identity_prover.py generate --input <user_data.json> --key <private_key.pem>
```
- `<user_data.json>`: Path to a JSON file containing user data.
- `<private_key.pem>`: Path to the RSA private key file.

Example:
```bash
python zkp_identity_prover.py generate --input user_data.json --key private_key.pem
```

### Verify a ZKP
To verify a zero-knowledge proof:
```bash
python zkp_identity_prover.py verify --zkp <zkp.json> --key <public_key.pem>
```
- `<zkp.json>`: Path to a JSON file containing the ZKP.
- `<public_key.pem>`: Path to the RSA public key file.

Example:
```bash
python zkp_identity_prover.py verify --zkp zkp.json --key public_key.pem
```

## Testing
To run the tests:
```bash
pytest test_zkp_identity_prover.py
```

## Notes
- The tool uses RSA keys for signing and verification.
- Ensure that the private and public keys are properly generated and stored securely.
