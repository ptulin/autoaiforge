# Token Optimizer

## Overview
The Token Optimizer is a Python tool designed to analyze token usage patterns in text inputs and provide suggestions for optimization. This can help developers reduce token consumption when working with APIs that charge based on token usage, such as OpenAI's GPT models.

## Features
- Analyze token usage in text inputs.
- Provide suggestions for reducing token usage, such as rephrasing or truncation.
- Support for analyzing text from files or direct input.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd token_optimizer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
You can use the tool by providing either a text file or a text string as input.

### Analyze a Text File
```bash
python token_optimizer.py --input_file path/to/textfile.txt
```

### Analyze a Text String
```bash
python token_optimizer.py --input_text "Your text here."
```

## Testing
This project uses `pytest` for testing. To run the tests:

1. Install `pytest` if you haven't already:
   ```bash
   pip install pytest
   ```
2. Run the tests:
   ```bash
   pytest test_token_optimizer.py
   ```

## Dependencies
- Python 3.7+
- nltk

## Notes
- The tool uses a mock encoding class (`MockEncoding`) to simulate tokenization behavior. Replace this with your desired encoding library (e.g., `tiktoken`) for production use.
- The `nltk` library is used for word tokenization. The `punkt` tokenizer is downloaded automatically if not already available.

## License
This project is licensed under the MIT License.