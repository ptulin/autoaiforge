# Model Stability Benchmark

## Description
Model Stability Benchmark is a CLI tool designed to evaluate the stability of generative AI models by running multiple iterations of the same prompt and analyzing the consistency of the outputs. It provides metrics on output variance, token-level differences, and semantic similarity, helping developers identify how deterministic or stable their models are.

## Features
- Measures output consistency across multiple runs.
- Calculates token-level differences between outputs.
- Computes semantic similarity using cosine distance.
- Saves results to a CSV file for further analysis.

## Installation

1. Clone this repository:
   ```
   git clone <repository_url>
   cd model_stability_benchmark
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python model_stability_benchmark.py --api_key <your_openai_api_key> \
                                    --prompt "Translate this to French" \
                                    --iterations 10 \
                                    --output results.csv
```

### Arguments
- `--api_key`: Your OpenAI API key (required).
- `--prompt`: The prompt text to evaluate (required).
- `--iterations`: Number of iterations to run the prompt (required).
- `--output`: Path to the output CSV file (required).

## Example
```bash
python model_stability_benchmark.py --api_key "sk-abc123" \
                                    --prompt "Translate this to French" \
                                    --iterations 10 \
                                    --output results.csv
```

## Testing

Run the tests using `pytest`:
```bash
pytest test_model_stability_benchmark.py
```

## License
MIT License