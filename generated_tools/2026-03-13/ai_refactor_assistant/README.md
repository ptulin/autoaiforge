# AI Refactor Assistant

AI Refactor Assistant helps developers refactor and optimize Python scripts for readability, performance, and best practices. It uses OpenAI's GPT-4 model to understand the code context and generate improved versions of existing functions or modules.

## Features
- Refactor Python code using OpenAI's GPT-4.
- Format code using Black for consistent style.
- Optionally write the refactored code back to the original file.

## Installation

Install the required dependencies:

```bash
pip install openai black rich
```

## Usage

Run the tool from the command line:

```bash
python ai_refactor_assistant.py --file <path_to_python_file> --api-key <your_openai_api_key> [--write-back]
```

### Arguments
- `--file`: Path to the Python file to refactor.
- `--api-key`: Your OpenAI API key for generating refactored code.
- `--write-back`: Optional. Write the refactored code back to the file and format it with Black.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_refactor_assistant.py
```

## License

This project is licensed under the MIT License.