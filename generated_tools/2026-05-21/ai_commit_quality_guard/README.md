# AI Commit Quality Guard

## Overview

`ai_commit_quality_guard` is a pre-commit hook that uses OpenAI's GPT-4 model to automatically review staged Python files before committing. It assesses the code for bugs, stylistic issues, and adherence to best practices, ensuring higher-quality code is pushed to the repository.

## Features

- Automatically reviews staged Python files in a Git repository.
- Provides feedback on potential bugs, stylistic issues, and best practices.
- Blocks commits if issues are found in the code.

## Installation

1. Install the required Python packages:

   ```bash
   pip install openai pyyaml
   ```

2. Save the `ai_commit_quality_guard.py` script in your repository.

3. Create a configuration file named `.ai_commit_quality_guard.yaml` in the root of your repository (optional):

   ```yaml
   rules:
     max_line_length: 80
   ```

4. Add the script as a pre-commit hook by creating a `.git/hooks/pre-commit` file with the following content:

   ```bash
   #!/bin/sh
   python3 path/to/ai_commit_quality_guard.py --config .ai_commit_quality_guard.yaml
   ```

5. Make the pre-commit hook executable:

   ```bash
   chmod +x .git/hooks/pre-commit
   ```

## Usage

When you attempt to commit Python files, the pre-commit hook will automatically review the staged files. If any issues are found, the commit will be blocked, and the issues will be displayed in the terminal.

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key is required for the script to function. Set this environment variable before using the tool.

## Testing

To run the tests, install `pytest` and execute:

```bash
pytest test_ai_commit_quality_guard.py
```

## License

MIT License