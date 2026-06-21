import os
import pickle
import lz4.frame
from collections import OrderedDict
import numpy as np

class MemoryStore:
    def __init__(self, cache_size=100):
        """
        Initialize the MemoryStore.

        Args:
            cache_size (int): Maximum number of items to keep in the in-memory cache.
        """
        self.memory = {}
        self.cache = OrderedDict()
        self.cache_size = cache_size

    def add_memory(self, key, data):
        """
        Add a memory snapshot to the store.

        Args:
            key (str): Unique identifier for the memory.
            data (object): The memory data to store (e.g., dict, list, string).
        """
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")

        serialized_data = pickle.dumps(data)
        compressed_data = lz4.frame.compress(serialized_data)
        self.memory[key] = compressed_data

        # Update cache
        self._update_cache(key, data)

    def retrieve_memory(self, key):
        """
        Retrieve a memory snapshot by its key.

        Args:
            key (str): Unique identifier for the memory.

        Returns:
            object: The decompressed memory data.
        """
        if key in self.cache:
            return self.cache[key]

        compressed_data = self.memory.get(key)
        if compressed_data is None:
            return None

        serialized_data = lz4.frame.decompress(compressed_data)
        data = pickle.loads(serialized_data)

        # Update cache
        self._update_cache(key, data)

        return data

    def _update_cache(self, key, data):
        """
        Update the in-memory cache with the given key and data.

        Args:
            key (str): The key to update in the cache.
            data (object): The data to cache.
        """
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.cache_size:
            self.cache.popitem(last=False)

        self.cache[key] = data

    def delete_memory(self, key):
        """
        Delete a memory snapshot by its key.

        Args:
            key (str): Unique identifier for the memory.
        """
        if key in self.memory:
            del self.memory[key]
        if key in self.cache:
            del self.cache[key]

    def clear_memory(self):
        """
        Clear all stored memory and cache.
        """
        self.memory.clear()
        self.cache.clear()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compact Memory Store CLI")
    parser.add_argument("action", choices=["add", "retrieve", "delete", "clear"], help="Action to perform on the memory store.")
    parser.add_argument("--key", type=str, help="Key for the memory entry.")
    parser.add_argument("--data", type=str, help="Data to store (as a string).")

    args = parser.parse_args()

    store = MemoryStore()

    if args.action == "add":
        if args.key is None or args.data is None:
            print("Error: Both --key and --data are required for 'add' action.")
        else:
            store.add_memory(args.key, args.data)
            print(f"Memory added with key: {args.key}")

    elif args.action == "retrieve":
        if args.key is None:
            print("Error: --key is required for 'retrieve' action.")
        else:
            data = store.retrieve_memory(args.key)
            if data is None:
                print("No memory found for the given key.")
            else:
                print(f"Retrieved memory: {data}")

    elif args.action == "delete":
        if args.key is None:
            print("Error: --key is required for 'delete' action.")
        else:
            store.delete_memory(args.key)
            print(f"Memory deleted with key: {args.key}")

    elif args.action == "clear":
        store.clear_memory()
        print("All memory cleared.")