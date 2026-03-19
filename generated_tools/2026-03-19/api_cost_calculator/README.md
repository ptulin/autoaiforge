# API Cost Calculator

## Description
The API Cost Calculator is a command-line tool designed to estimate the cost of using AI language models based on input text length, tokenization, and current pricing. It supports multiple models and provides a side-by-side cost comparison to help developers make informed decisions about their API usage.

## Features
- Tokenize input text using model-specific tokenizers.
- Calculate API cost based on current pricing rates.
- Supports multiple models for side-by-side cost comparison.
- Outputs results in a human-readable table or JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/api_cost_calculator.git
   cd api_cost_calculator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

```bash
python api_cost_calculator.py --input example.txt --models gpt-4 claude-2 --pricing pricing.json --output human
```

### Options
- `--input`: Path to the input text file. Use `-` to read from standard input.
- `--models`: List of models to compare (e.g., `gpt-4`, `gpt-3.5`, `claude-2`).
- `--pricing`: Path to a JSON file containing pricing information.
- `--output`: Output format (`human` or `json`). Default is `human`.

### Example Pricing File

```json
{
  "gpt-4": 0.03,
  "gpt-3.5": 0.015,
  "claude-2": 0.02
}
```

### Example Input File

```
This is an example input text.
It will be tokenized and used for cost calculation.
```

### Example Output

#### Human-Readable Format
```
Model Comparison:
  model   tokens   cost
  gpt-4       12  0.00036
  claude-2    12  0.00024
```

#### JSON Format
```json
[
  {
    "model": "gpt-4",
    "tokens": 12,
    "cost": 0.00036
  },
  {
    "model": "claude-2",
    "tokens": 12,
    "cost": 0.00024
  }
]
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_api_cost_calculator.py
```

## License

This project is licensed under the MIT License.
