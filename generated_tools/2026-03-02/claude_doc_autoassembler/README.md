# Claude Document Auto-Assembler

## Overview
The Claude Document Auto-Assembler is a Python CLI tool designed to help generate and assemble business documents using Claude AI. Users can provide input data (in JSON or CSV format) and predefined templates (in Jinja2 format). The tool uses Claude AI to refine the generated content and outputs polished documents in either PDF or DOCX format.

## Features
- Load input data from JSON or CSV files.
- Use Jinja2 templates to generate content dynamically.
- Refine content using Claude AI API.
- Save the final output as a PDF or DOCX file.

## Requirements
- Python 3.7+
- Install required packages:
  ```bash
  pip install -r requirements.txt
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd claude_doc_autoassembler
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python claude_doc_autoassembler.py --template <template_path> --input <input_path> --output <output_path> --api-key <api_key>
```

### Arguments
- `--template`: Path to the Jinja2 template file.
- `--input`: Path to the input data file (JSON or CSV).
- `--output`: Path to the output file (PDF or DOCX).
- `--api-key`: API key for Claude AI.

### Example
```bash
python claude_doc_autoassembler.py --template template.j2 --input data.json --output output.pdf --api-key YOUR_API_KEY
```

## Testing
Run the tests using pytest:
```bash
pytest test_claude_doc_autoassembler.py
```

## License
MIT License