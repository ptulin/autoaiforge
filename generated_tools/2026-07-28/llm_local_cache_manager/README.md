# LLM Local Cache Manager

## Overview

The LLM Local Cache Manager is a Python utility for managing local caching of large language models (LLMs) and their weights. It helps AI developers optimize their local storage by identifying redundant or unused model files, cleaning up disk space, and downloading specific versions of models.

## Features

- List all locally cached models.
- Identify and remove unused models from the local cache.
- Download specific versions of models and cache them locally.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd llm_local_cache_manager
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following options:

- **List all cached models:**
  ```bash
  python llm_local_cache_manager.py --list
  ```

- **Clean unused models:**
  ```bash
  python llm_local_cache_manager.py --clean-unused
  ```

- **Download a specific model version:**
  ```bash
  python llm_local_cache_manager.py --download <MODEL_NAME> <VERSION>
  ```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_local_cache_manager.py
```

## Dependencies

- `huggingface_hub`
- `sqlalchemy`
- `pytest`

## License

This project is licensed under the MIT License.