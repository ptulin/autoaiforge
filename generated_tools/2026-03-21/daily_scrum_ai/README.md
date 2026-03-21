# Daily Scrum AI

## Overview
Daily Scrum AI is a command-line tool that summarizes recent project activity by analyzing task updates and generates a suggested agenda for daily Scrum meetings. The tool can also identify blockers and help prepare individual developer summaries based on task progress.

## Features
- Supports input files in CSV or JSON format.
- Summarizes task updates by developer.
- Generates a Scrum meeting agenda using OpenAI's GPT model.
- Identifies blockers and highlights task progress.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd daily_scrum_ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the command line:

```bash
python daily_scrum_ai.py --updates_file <path_to_updates_file> --openai_api_key <your_openai_api_key>
```

### Arguments
- `--updates_file`: Path to the project updates file (CSV or JSON).
- `--openai_api_key`: Your OpenAI API key for generating summaries.

### Example

```bash
python daily_scrum_ai.py --updates_file updates.csv --openai_api_key sk-xxxxxxxxxxxxxxxxxxxxxx
```

## Testing

To run the tests, install `pytest` and execute the following command:

```bash
pytest test_daily_scrum_ai.py
```

## Requirements
- Python 3.7+
- pandas
- python-dateutil
- openai

## Notes
- Ensure your input file contains the following columns: `task_id`, `developer`, `status`, `description`, `updated_at`.
- The `updated_at` column should contain valid date strings.
- The OpenAI API key is required to generate the Scrum agenda and summaries.

## License
This project is licensed under the MIT License.