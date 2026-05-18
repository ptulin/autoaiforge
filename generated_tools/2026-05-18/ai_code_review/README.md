# AI Code Review

AI Code Review is a Python CLI tool that analyzes Python code files or snippets for potential bugs, optimization opportunities, and adherence to best practices. It leverages OpenAI's AI models to provide actionable feedback and explanations, making it a valuable companion for improving code quality.

## Features
- Analyze Python code for bugs and potential issues.
- Suggest optimizations and best practices.
- Provide actionable feedback with explanations.
- Supports both file-based and inline code snippet analysis.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_code_review.git
   cd ai_code_review
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Analyze a Python file
```bash
python ai_code_review.py --file example.py --api-key YOUR_OPENAI_API_KEY
```

### Analyze a Python code snippet
```bash
python ai_code_review.py --code "print('Hello, world!')" --api-key YOUR_OPENAI_API_KEY
```

### Options
- `--file`: Path to the Python file to analyze.
- `--code`: Python code snippet to analyze.
- `--api-key`: Your OpenAI API key (required).

## Example Output
```
Analyzing code...

Analysis Feedback:
========================================
- The print statement is used for debugging purposes. Consider using logging instead.
- The code is simple and does not contain any apparent bugs.
```

## Testing

Run the tests using `pytest`:
```bash
pytest test_ai_code_review.py
```

## License
This project is licensed under the MIT License.