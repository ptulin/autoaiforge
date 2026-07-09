# Session-Aware LLM Limiter

## Description
The Session-Aware LLM Limiter is a Python library that provides a session-aware mechanism to limit interactions with large language models. It monitors user behavior, including query frequency and session durations, and triggers warnings or blocks further interactions when thresholds are exceeded. This ensures healthy usage patterns and prevents user fatigue.

## Features
- Customizable thresholds for interactions and session limits.
- Real-time monitoring of user engagement metrics.
- Hooks for alerting and throttling mechanisms.

## Installation
1. Clone the repository or download the `session_aware_llm_limiter.py` file.
2. Install the required dependencies:
   ```bash
   pip install pytest==7.4.2
   ```

## Usage
```python
from session_aware_llm_limiter import Limiter

# Initialize the limiter with custom thresholds
limiter = Limiter(query_limit=100, session_duration=3600)

# Log interactions
limiter.log_interaction(user_id='123')

# Export session data
print(limiter.export_sessions())

# Reset a user's session
limiter.reset_session(user_id='123')
```

## CLI Example
You can also initialize the limiter via the command line:
```bash
python session_aware_llm_limiter.py --query_limit 100 --session_duration 3600
```

## Testing
Run the test suite using pytest:
```bash
pytest test_session_aware_llm_limiter.py
```

## License
This project is licensed under the MIT License.