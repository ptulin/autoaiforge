# Token Optimizer Rewriter

## Description
Token Optimizer Rewriter is a Python CLI tool designed to minimize token usage in text while retaining its original meaning. This tool is particularly useful for developers working with token-limited APIs, ensuring that their prompts are concise and effective.

## Features
- Count the number of tokens in a given text.
- Optimize text using OpenAI's GPT-3.5-turbo model.
- Read input text from a file or inline text.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python token_optimizer_rewriter.py --input <input_text_or_file_path> --api_key <your_openai_api_key>
```

### Arguments
- `--input`: Path to the input text file or inline text.
- `--api_key`: Your OpenAI API key.

### Example
```bash
python token_optimizer_rewriter.py --input "This is a sample text." --api_key "your_api_key_here"
```

## Testing
To run the tests, use:
```bash
pytest test_token_optimizer_rewriter.py
```

## Requirements
- Python 3.7+
- `openai`
- `tiktoken`
- `pytest`

## License
MIT License