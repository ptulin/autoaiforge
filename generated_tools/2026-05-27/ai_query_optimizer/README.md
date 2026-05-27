# AI Query Optimizer

## Description
The AI Query Optimizer leverages OpenAI's API to analyze and optimize search queries by suggesting refined keywords and query structures for better search results. Developers can integrate this tool into applications to enhance search accuracy and relevance.

## Installation

1. Install Python 3.7 or later.
2. Install the required packages:
   ```bash
   pip install openai pytest
   ```

## Usage

Run the tool from the command line:

```bash
python ai_query_optimizer.py --query "example query" --api_key YOUR_API_KEY --output optimized_query.json --format json
```

### Arguments

- `--query`: The search query to optimize.
- `--input_file`: Path to a text file containing the search query.
- `--output`: File path to save the optimized query.
- `--format`: Output format (`json` or `text`). Default is `json`.
- `--api_key`: Your OpenAI API key (required).

## Testing

Run the tests using pytest:

```bash
pytest test_ai_query_optimizer.py
```

## License

This project is licensed under the MIT License.