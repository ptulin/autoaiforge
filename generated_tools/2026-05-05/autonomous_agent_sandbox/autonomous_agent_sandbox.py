import json
import yaml
import gym
import pandas as pd
import typer
from pathlib import Path
from typing import Optional

app = typer.Typer()

def load_scenario(file_path: str):
    """Load scenario configuration from a JSON or YAML file."""
    try:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                return json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format. Use JSON or YAML.")
    except FileNotFoundError:
        typer.echo("Scenario file not found.")
        raise
    except Exception as e:
        typer.echo(f"Error loading scenario: {e}")
        raise

def load_agent(file_path: str):
    """Load agent logic from a Python file."""
    try:
        agent_globals = {}
        with open(file_path, 'r') as f:
            exec(f.read(), agent_globals)
        if 'Agent' not in agent_globals:
            raise ValueError("Agent class not found in the provided file.")
        return agent_globals['Agent']
    except FileNotFoundError:
        typer.echo("Agent file not found.")
        raise
    except Exception as e:
        typer.echo(f"Error loading agent: {e}")
        raise

def run_simulation(scenario: dict, agent_class):
    """Run the simulation based on the scenario and agent logic."""
    env_name = scenario.get("environment", "CartPole-v1")
    try:
        env = gym.make(env_name)
    except gym.error.Error as e:
        typer.echo(f"Error creating environment: {e}")
        raise

    agent = agent_class()
    logs = []

    for episode in range(scenario.get("episodes", 10)):
        observation = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.act(observation)
            observation, reward, done, info = env.step(action)
            total_reward += reward
            logs.append({
                "episode": episode,
                "observation": observation,
                "action": action,
                "reward": reward,
                "done": done
            })

    env.close()

    return pd.DataFrame(logs)

@app.command()
def main(scenario: str, agent: str, output: Optional[str] = None):
    """Run the Autonomous Agent Sandbox simulation."""
    try:
        scenario_config = load_scenario(scenario)
        agent_class = load_agent(agent)
        results = run_simulation(scenario_config, agent_class)

        if output:
            results.to_csv(output, index=False)
            typer.echo(f"Simulation results saved to {output}")
        else:
            typer.echo(results.head())

    except Exception as e:
        typer.echo(f"Simulation failed: {e}")

if __name__ == "__main__":
    app()
