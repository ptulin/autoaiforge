import pytest
import asyncio
import json
from unittest.mock import AsyncMock, patch
from multi_agent_orchestrator import MultiAgentOrchestrator, AgentConfig

@pytest.fixture
def sample_config():
    return {
        "agents": [
            {"name": "Agent1", "role": "Developer", "tasks": ["Task1", "Task2"]},
            {"name": "Agent2", "role": "Reviewer", "tasks": ["Task3"]}
        ]
    }

@pytest.mark.asyncio
async def test_orchestrator_run(sample_config):
    orchestrator = MultiAgentOrchestrator(sample_config)
    with patch("multi_agent_orchestrator.MultiAgentOrchestrator._simulate_openai_call", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = "Mocked response"
        await orchestrator.run()

    assert not orchestrator.messages.empty()
    messages = []
    while not orchestrator.messages.empty():
        messages.append(await orchestrator.messages.get())

    assert len(messages) == 3
    assert messages[0].sender == "Agent1"
    assert messages[1].sender == "Agent1"
    assert messages[2].sender == "Agent2"

@pytest.mark.asyncio
async def test_agent_task_processing(sample_config):
    orchestrator = MultiAgentOrchestrator(sample_config)
    agent = orchestrator.agents[0]

    with patch("multi_agent_orchestrator.MultiAgentOrchestrator._simulate_openai_call", new_callable=AsyncMock) as mock_api:
        mock_api.return_value = "Mocked response"
        await orchestrator._process_task(agent, "Task1")

    assert not orchestrator.messages.empty()
    message = await orchestrator.messages.get()
    assert message.sender == "Agent1"
    assert message.task == "Task1"
    assert message.content == "Mocked response"

@pytest.mark.asyncio
async def test_invalid_config():
    invalid_config = {
        "agents": [
            {"name": "Agent1", "role": "Developer"}  # Missing 'tasks'
        ]
    }

    with pytest.raises(Exception):
        MultiAgentOrchestrator(invalid_config)