# Token Budget Manager

Token Budget Manager is a Python library designed to help developers enforce token limits on AI agents dynamically. It allows tracking token consumption per agent or session, automatically enforces token limits, and provides customizable warnings and error handling when limits are exceeded.

## Features

- **Token consumption tracking**: Monitor token usage per agent or session.
- **Automatic enforcement of token limits**: Prevent exceeding predefined token budgets.
- **Customizable warnings and error handling**: Define token costs for specific API calls and handle limit exceedance gracefully.

## Installation

Install the library using pip:

```bash
pip install tiktoken pytest
```

## Usage

```python
from token_budget_manager import TokenBudgetManager

def mock_api_call():
    return "This is a response from the API."

# Initialize the TokenBudgetManager with a token limit and optional token costs
manager = TokenBudgetManager(token_limit=1000, token_costs={"mock_api": 50})

try:
    # Track an API call
    response = manager.track(mock_api_call, api_name="mock_api")
    print("API Response:", response)
    print("Remaining tokens:", manager.get_remaining_tokens())
except RuntimeError as e:
    print("Error:", e)

# Reset the token tracker
manager.reset()
print("Tokens after reset:", manager.get_remaining_tokens())
```

## Testing

Run the tests using pytest:

```bash
pytest test_token_budget_manager.py
```

## License

This project is licensed under the MIT License.
