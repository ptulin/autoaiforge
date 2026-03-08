# Code Assistant GPT-5.4

Code Assistant GPT-5.4 is a Python library designed to help developers analyze, debug, and document large-scale codebases using the GPT-5.4 model. It can handle entire projects or repositories for advanced code analysis and refactoring.

## Features
- Analyze entire codebases up to 1 million tokens.
- Detect bugs and suggest optimizations.
- Generate comprehensive inline comments and documentation.
- Provide architectural improvement suggestions for large projects.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### CLI

```bash
python code_assistant_gpt54.py <directory_path> <openai_api_key>
```

### Library

```python
from code_assistant_gpt54 import analyze_codebase

analyze_codebase('./my_project', 'your_openai_api_key')
```

## Example

```bash
python code_assistant_gpt54.py ./my_project sk-abc123
```

## Notes
- Ensure you have an OpenAI API key.
- The tool processes `.py` files only.

## License
MIT License