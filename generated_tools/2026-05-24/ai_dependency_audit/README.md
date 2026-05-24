# ai_dependency_audit

`ai_dependency_audit` is a Python tool that analyzes project dependencies (e.g., `requirements.txt` or `package.json`) for security vulnerabilities using AI. It flags outdated or vulnerable packages and provides recommendations for safer alternatives, making it indispensable for secure software development.

## Features

- Analyze Python `requirements.txt` and Node.js `package.json` files.
- Identify outdated or vulnerable packages.
- Suggest safer alternatives for vulnerable dependencies.

## Installation

Install the required dependencies using pip:

```bash
pip install openai pytest
```

## Usage

Run the tool from the command line:

```bash
python ai_dependency_audit.py <path_to_dependency_file>
```

Example:

```bash
python ai_dependency_audit.py requirements.txt
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_dependency_audit.py
```

## Environment Variables

Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

## License

This project is licensed under the MIT License.