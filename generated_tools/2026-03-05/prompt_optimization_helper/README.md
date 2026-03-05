# Prompt Optimization Helper

## Description
The Prompt Optimization Helper is a CLI tool designed to help AI developers optimize and refine prompts for large language models (LLMs). It allows users to test multiple variations of prompts and benchmark their outputs based on defined quality metrics. This tool is particularly useful for fine-tuning prompt phrasing for better AI responses in chatbot systems, content generation, and other LLM-based applications.

## Features
- Test multiple prompt variations with a single command.
- Automatically score outputs based on user-defined metrics (e.g., relevance, conciseness).
- Supports batch input for bulk prompt optimization.
- Outputs results as a ranked and scored CSV file.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd prompt_optimization_helper
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```bash
python prompt_optimization_helper.py --base "Explain AI" --variations variations.txt --output results.csv --key <API_KEY>
```

### Arguments
- `--base`: The base prompt to use for testing variations.
- `--variations`: Path to a text file containing prompt variations (one per line).
- `--output`: Path to save the output CSV file.
- `--key`: OpenAI API key.

### Example
1. Create a `variations.txt` file:
   ```
   in simple terms
   to a 5-year-old
   for a technical audience
   ```
2. Run the tool:
   ```bash
   python prompt_optimization_helper.py --base "Explain AI" --variations variations.txt --output results.csv --key <API_KEY>
   ```
3. Check the generated `results.csv` for the ranked and scored output.

## Testing
Run the tests using pytest:
```bash
pytest test_prompt_optimization_helper.py
```

## License
MIT License