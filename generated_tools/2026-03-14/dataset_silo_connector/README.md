# Dataset Silo Connector

## Overview

The Dataset Silo Connector is a Python library that streamlines the integration of encrypted AI silos into AI training pipelines. It allows developers to load encrypted datasets directly into memory, decrypt them on-the-fly, and ensure the data remains secure during processing.

## Features

- Decrypt AES-encrypted datasets using CBC mode.
- Stream decrypted data as Pandas DataFrames.
- Support for chunked loading to handle large datasets.

## Installation

Install the required dependencies using pip:

```bash
pip install pandas cryptography
```

## Usage

Run the script from the command line:

```bash
python dataset_silo_connector.py <encrypted_file> <key_file> [--chunk_size CHUNK_SIZE]
```

- `encrypted_file`: Path to the encrypted dataset file.
- `key_file`: Path to the file containing the decryption key and IV.
- `--chunk_size`: (Optional) Number of rows to load per chunk.

## Example

```bash
python dataset_silo_connector.py encrypted_data.enc decryption_key.key --chunk_size 100
```

## Testing

Run the tests using pytest:

```bash
pytest test_dataset_silo_connector.py
```

Ensure all tests pass before deploying or using the library in production.

## License

This project is licensed under the MIT License.