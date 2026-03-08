# Dataset Explorer for GPT-5.4

## Description
Dataset Explorer for GPT-5.4 is a Python tool that allows users to analyze large datasets (e.g., CSV or Excel files) using natural language queries. By leveraging OpenAI's GPT-5.4, the tool provides insights, summaries, and statistics directly from datasets, even those spanning millions of rows.

## Features
- Handles datasets of significant size using batching and streaming.
- Supports natural language queries for intuitive data exploration.
- Outputs human-readable insights and visual summaries.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dataset_explorer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python dataset_explorer.py --input <path_to_dataset> --query <natural_language_query> --api_key <your_openai_api_key>
```

### Example
```bash
python dataset_explorer.py --input data.csv --query "Summarize sales by region" --api_key "your_api_key"
```

To save the output to a file, use the `--output` argument:
```bash
python dataset_explorer.py --input data.csv --query "Summarize sales by region" --api_key "your_api_key" --output report.txt
```

## Requirements
- Python 3.8+
- Required Python packages:
  - openai==0.27.8
  - pandas==1.5.3
  - matplotlib==3.7.1

## Testing
Run the tests using pytest:
```bash
pytest test_dataset_explorer.py
```

## Notes
- Ensure you have a valid OpenAI API key to use this tool.
- The tool supports CSV and Excel file formats.

## License
MIT License