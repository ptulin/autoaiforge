# Secure Silo Manager

Secure Silo Manager is a command-line tool for creating and managing encrypted data silos for AI workflows. It allows users to securely store, encrypt, and retrieve datasets with tightly controlled access permissions, ensuring privacy and compliance in AI development workflows.

## Features

- Create secure silos for storing encrypted data.
- Add files to silos with role-based encryption.
- Retrieve and decrypt files from silos.
- Delete silos when no longer needed.

## Installation

Install the required dependencies:

```bash
pip install cryptography
```

## Usage

Run the tool using the command line:

### Create a new silo

```bash
python secure_silo_manager.py create --name <silo_name>
```

### Add a file to a silo

```bash
python secure_silo_manager.py add --name <silo_name> --file <file_path> --role <role_name>
```

### Retrieve a file from a silo

```bash
python secure_silo_manager.py retrieve --name <silo_name> --role <role_name> --output <output_path>
```

### Delete a silo

```bash
python secure_silo_manager.py delete --name <silo_name>
```

## Testing

Run the tests using pytest:

```bash
pytest test_secure_silo_manager.py
```

## License

This project is licensed under the MIT License.