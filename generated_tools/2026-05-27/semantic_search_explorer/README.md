# Semantic Search Explorer

Semantic Search Explorer is a Python CLI tool that allows developers to interact with AI-powered search engines. It helps in testing and exploring semantic search capabilities with custom queries, displaying structured results, metadata, and ranking insights.

## Features
- Perform semantic search using AI-enhanced APIs.
- Display search results in a formatted table with metadata like relevance scores and sources.
- Debug and experiment with query variations.

## Installation
1. Clone the repository or download the `semantic_search_explorer.py` file.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool from the command line:
```bash
python semantic_search_explorer.py --query "machine learning trends" --api_key YOUR_API_KEY
```

### Optional Arguments
- `--api_url`: Specify a custom API endpoint URL (default: `https://api.example.com/search`).

## Example
```bash
python semantic_search_explorer.py --query "AI advancements" --api_key YOUR_API_KEY
```

## Testing
Run the tests using pytest:
```bash
pytest test_semantic_search_explorer.py
```

## Requirements
- Python 3.7+
- `requests`
- `rich`
- `pytest`

## License
This project is licensed under the MIT License.