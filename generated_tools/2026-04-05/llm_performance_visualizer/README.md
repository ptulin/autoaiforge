# LLM Performance Visualizer

## Description
The LLM Performance Visualizer is a CLI tool designed to benchmark large language models (LLMs) across various dataset slices and visualize their performance trends. It helps researchers and developers pinpoint bottlenecks and areas for improvement in model performance.

## Features
- Benchmark LLMs against dataset slices.
- Supports multiple evaluation metrics (accuracy, perplexity).
- Generates heatmaps and line charts for performance diagnostics.
- Outputs a summary report in CSV format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/llm_performance_visualizer.git
   cd llm_performance_visualizer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Example Command
```bash
python llm_performance_visualizer.py --model gpt2 --dataset data.jsonl --metric accuracy
```

### Arguments
- `--model`: Hugging Face model name (e.g., `gpt2`).
- `--dataset`: Path to dataset file (CSV or JSONL).
- `--metric`: Evaluation metric (`accuracy` or `perplexity`).
- `--output_dir`: Directory to save visualizations and report (default: `output`).

### Output
- Heatmaps and line charts saved as images.
- A summary report saved as a CSV file.

## Testing
Run tests using pytest:
```bash
pytest test_llm_performance_visualizer.py
```

## License
MIT License