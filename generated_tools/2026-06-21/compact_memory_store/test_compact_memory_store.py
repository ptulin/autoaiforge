import pytest
from unittest.mock import patch
from compact_memory_store import MemoryStore

def test_add_and_retrieve_memory():
    store = MemoryStore()
    store.add_memory("test_key", {"input": "hello", "response": "world"})
    result = store.retrieve_memory("test_key")
    assert result == {"input": "hello", "response": "world"}

def test_retrieve_nonexistent_key():
    store = MemoryStore()
    result = store.retrieve_memory("nonexistent_key")
    assert result is None

def test_delete_memory():
    store = MemoryStore()
    store.add_memory("test_key", {"input": "hello", "response": "world"})
    store.delete_memory("test_key")
    result = store.retrieve_memory("test_key")
    assert result is None

def test_cache_eviction():
    store = MemoryStore(cache_size=2)
    store.add_memory("key1", "data1")
    store.add_memory("key2", "data2")
    store.add_memory("key3", "data3")

    assert "key1" not in store.cache
    assert "key2" in store.cache
    assert "key3" in store.cache

def test_clear_memory():
    store = MemoryStore()
    store.add_memory("key1", "data1")
    store.add_memory("key2", "data2")
    store.clear_memory()
    assert store.retrieve_memory("key1") is None
    assert store.retrieve_memory("key2") is None