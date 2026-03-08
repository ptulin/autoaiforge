import pytest
from unittest.mock import MagicMock
from skill_registry_builder import SkillRegistry, register_skill, SkillMetadata

def sample_skill(name: str) -> str:
    return f"Hello, {name}!"

def test_register_skill():
    registry = SkillRegistry()
    metadata = {
        "name": "greet",
        "description": "Greets a user by name.",
        "inputs": {"name": "str"},
        "outputs": {"greeting": "str"}
    }
    registry.register_skill(sample_skill, SkillMetadata(**metadata))
    assert "greet" in registry.skills

def test_validate_skill():
    registry = SkillRegistry()
    metadata = {
        "name": "greet",
        "description": "Greets a user by name.",
        "inputs": {"name": "str"},
        "outputs": {"greeting": "str"}
    }
    registry.register_skill(sample_skill, SkillMetadata(**metadata))
    inputs = {"name": "Alice"}
    validated_inputs = registry.validate_skill("greet", inputs)
    assert validated_inputs == inputs

def test_execute_skill():
    registry = SkillRegistry()
    metadata = {
        "name": "greet",
        "description": "Greets a user by name.",
        "inputs": {"name": "str"},
        "outputs": {"greeting": "str"}
    }
    registry.register_skill(sample_skill, SkillMetadata(**metadata))
    inputs = {"name": "Alice"}
    result = registry.execute_skill("greet", inputs)
    assert result == "Hello, Alice!"
