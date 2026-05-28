# Persistent Agent Memory

## Description
Persistent Agent Memory is a lightweight Python library that provides a flexible system for AI agents to store and retrieve persistent memories. It supports multiple storage backends, including SQLite, JSON files, and Redis, making it easy to integrate into various AI frameworks. This allows AI agents to maintain state, identity, and context across sessions.

## Features
- **Multiple Backends**: Supports SQLite, JSON files, and Redis.
- **Flexible Schema**: Store agent states and memories in a structured format.
- **Simple API**: Save, retrieve, and delete agent states with ease.

## Installation
Install the library using pip:

```bash
pip install -r requirements.txt
```

## Usage

### Example
```python
from persistent_agent_memory import AgentMemory

# Using SQLite backend
memory = AgentMemory(backend='sqlite', db_path='memory.db')
memory.save_state(agent_id='agent_123', state={'mood': 'happy'})
print(memory.load_state('agent_123'))  # Output: {'mood': 'happy'}
memory.delete_state('agent_123')

# Using JSON backend
memory = AgentMemory(backend='json', file_path='memory.json')
memory.save_state(agent_id='agent_456', state={'mood': 'curious'})
print(memory.load_state('agent_456'))  # Output: {'mood': 'curious'}
memory.delete_state('agent_456')

# Using Redis backend
memory = AgentMemory(backend='redis', host='localhost', port=6379)
memory.save_state(agent_id='agent_789', state={'mood': 'excited'})
print(memory.load_state('agent_789'))  # Output: {'mood': 'excited'}
memory.delete_state('agent_789')
```

## Testing
Run the tests using pytest:

```bash
pytest test_persistent_agent_memory.py
```

## License
MIT License