# AI Model Benchmark Tool

## Description
This tool allows developers to benchmark GPT-5 and Claude 4.7 against a custom dataset of prompts. It evaluates response quality using metrics like response length, latency, and BLEU score (for reference-based evaluation), generating a comparative report. Useful for developers optimizing workflows.

## Installation

1. Install the required Python packages:

```bash
pip install pandas nltk openai anthropic
```

2. Ensure you have access to the GPT-5 and Claude 4.7 APIs.

## Usage

Run the tool using the following command:

```bash
python ai_model_benchmark.py --dataset <path_to_dataset> --output <path_to_output_report>
```

- `--dataset`: Path to the dataset file (JSON or CSV).
- `--output`: Path to the output report file (JSON or HTML).

## Testing

To run the tests, use:

```bash
pytest test_ai_model_benchmark.py
```

## Notes
- Replace `YOUR_ANTHROPIC_API_KEY` in the code with your actual API key for the Claude API.
- Ensure the dataset file contains prompts and optionally references for BLEU score calculation.

## Example

Dataset file (`dataset.json`):

```json
[
  {"prompt": "What is AI?", "reference": "Artificial Intelligence is the simulation of human intelligence."}
]
```

Command:

```bash
python ai_model_benchmark.py --dataset dataset.json --output report.html
```

Output (`report.html`):

```html
<html>
<head><title>AI Model Benchmark Report</title></head>
<body>
<h1>AI Model Benchmark Report</h1>
<h2>GPT-5</h2>
<table border='1'>
<tr><th>Prompt</th><th>Response</th><th>Latency</th><th>Response Length</th><th>BLEU Score</th></tr>
<tr><td>What is AI?</td><td>Artificial Intelligence is the simulation of human intelligence.</td><td>0.10</td><td>50</td><td>1.0</td></tr>
</table>
<h2>Claude-4.7</h2>
<table border='1'>
<tr><th>Prompt</th><th>Response</th><th>Latency</th><th>Response Length</th><th>BLEU Score</th></tr>
<tr><td>What is AI?</td><td>Artificial Intelligence is the simulation of human intelligence.</td><td>0.10</td><td>50</td><td>1.0</td></tr>
</table>
</body>
</html>
```