import argparse
import asyncio
import json
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError
import openai

class AgentConfig(BaseModel):
    name: str
    role: str
    tasks: List[str]

class TaskMessage(BaseModel):
    sender: str
    task: str
    content: str

class MultiAgentOrchestrator:
    def __init__(self, config: Dict[str, Any]):
        self.agents = [AgentConfig(**agent) for agent in config.get("agents", [])]
        self.messages = asyncio.Queue()

    async def run(self):
        tasks = [self._run_agent(agent) for agent in self.agents]
        await asyncio.gather(*tasks)

    async def _run_agent(self, agent: AgentConfig):
        for task in agent.tasks:
            await self._process_task(agent, task)

    async def _process_task(self, agent: AgentConfig, task: str):
        try:
            response = await self._simulate_openai_call(agent, task)
            message = TaskMessage(sender=agent.name, task=task, content=response)
            await self.messages.put(message)
            print(f"[{agent.name}] Completed task '{task}': {response}")
        except Exception as e:
            print(f"[{agent.name}] Error processing task '{task}': {e}")

    async def _simulate_openai_call(self, agent: AgentConfig, task: str) -> str:
        await asyncio.sleep(1)  # Simulate API delay
        return f"Simulated response for {task} by {agent.role}"

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-Agent Orchestrator")
    parser.add_argument("--config", required=True, help="Path to configuration JSON file")
    return parser.parse_args()

def main():
    args = parse_args()

    try:
        with open(args.config, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: Configuration file not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in configuration file.")
        return

    try:
        orchestrator = MultiAgentOrchestrator(config)
        asyncio.run(orchestrator.run())
    except ValidationError as e:
        print(f"Configuration validation error: {e}")

if __name__ == "__main__":
    main()