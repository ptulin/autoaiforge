# AI Error Explainer

AI Error Explainer is a Python tool that helps developers understand complex error messages from their Python projects. By leveraging OpenAI's GPT-4, the tool provides detailed explanations and potential fixes for errors, making debugging faster and easier.

## Features
- Input Python error messages and receive AI-generated explanations.
- Get actionable advice to resolve errors.
- Supports input via command-line arguments or standard input (stdin).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_error_explainer.git
   cd ai_error_explainer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the command line:

```bash
python ai_error_explainer.py --api-key YOUR_OPENAI_API_KEY --error "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
```

Alternatively, you can provide the error message via standard input:

```bash
echo "TypeError: unsupported operand type(s) for +: 'int' and 'str'" | python ai_error_explainer.py --api-key YOUR_OPENAI_API_KEY
```

## Requirements

- Python 3.7+
- `rich`
- `openai`

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then run:

```bash
pytest test_ai_error_explainer.py
```

The tests include:
- Successful explanation retrieval.
- Handling of API errors.
- Handling of empty error messages.

## License

This project is licensed under the MIT License.
