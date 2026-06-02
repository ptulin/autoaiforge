# LLM Code Assistant

LLM Code Assistant is a CLI tool that integrates with OpenAI's API to provide inline code suggestions, refactorings, and debugging hints based on user queries. This tool helps developers streamline their coding process by leveraging LLMs to automate routine tasks and enhance productivity.

## Features
- Generate code snippets based on natural language queries.
- Refactor and optimize existing Python code.
- Save generated or refactored code to a specified file.

## Installation

Install the required dependencies:

```bash
pip install openai pytest
```

## Usage

Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

Run the tool with the following options:

### Generate Code Snippets
```bash
python llm_code_assistant.py --query "Write a Python function to sort an array"
```

### Refactor Code
```bash
python llm_code_assistant.py --file path/to/your/code.py
```

### Save Output to a File
```bash
python llm_code_assistant.py --query "Write a Python function to sort an array" --output path/to/output.py
```

## Testing

Run the tests using pytest:

```bash
pytest test_llm_code_assistant.py
```

## License

This project is licensed under the MIT License.