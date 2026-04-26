# Claude Test Generator

Claude Test Generator is a Python library and CLI tool that uses Claude AI to auto-generate unit tests for Python functions or classes. This tool aids developers in quickly generating robust test cases, saving time and improving test coverage.

## Installation

To install the required dependencies, run:

```bash
pip install openai click pytest
```

## Usage

You can use the tool via the command line. The tool requires an OpenAI API key to interact with Claude AI.

### Command Line Interface

```bash
python claude_test_generator.py --input <path_to_python_file> --output <path_to_output_test_file> --api-key <your_openai_api_key>
```

- `--input`: Path to the Python file you want to analyze.
- `--output`: Path where the generated test file will be saved.
- `--api-key`: Your OpenAI API key for accessing Claude AI.

### Example

```bash
python claude_test_generator.py --input example.py --output test_example.py --api-key YOUR_API_KEY
```

This will generate a `test_example.py` file containing unit tests for the code in `example.py`.

## Testing

To run the tests, use `pytest`:

```bash
pytest test_claude_test_generator.py
```

The tests include mocking for the OpenAI API, so no network access is required.

## License

This project is licensed under the MIT License.