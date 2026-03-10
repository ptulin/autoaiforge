# Agent Interaction Logger

## Description
This library intercepts and logs interactions between Nvidia's open-source AI agents and their environments. It provides developers with detailed, structured logs of agent decisions, state transitions, and environment feedback, which are essential for debugging, performance tuning, and creating reproducible experiments.

## Features
- Log interactions between agents and environments.
- Save logs in JSON or CSV format.
- Filter logs using custom filter functions.

## Installation
Install the required dependencies:

```bash
pip install loguru pandas
```

## Usage
Run the logger from the command line:

```bash
python agent_interaction_logger.py --output_path logs --log_format json --filename interactions
```

### Example Code
```python
from agent_interaction_logger import InteractionLogger

logger_instance = InteractionLogger(output_path="logs", log_format="json")

logger_instance.log_interaction(
    agent_state={"position": [0, 0], "health": 100},
    action={"move": "forward"},
    environment_feedback={"reward": 10, "done": False}
)

logger_instance.save_logs(filename="interactions")
```

## Testing
To run the tests:

```bash
pytest test_agent_interaction_logger.py
```

## License
MIT License