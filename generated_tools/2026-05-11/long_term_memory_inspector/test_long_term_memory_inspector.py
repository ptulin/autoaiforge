import pytest
from long_term_memory_inspector import MemoryInspector

def test_query():
    memory_data = ["Learned about pandas", "AI ethics discussion", "Reinforcement learning"]
    inspector = MemoryInspector(memory_data)
    result = inspector.query("pandas")
    assert result == ["Learned about pandas"]

def test_prune():
    memory_data = ["Learned about pandas", "AI ethics discussion", "Reinforcement learning"]
    inspector = MemoryInspector(memory_data)
    result = inspector.prune(lambda x: "pandas" in x)
    assert result == ["AI ethics discussion", "Reinforcement learning"]

def test_summarize():
    memory_data = ["Learned about pandas", "AI ethics discussion", "Reinforcement learning"]
    inspector = MemoryInspector(memory_data)
    result = inspector.summarize(width=30)
    assert result == "Learned about pandas, AI..."

def test_query_dict():
    memory_data = {"entry1": "Learned about pandas", "entry2": "AI ethics discussion"}
    inspector = MemoryInspector(memory_data)
    result = inspector.query("pandas")
    assert result == {"entry1": "Learned about pandas"}

def test_prune_dict():
    memory_data = {"entry1": "Learned about pandas", "entry2": "AI ethics discussion"}
    inspector = MemoryInspector(memory_data)
    result = inspector.prune(lambda x: "pandas" in x)
    assert result == {"entry2": "AI ethics discussion"}