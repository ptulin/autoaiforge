# AI Code Linter

## Overview
AI Code Linter is a Python-based tool that integrates with OpenAI Codex to provide intelligent code linting suggestions. It checks for style, syntax, and potential bugs in your code and offers fixes and explanations. This tool is ideal for developers who want real-time feedback and cleaner code.

## Features
- Lint code files using OpenAI Codex.
- Get suggestions for improving code style, syntax, and potential bug fixes.
- Handles edge cases such as empty files, missing files, and API errors.

## Requirements
- Python 3.7+
- `openai` Python package
- `python-dotenv` Python package
- `pytest` for testing

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ai_code_linter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage
Run the tool with the following command:
```bash
python ai_code_linter.py --file <path_to_code_file>
```

Example:
```bash
python ai_code_linter.py --file example.py
```

## Running Tests
To run the tests, use the following command:
```bash
pytest test_ai_code_linter.py
```

## License
This project is licensed under the MIT License.