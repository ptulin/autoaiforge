# GPT Cost Analyzer

## Description
GPT Cost Analyzer is a Python tool designed to help developers and teams compare the cost efficiency of OpenAI's GPT-5 model against earlier models like GPT-4. By calculating tokens-per-dollar based on OpenAI's pricing and efficiency data, this tool provides insights into the financial impact of migrating workloads to GPT-5. It supports bulk evaluation of multiple prompts and generates detailed cost savings analysis.

## Features
- Calculate tokens-per-dollar for GPT models.
- Supports bulk evaluation of multiple prompts.
- Generates cost savings analysis for migration scenarios.
- Outputs results in CSV or JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gpt-cost-analyzer.git
   cd gpt-cost-analyzer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

```bash
python gpt_cost_analyzer.py --models gpt-4,gpt-5 --prompts prompts.json --pricing pricing.json --output results.csv --format csv
```

### Arguments
- `--models`: Comma-separated list of GPT models to analyze (e.g., `gpt-4,gpt-5`).
- `--prompts`: Path to a JSON file containing an array of prompts.
- `--pricing`: Path to a JSON file containing pricing data for GPT models.
- `--output`: Path to the output file (CSV or JSON format).
- `--format`: Output file format (`csv` or `json`).

### Example Input Files

#### prompts.json
```json
[
    "What is the capital of France?",
    "Explain the theory of relativity."
]
```

#### pricing.json
```json
{
    "gpt-4": {
        "price_per_1k_tokens": 0.03
    },
    "gpt-5": {
        "price_per_1k_tokens": 0.02
    }
}
```

### Example Output (CSV)

| model  | total_tokens | tokens_per_dollar |
|--------|--------------|-------------------|
| gpt-4  | 10           | 333.33            |
| gpt-5  | 10           | 500.00            |

### Example Output (JSON)

```json
[
    {
        "model": "gpt-4",
        "total_tokens": 10,
        "tokens_per_dollar": 333.33
    },
    {
        "model": "gpt-5",
        "total_tokens": 10,
        "tokens_per_dollar": 500.00
    }
]
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_gpt_cost_analyzer.py
```

## License

MIT License