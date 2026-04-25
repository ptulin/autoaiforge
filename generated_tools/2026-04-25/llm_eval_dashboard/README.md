# LLM Evaluation Dashboard

## Overview

The `llm_eval_dashboard` tool generates an interactive dashboard to visualize and compare the evaluation metrics of multiple large language models (LLMs) across diverse datasets. It supports metrics like BLEU, ROUGE, and latency, helping developers interpret results more effectively.

## Features

- Load evaluation data from JSON or CSV files.
- Filter results by model, dataset, and task.
- Visualize metrics using bar charts and line charts.
- Interactive Streamlit-based dashboard.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd llm_eval_dashboard
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python llm_eval_dashboard.py --data <path_to_data_file>
```

- `<path_to_data_file>`: Path to a JSON or CSV file containing evaluation results.

### Example Data Format

#### JSON Format
```json
[
    {"model": "GPT-5.5", "dataset": "Dataset1", "task": "Task1", "BLEU": 0.8, "latency": 1.2},
    {"model": "Claude Opus 4.7", "dataset": "Dataset2", "task": "Task2", "BLEU": 0.9, "latency": 1.5}
]
```

#### CSV Format
```csv
model,dataset,task,BLEU,latency
GPT-5.5,Dataset1,Task1,0.8,1.2
Claude Opus 4.7,Dataset2,Task2,0.9,1.5
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_eval_dashboard.py
```

The tests include:
- Loading data from JSON and CSV files.
- Handling invalid file formats.
- Mocking Streamlit components to test dashboard generation.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib

## License

This project is licensed under the MIT License.