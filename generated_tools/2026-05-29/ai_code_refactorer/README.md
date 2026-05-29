# AI Code Refactorer

## Description
The AI Code Refactorer is a Python-based tool that integrates with the OpenAI API to refactor code for better readability and optimization. It scans a given file, detects areas for improvement (e.g., redundant code, poor variable naming, or suboptimal logic), and provides refactored versions of the code.

## Features
- Reads code from a specified file.
- Uses OpenAI's GPT model to suggest refactored code.
- Allows saving the refactored code to a specified file.

## Requirements
- Python 3.7+
- `openai` Python package
- `python-dotenv` Python package
- `pytest` for testing

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install openai python-dotenv pytest
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage
Run the script with the following command:
```bash
python ai_code_refactorer.py --file <path_to_input_file> [--save <path_to_output_file>]
```

### Arguments
- `--file`: Path to the file containing the code to be refactored (required).
- `--save`: Path to save the refactored code (optional). If not provided, the refactored code will be printed to the console.

### Example
```bash
python ai_code_refactorer.py --file example.py --save refactored_example.py
```

## Testing
Run the tests using `pytest`:
```bash
pytest test_ai_code_refactorer.py
```

## Notes
- Ensure your OpenAI API key is valid and has sufficient quota.
- The tool does not modify the original file unless explicitly saved to the same path.
