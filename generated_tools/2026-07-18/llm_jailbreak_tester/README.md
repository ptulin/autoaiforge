# LLM Jailbreak Tester

## Description
LLM Jailbreak Tester automates the evaluation of large language models against a suite of predefined jailbreak prompts. This helps developers identify vulnerabilities in their models and improve their defenses against adversarial prompt engineering.

## Features
- **Preloaded Prompt Library**: Includes common jailbreak prompts to test your LLM.
- **Customizable Prompts**: Add your own prompts via a JSON file for targeted testing.
- **Detailed Reports**: Outputs pass/fail results for each prompt, either in the terminal or as a JSON file.

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python llm_jailbreak_tester.py --api_key YOUR_API_KEY --prompts prompts.json --output results.json
```

### Arguments
- `--api_key`: Your OpenAI API key (required).
- `--prompts`: Path to a JSON file containing test prompts (optional).
- `--output`: Path to save the results JSON file (optional).

If no `--prompts` file is provided, the tool uses a default set of jailbreak prompts.

### Example
```bash
python llm_jailbreak_tester.py --api_key sk-abc123 --prompts prompts.json --output results.json
```

## Testing
Run tests using pytest:
```bash
pytest test_llm_jailbreak_tester.py
```

## License
MIT License