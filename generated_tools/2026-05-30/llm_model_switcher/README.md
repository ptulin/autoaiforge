# LLM Model Switcher

## Description

LLM Model Switcher is a CLI tool that allows developers to easily switch between different versions of open-source LLM models and frameworks (like Llama.cpp) installed locally. It handles symbolic links, environment variables, and dependencies, enabling developers to test multiple configurations quickly.

## Features

- Switch between different versions of locally installed LLM models.
- Automatically updates symbolic links to point to the active model version.
- Sets environment variables for the active model.
- Handles errors gracefully, including missing versions and symbolic link creation issues.

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd llm_model_switcher
    ```

2. Run the tool directly using Python:
    ```bash
    python llm_model_switcher.py --activate <model_version> --base-path <path_to_models>
    ```

## Usage

### Command-line Arguments

- `--activate`: The model/framework version to activate.
- `--base-path`: The base directory where model versions are stored.

### Example

```bash
python llm_model_switcher.py --activate llama_cpp_v0.2 --base-path /path/to/models
```

This command will activate the `llama_cpp_v0.2` model version and update the symbolic link and environment variable accordingly.

## Testing

To run the tests:

1. Install pytest:
    ```bash
    pip install pytest
    ```

2. Run the tests:
    ```bash
    pytest test_llm_model_switcher.py
    ```

## License

This project is licensed under the MIT License.