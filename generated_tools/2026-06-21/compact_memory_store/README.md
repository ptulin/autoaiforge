# Compact Memory Store

## Description
Compact Memory Store is a lightweight Python library for storing and retrieving AI agent memory snapshots in a memory-efficient, compact format. It uses techniques like deduplication and compression to reduce memory footprint and speed up memory access, making it ideal for long-running agent workflows.

## Features
- **Efficient Deduplication**: Avoids storing duplicate memory entries.
- **Compression Support**: Reduces storage size using the `lz4` compression library.
- **Fast Retrieval**: Includes an in-memory cache with configurable size for quick access to frequently used memory entries.

## Installation
To install the required dependencies, run:

```bash
pip install numpy==1.23.5 lz4==4.3.2
```

## Usage

### Example
```python
from compact_memory_store import MemoryStore

# Initialize the memory store
store = MemoryStore(cache_size=50)

# Add memory
store.add_memory('key1', {'input': 'hello', 'response': 'world'})

# Retrieve memory
print(store.retrieve_memory('key1'))  # Output: {'input': 'hello', 'response': 'world'}

# Delete memory
store.delete_memory('key1')
print(store.retrieve_memory('key1'))  # Output: None

# Clear all memory
store.clear_memory()
```

### CLI Usage
You can also interact with the memory store using the command line interface:

```bash
python compact_memory_store.py add --key key1 --data "{'input': 'hello', 'response': 'world'}"
python compact_memory_store.py retrieve --key key1
python compact_memory_store.py delete --key key1
python compact_memory_store.py clear
```

## License
This project is licensed under the MIT License.
