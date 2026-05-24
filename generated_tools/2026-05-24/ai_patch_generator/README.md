# AI Patch Generator

## Description
`ai_patch_generator` is a Python-based CLI tool that analyzes a source code file containing a known vulnerability and uses OpenAI's GPT model to suggest potential patches. The tool highlights the vulnerable code, proposes fixes, and generates a patch file for easy integration.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install openai
   ```

## Usage

Run the tool using the following command:

```bash
python ai_patch_generator.py --file <path_to_vulnerable_file> --output <path_to_patch_file>
```

### Arguments
- `--file`: Path to the source code file containing a known vulnerability.
- `--output`: Path to save the AI-generated patch file.

### Example

```bash
python ai_patch_generator.py --file vulnerable_code.py --output patch_file.patch
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then execute the tests:

```bash
pytest test_ai_patch_generator.py
```

## Notes
- This tool uses OpenAI's GPT model to analyze and generate patches. Ensure you have set up your OpenAI API key as an environment variable (`OPENAI_API_KEY`).
- The tool assumes that the AI response will include the vulnerable code and the suggested patch separated by the phrase `Suggested Patch:`.

## License
This project is licensed under the MIT License.