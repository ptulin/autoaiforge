# Commit Message Linter

## Description

The Commit Message Linter is a Python tool that analyzes Git commit messages using OpenAI's GPT model. It ensures that commit messages follow best practices for clarity, conciseness, and relevance. The tool flags ambiguous messages and suggests improvements to make them more informative and helpful.

## Features

- Analyze individual commit messages or all commit messages in a repository.
- Provide AI-powered suggestions for improving commit message quality.
- Highlight issues in commit messages.

## Requirements

- Python 3.7+
- GitPython
- OpenAI Python SDK
- Colorama

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd commit_message_linter
   ```

2. Install dependencies:
   ```
   pip install gitpython openai colorama
   ```

## Usage

Run the script with the following command:

```bash
python commit_message_linter.py --repo <path_to_git_repo> --api-key <your_openai_api_key>
```

Optional arguments:
- `--commit <commit_hash>`: Analyze a specific commit message.

Example:

```bash
python commit_message_linter.py --repo ./my-repo --api-key YOUR_API_KEY
```

## Testing

To run tests:

1. Install pytest:
   ```
   pip install pytest
   ```

2. Run the tests:
   ```
   pytest test_commit_message_linter.py
   ```

## License

This project is licensed under the MIT License.