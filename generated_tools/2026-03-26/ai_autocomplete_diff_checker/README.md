# AI Autocomplete Diff Checker

## Description
The AI Autocomplete Diff Checker is a Python tool designed to help developers review and validate AI-suggested code changes. By generating unified diff files, it highlights the exact changes between the original source code and the AI-suggested modifications, enabling developers to easily evaluate and decide whether to accept or reject the changes.

## Features
- Generate unified diff files between original and AI-suggested code.
- Optional output to a file or display directly in the terminal.
- User-friendly CLI for quick and efficient review of changes.

## Installation
1. Clone the repository or download the `ai_autocomplete_diff_checker.py` file.
2. Install Python 3.7 or higher.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python ai_autocomplete_diff_checker.py original.py suggested.py --output diff.txt
```

### Arguments
- `original_file`: Path to the original source file.
- `suggested_file`: Path to the AI-suggested modified file.
- `--output`: (Optional) Path to save the generated diff file. If not provided, the diff will be displayed in the terminal.

### Example
```bash
python ai_autocomplete_diff_checker.py original.py suggested.py --output diff.txt
```

This will generate a diff file named `diff.txt` containing the differences between `original.py` and `suggested.py`.

## Testing
Run the tests using `pytest`:
```bash
pytest test_ai_autocomplete_diff_checker.py
```

## License
This project is licensed under the MIT License.