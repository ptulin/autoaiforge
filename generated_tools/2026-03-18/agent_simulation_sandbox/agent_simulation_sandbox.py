import json
import importlib.util
import os
import sys
import gym
import click
import matplotlib.pyplot as plt

def load_agent(agent_path):
    """Dynamically load the agent script."""
    if not os.path.exists(agent_path):
        raise FileNotFoundError(f"Agent script not found: {agent_path}")

    spec = importlib.util.spec_from_file_location("agent", agent_path)
    agent_module = importlib.util.module_from_spec(spec)
    sys.modules["agent"] = agent_module
    spec.loader.exec_module(agent_module)

    if not hasattr(agent_module, "Agent"):
        raise AttributeError("Agent script must define a class named 'Agent'.")

    return agent_module.Agent()

def load_scenario(config_path):
    """Load the scenario configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Scenario configuration file not found: {config_path}")

    with open(config_path, "r") as file:
        return json.load(file)

def run_simulation(agent, env_name, max_steps):
    """Run the simulation with the given agent and environment."""
    env = gym.make(env_name)
    observation = env.reset()
    total_reward = 0
    steps = 0

    while steps < max_steps:
        action = agent.act(observation)
        observation, reward, done, _ = env.step(action)
        total_reward += reward
        steps += 1

        if done:
            break

    env.close()
    return total_reward, steps

def visualize_results(results):
    """Visualize the simulation results."""
    plt.plot(results["steps"], results["rewards"], marker="o")
    plt.title("Agent Performance")
    plt.xlabel("Steps")
    plt.ylabel("Cumulative Reward")
    plt.grid()
    plt.show()

@click.command()
@click.option("--config", required=True, type=click.Path(exists=True), help="Path to the scenario configuration file.")
@click.option("--agent", required=True, type=click.Path(exists=True), help="Path to the agent script.")
def main(config, agent):
    """Agent Simulation Sandbox CLI."""
    try:
        scenario = load_scenario(config)
        agent_instance = load_agent(agent)

        env_name = scenario.get("environment")
        max_steps = scenario.get("max_steps", 1000)

        if not env_name:
            raise ValueError("Scenario configuration must specify an 'environment'.")

        total_reward, steps = run_simulation(agent_instance, env_name, max_steps)

        results = {
            "total_reward": total_reward,
            "steps": list(range(1, steps + 1)),
            "rewards": [total_reward / steps] * steps
        }

        print("Simulation completed.")
        print(f"Total Reward: {total_reward}")
        print(f"Steps Taken: {steps}")

        visualize_results(results)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
