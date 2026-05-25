# Bug Sleuth

Bug Sleuth is an AI-powered Python code analysis tool that helps developers identify potential bugs in their Python scripts and provides suggestions for fixes. It leverages OpenAI's GPT-4 model to analyze code and return insights, making debugging workflows faster and more efficient.

## Features
- Analyze Python scripts or raw code for potential bugs.
- Get detailed suggestions for fixes.
- Handles invalid Python code gracefully.
- Provides meaningful error messages for missing files or API issues.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/bug_sleuth.git
   cd bug_sleuth
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line by providing a Python script file or raw Python code as input:

```bash
python bug_sleuth.py "path/to/your_script.py"
```

Or provide raw Python code as a string:

```bash
python bug_sleuth.py "def add(a, b):\n    return a + b"
```

## Example Output

```json
{
    "code": "def add(a, b):\n    return a + b",
    "analysis": "No issues detected."
}
```

## Running Tests

To run the tests, install `pytest` and run the following command:

```bash
pip install pytest
pytest test_bug_sleuth.py
```

## Requirements

- Python 3.7+
- loguru
- openai

## Notes

- Ensure you have a valid OpenAI API key set up in your environment to use this tool.
- This tool is designed to work with Python code only.

## License

This project is licensed under the MIT License.