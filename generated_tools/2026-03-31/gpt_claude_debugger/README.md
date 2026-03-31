# GPT-Claude Debug Assistant

## Description
The GPT-Claude Debug Assistant is a command-line tool designed to help developers debug Python error tracebacks. It integrates OpenAI's GPT and Anthropic's Claude models to provide AI-suggested fixes, explanations, and improved code snippets for Python errors. This tool is particularly useful for debugging complex AI workflows or unfamiliar libraries.

## Features
- Analyze Python traceback errors using GPT and Claude models.
- Provide detailed explanations, suggested fixes, and code snippets.
- Interactive mode for follow-up questions and clarifications.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gpt_claude_debugger.git
   cd gpt_claude_debugger
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Analyze a Python traceback from a file:
```bash
python gpt_claude_debugger.py --error-log traceback.txt --gpt-api-key YOUR_OPENAI_API_KEY --claude-api-key YOUR_ANTHROPIC_API_KEY
```

### Paste a traceback directly into the CLI:
```bash
python gpt_claude_debugger.py --gpt-api-key YOUR_OPENAI_API_KEY --claude-api-key YOUR_ANTHROPIC_API_KEY
```

### Enable interactive mode:
```bash
python gpt_claude_debugger.py --interactive --gpt-api-key YOUR_OPENAI_API_KEY --claude-api-key YOUR_ANTHROPIC_API_KEY
```

## Example
```bash
python gpt_claude_debugger.py --error-log traceback.txt --gpt-api-key sk-1234 --claude-api-key sk-5678
```

## License
This project is licensed under the MIT License.
