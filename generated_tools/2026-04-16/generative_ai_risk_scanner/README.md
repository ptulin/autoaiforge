# Generative AI Risk Scanner

## Overview
The Generative AI Risk Scanner is a CLI tool designed to analyze generative AI model configurations and parameters for common security vulnerabilities. It helps developers identify potential risks such as unsafe sampling settings, exposure to prompt injection attacks, and susceptibility to adversarial examples.

## Features
- Analyze model parameters for unsafe configurations (e.g., low temperature, high top-p values).
- Simulate prompt injection attacks to assess model vulnerability.
- Generate a detailed vulnerability report in JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd generative_ai_risk_scanner
   ```

2. Install the required dependencies:
   ```bash
   pip install transformers
   ```

## Usage

Run the CLI tool with the following command:

```bash
python generative_ai_risk_scanner.py --model-id <model_id> --config-file <config_file> --output <output_file>
```

### Arguments
- `--model-id`: Hugging Face model identifier (required).
- `--config-file`: Path to the model configuration JSON file (optional).
- `--output`: Path to save the vulnerability report (required).

### Example

```bash
python generative_ai_risk_scanner.py --model-id gpt2 --config-file model_config.json --output report.json
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_generative_ai_risk_scanner.py
```

## License

This project is licensed under the MIT License.