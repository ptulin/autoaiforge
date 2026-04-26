# Claude Code Assistant

Claude Code Assistant is a CLI tool that integrates with Claude AI to help developers generate boilerplate code, refactor existing codebases, and provide code completion suggestions. This tool is designed to streamline repetitive coding tasks and assist developers in exploring AI-generated solutions.

## Features

- **Generate Boilerplate Code**: Quickly generate boilerplate code for various project types.
- **Refactor Code**: Optimize and refactor existing Python code.
- **Code Completion**: Get in-line code completion suggestions.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claude_code_assistant
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

## Usage

Run the tool using the command line:

- Generate boilerplate code:
  ```bash
  python claude_code_assistant.py --generate flask_app
  ```

- Refactor code from a file:
  ```bash
  python claude_code_assistant.py --refactor path/to/your/code.py
  ```

- Provide code completion suggestions:
  ```bash
  python claude_code_assistant.py --complete "print('Hello"
  ```

- Save the output to a file:
  ```bash
  python claude_code_assistant.py --generate flask_app --output output.py
  ```

## Testing

To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_claude_code_assistant.py
```

## License

This project is licensed under the MIT License.
