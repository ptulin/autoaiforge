# Claude CI Linter

Claude CI Linter is a pre-commit hook tool that integrates Claude AI to automatically review and provide suggestions for Python code in pull requests or commits. It evaluates Python code for style, bugs, and optimization opportunities, ensuring high-quality codebases.

## Features

- **AI-Powered Code Analysis**: Uses Claude AI to provide feedback on Python code.
- **Git Integration**: Runs as a pre-commit hook to analyze staged Python files.
- **Customizable**: Allows you to specify your Claude API key.

## Installation

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Add the following to your `.pre-commit-config.yaml` file:

   ```yaml
   - repo: local
     hooks:
       - id: claude-ci-linter
         name: Claude CI Linter
         entry: python claude_ci_linter.py --api-key YOUR_API_KEY
         language: system
         files: \.py$
   ```

3. Install the pre-commit hook:

   ```bash
   pre-commit install
   ```

## Usage

Once installed, the linter will automatically analyze staged Python files whenever you make a commit. It will provide AI-generated feedback directly in the terminal.

You can also run the linter manually:

```bash
python claude_ci_linter.py --api-key YOUR_API_KEY
```

## Example

1. Stage some Python files:

   ```bash
   git add file1.py file2.py
   ```

2. Commit your changes:

   ```bash
   git commit -m "Add new features"
   ```

3. The linter will analyze the staged files and display feedback in the terminal.

## Limitations

- Requires an active Claude API key.
- Internet connection is required for API calls.

## License

MIT License
