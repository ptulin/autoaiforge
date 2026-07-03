import simpy
import pandas as pd
from typing import Callable, Dict, List

class Simulation:
    def __init__(self, env_config: Dict):
        """Initialize the simulation environment.

        Args:
            env_config (Dict): Configuration for the simulation environment.
        """
        self.env = simpy.Environment()
        self.env_config = env_config
        self.agents = []
        self.tasks = []
        self.logs = []

    def add_agent(self, agent_func: Callable):
        """Add an agent to the simulation.

        Args:
            agent_func (Callable): A function defining the agent's behavior.
        """
        self.agents.append(agent_func)

    def add_task(self, task_func: Callable):
        """Add a task to the simulation.

        Args:
            task_func (Callable): A function defining the task.
        """
        self.tasks.append(task_func)

    def run(self, until: int):
        """Run the simulation.

        Args:
            until (int): The number of simulation time units to run.
        """
        for task in self.tasks:
            self.env.process(task(self.env, self.logs))

        for agent in self.agents:
            self.env.process(agent(self.env, self.logs))

        self.env.run(until=until)

    def get_metrics(self) -> pd.DataFrame:
        """Generate performance metrics from the simulation logs.

        Returns:
            pd.DataFrame: A DataFrame containing performance metrics.
        """
        df = pd.DataFrame(self.logs)
        if not df.empty:
            df['completion_time'] = df['end_time'] - df['start_time']
        return df

# Example agent and task definitions
def example_agent(env, logs):
    while True:
        start_time = env.now
        yield env.timeout(5)  # Simulate agent work
        end_time = env.now
        logs.append({'type': 'agent', 'start_time': start_time, 'end_time': end_time})

def example_task(env, logs):
    while True:
        start_time = env.now
        yield env.timeout(10)  # Simulate task duration
        end_time = env.now
        logs.append({'type': 'task', 'start_time': start_time, 'end_time': end_time})

if __name__ == "__main__":
    # Example usage
    env_config = {}
    sim = Simulation(env_config)
    sim.add_agent(example_agent)
    sim.add_task(example_task)
    sim.run(until=50)
    metrics = sim.get_metrics()
    print(metrics)