# GPT Efficiency Benchmark

## Description
GPT Efficiency Benchmark is a CLI tool designed to benchmark the processing speed, memory usage, and token throughput of GPT-5 against previous GPT models. It automates testing using predefined prompts and datasets, generating detailed comparison metrics to help developers understand efficiency gains in real-world scenarios.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python gpt_efficiency_benchmark.py --models gpt-4,gpt-5 --prompts prompts.json --output report.html
```

## Features
- Benchmark GPT-5 against older models
- Analyze token throughput, latency, and memory usage
- Generate visual performance comparison reports

## Example
1. Create a `prompts.json` file with prompts:
```json
[
    "What is AI?",
    "Explain quantum physics."
]
```
2. Run the tool:
```bash
python gpt_efficiency_benchmark.py --models gpt-4,gpt-5 --prompts prompts.json --output report.html
```
3. Open `report.html` to view the detailed benchmark report.

## Requirements
- Python 3.8+
- `openai==0.27.0`
- `psutil==5.9.5`
- `matplotlib==3.7.2`

## License
MIT License