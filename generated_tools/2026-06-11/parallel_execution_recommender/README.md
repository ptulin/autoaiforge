# Parallel Execution Recommender

Parallel Execution Recommender analyzes Python code to identify sequential operations that could be parallelized for better performance. It uses OpenAI's API to detect opportunities for multiprocessing or threading and suggests rewrites to improve runtime efficiency.

## Installation

1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line:

```bash
python parallel_execution_recommender.py --script <path_to_python_script> --api-key <your_openai_api_key>
```

- `--script`: Path to the Python script you want to analyze.
- `--api-key`: Your OpenAI API key.

## Testing

To run the tests, install `pytest` if you haven't already:

```bash
pip install pytest
```

Then run:

```bash
pytest test_parallel_execution_recommender.py
```

All tests should pass without requiring network access, as external API calls are mocked.

## Requirements

- Python 3.7+
- `openai`
- `pytest`

## License

This project is licensed under the MIT License.