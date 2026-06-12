import tiktoken
from typing import Callable, Dict, Optional

class TokenBudgetManager:
    def __init__(self, token_limit: int, token_costs: Optional[Dict[str, int]] = None):
        """
        Initialize the TokenBudgetManager.

        :param token_limit: The maximum number of tokens allowed.
        :param token_costs: A dictionary mapping API call names to their token costs.
        """
        if token_limit <= 0:
            raise ValueError("Token limit must be a positive integer.")
        
        self.token_limit = token_limit
        self.token_costs = token_costs or {}
        self.tokens_used = 0

    def track(self, api_call: Callable, api_name: Optional[str] = None, *args, **kwargs):
        """
        Track an API call's token usage and enforce token limits.

        :param api_call: The API call function to be tracked.
        :param api_name: The name of the API call (optional, used for token cost lookup).
        :param args: Positional arguments for the API call.
        :param kwargs: Keyword arguments for the API call.
        :return: The result of the API call.
        :raises: RuntimeError if the token limit is exceeded.
        """
        # Determine token cost for the API call
        token_cost = self.token_costs.get(api_name, 0)

        if self.tokens_used + token_cost > self.token_limit:
            raise RuntimeError("Token limit exceeded. Cannot proceed with the API call.")

        # Execute the API call
        result = api_call(*args, **kwargs)

        # Estimate tokens used by the result using tiktoken
        encoder = tiktoken.get_encoding("cl100k_base")
        result_tokens = len(encoder.encode(str(result)))

        # Update token usage
        self.tokens_used += token_cost + result_tokens

        if self.tokens_used > self.token_limit:
            raise RuntimeError("Token limit exceeded after processing the API call.")

        return result

    def reset(self):
        """
        Reset the token usage tracker.
        """
        self.tokens_used = 0

    def get_remaining_tokens(self) -> int:
        """
        Get the number of remaining tokens.

        :return: The number of tokens remaining.
        """
        return self.token_limit - self.tokens_used

if __name__ == "__main__":
    # Example usage
    def mock_api_call():
        return "This is a response from the API."

    manager = TokenBudgetManager(token_limit=1000, token_costs={"mock_api": 50})

    try:
        response = manager.track(mock_api_call, api_name="mock_api")
        print("API Response:", response)
        print("Remaining tokens:", manager.get_remaining_tokens())
    except RuntimeError as e:
        print("Error:", e)
