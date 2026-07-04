# LLM Cost Estimator

## Description
The LLM Cost Estimator is a command-line tool designed to calculate the estimated cost of using a Large Language Model (LLM) API based on the token counts of one or more input prompts and the pricing structure of specific providers. This tool is useful for budgeting and cost prediction before running expensive queries on LLM APIs.

## Features
- Token-based cost estimation for multiple LLM providers
- Batch processing for multiple prompts
- Customizable pricing configuration via YAML files

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Example Command
```bash
python llm_cost_estimator.py --file prompts.txt --config pricing.yaml --llm openai
```

### Options
- `--file`: Path to the file containing prompts (required).
- `--config`: Path to the YAML pricing configuration file (required).
- `--llm`: The LLM model to use for token counting (required).

### Example Input Files
#### `prompts.txt`
```
Hello world!
How are you?
```

#### `pricing.yaml`
```yaml
openai:
  cost_per_token: 0.0001
```

### Example Output
```
Total tokens: 8
Estimated cost: $0.0008
```

## Testing
Run the tests using `pytest`:
```bash
pytest test_llm_cost_estimator.py
```

## License
MIT License
