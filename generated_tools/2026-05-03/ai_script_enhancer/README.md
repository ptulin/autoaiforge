# AI Script Enhancer

## Description
The AI Script Enhancer is a Python tool that takes a text-based script or screenplay as input and uses OpenAI's GPT-4 model to suggest improvements. These improvements include enhancing character dialogue, fixing grammar, and adjusting the tone of the script based on user preferences. This tool is designed for writers and filmmakers to refine their scripts.

## Features
- Analyze and enhance character dialogue.
- Fix grammar issues in the script.
- Adjust the tone of the script based on user input (e.g., formal, casual, dramatic).

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install openai
   ```

## Usage
Run the script from the command line with the following arguments:

```bash
python ai_script_enhancer.py --input <path_to_script_file> --tone <desired_tone> [--output <output_file>]
```

### Arguments
- `--input`: Path to the input script file (required).
- `--tone`: Desired tone/style for the script (e.g., formal, casual, dramatic) (required).
- `--output`: Path to save the enhanced script. If not provided, the enhanced script will be printed to the console.

### Example
```bash
python ai_script_enhancer.py --input my_script.txt --tone formal --output enhanced_script.txt
```

## Testing
This project includes a test suite using `pytest`. To run the tests:

1. Install `pytest`:
   ```bash
   pip install pytest
   ```
2. Run the tests:
   ```bash
   pytest test_ai_script_enhancer.py
   ```

The tests include the following scenarios:
- Valid input script.
- Non-existent input file.
- Empty input file.
- OpenAI API failure.

## Requirements
- Python 3.7+
- `openai` Python package

## Notes
- You need an OpenAI API key to use this tool. Set the `OPENAI_API_KEY` environment variable with your API key before running the script.
- This tool uses the GPT-4 model for script enhancement.

## License
This project is licensed under the MIT License.