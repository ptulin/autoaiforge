import argparse
import json
import logging
import os
import gym
import matplotlib.pyplot as plt
from gym import spaces

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path):
    """Load the simulation configuration from a JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as file:
        return json.load(file)

def create_environment(config):
    """Create a custom Gym environment based on the configuration."""
    class CustomEnv(gym.Env):
        def __init__(self):
            super(CustomEnv, self).__init__()
            self.action_space = spaces.Discrete(config['action_space'])
            self.observation_space = spaces.Box(
                low=config['observation_space']['low'],
                high=config['observation_space']['high'],
                shape=tuple(config['observation_space']['shape']),
                dtype=float
            )
            self.state = None
            self.steps = 0
            self.max_steps = config.get('max_steps', 100)

        def reset(self):
            self.state = config['initial_state']
            self.steps = 0
            return self.state

        def step(self, action):
            self.steps += 1
            reward = config['reward_function'](self.state, action)
            done = self.steps >= self.max_steps
            self.state = config['state_transition'](self.state, action)
            return self.state, reward, done, {}

        def render(self, mode='human'):
            if mode == 'human':
                print(f"State: {self.state}, Steps: {self.steps}")

    return CustomEnv()

def run_simulation(config_path, visualize):
    """Run the simulation based on the provided configuration."""
    config = load_config(config_path)
    env = create_environment(config)
    state = env.reset()

    states = []
    rewards = []

    for _ in range(config.get('max_steps', 100)):
        action = env.action_space.sample()  # Random action for simulation
        next_state, reward, done, _ = env.step(action)
        states.append(next_state)
        rewards.append(reward)
        env.render()
        if done:
            break

    if visualize:
        plt.plot(rewards)
        plt.title('Reward Over Time')
        plt.xlabel('Step')
        plt.ylabel('Reward')
        plt.show()

    logging.info("Simulation completed.")

def main():
    parser = argparse.ArgumentParser(description='Simulate AI Behavior in a customizable environment.')
    parser.add_argument('--config', required=True, help='Path to the JSON configuration file.')
    parser.add_argument('--visualize', action='store_true', help='Enable visualization of the simulation.')
    args = parser.parse_args()

    try:
        run_simulation(args.config, args.visualize)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()