# ZKP Model Authenticator

## Overview

The ZKP Model Authenticator is a Python library for enabling zero-knowledge proof-based authentication of AI models. This ensures that model ownership or validity can be proven without exposing the model itself, which is vital for protecting sensitive intellectual property.

## Features

- Generate a zero-knowledge proof for an AI model.
- Verify the validity of a zero-knowledge proof.

## Installation

Install the required dependencies using pip:

```bash
pip install pycryptodome
```

## Usage

### Command-Line Interface

#### Generate Proof

```bash
python zkp_model_authenticator.py generate <model_path> <private_key_path> [--proof_path <proof_path>]
```

- `model_path`: Path to the AI model file.
- `private_key_path`: Path to the private key file.
- `--proof_path`: (Optional) Path to save the generated proof file. Default is `proof.json`.

#### Verify Proof

```bash
python zkp_model_authenticator.py verify <model_path> <public_key_path> <proof_path>
```

- `model_path`: Path to the AI model file.
- `public_key_path`: Path to the public key file.
- `proof_path`: Path to the proof file.

### Example

#### Generate Proof

```bash
python zkp_model_authenticator.py generate model.pth private_key.pem --proof_path proof.json
```

#### Verify Proof

```bash
python zkp_model_authenticator.py verify model.pth public_key.pem proof.json
```

## Testing

Run the tests using pytest:

```bash
pytest test_zkp_model_authenticator.py
```

## License

This project is licensed under the MIT License.