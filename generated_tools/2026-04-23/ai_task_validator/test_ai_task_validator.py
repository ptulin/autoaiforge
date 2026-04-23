import pytest
from unittest.mock import patch
from ai_task_validator import validate_tasks

def test_valid_tasks():
    tasks = [
        {"id": "task1", "dependencies": [], "inputs": ["input1"], "outputs": ["output1"]},
        {"id": "task2", "dependencies": ["task1"], "inputs": ["output1"], "outputs": ["output2"]}
    ]
    result = validate_tasks(tasks)
    assert result["status"] == "success"
    assert len(result["optimizations"]) == 0

def test_circular_dependency():
    tasks = [
        {"id": "task1", "dependencies": ["task2"], "inputs": ["input1"], "outputs": ["output1"]},
        {"id": "task2", "dependencies": ["task1"], "inputs": ["output1"], "outputs": ["output2"]}
    ]
    result = validate_tasks(tasks)
    assert result["status"] == "error"
    assert "Circular dependencies detected." in result["message"]

def test_missing_dependency():
    tasks = [
        {"id": "task1", "dependencies": ["task2"], "inputs": ["input1"], "outputs": ["output1"]}
    ]
    result = validate_tasks(tasks)
    assert result["status"] == "error"
    assert "Missing dependencies found." in result["message"]
    assert len(result["details"]) == 1
    assert result["details"][0]["task"] == "task1"
    assert result["details"][0]["missing_dependency"] == "task2"

def test_optimization_suggestion():
    tasks = [
        {"id": "task1", "dependencies": [], "inputs": ["input1"], "outputs": ["output1"]},
        {"id": "task2", "dependencies": ["task1"], "inputs": ["output1"], "outputs": ["output2"]},
        {"id": "task3", "dependencies": ["task2"], "inputs": ["output1"], "outputs": ["output3"]}
    ]
    result = validate_tasks(tasks)
    assert result["status"] == "success"
    assert len(result["optimizations"]) == 1
    assert result["optimizations"][0]["task"] == "task1"
    assert result["optimizations"][0]["output"] == "output1"
    assert "Consider optimizing the output 'output1' to avoid redundancy." in result["optimizations"][0]["suggestion"]