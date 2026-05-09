import json
import yaml
import click
import pandas as pd
import psutil
from typing import Dict, List, Union

class MultiAgentWorkloadBalancer:
    def __init__(self, config: Dict):
        self.agents = config['agents']
        self.tasks = config['tasks']
        self.policy = config['policy']

    def monitor_agents(self) -> Dict[str, float]:
        """Simulate agent health checks and load monitoring."""
        agent_loads = {}
        for agent in self.agents:
            cpu_usage = psutil.cpu_percent() / len(self.agents)  # Simulated CPU usage per agent
            agent_loads[agent['id']] = cpu_usage
        return agent_loads

    def balance_workload(self) -> List[Dict]:
        """Balance tasks based on policy and agent performance."""
        agent_loads = self.monitor_agents()
        task_assignments = []

        if self.policy == 'round-robin':
            agent_index = 0
            for task in self.tasks:
                agent = self.agents[agent_index % len(self.agents)]
                task_assignments.append({'task_id': task['id'], 'agent_id': agent['id']})
                agent_index += 1

        elif self.policy == 'priority-based':
            sorted_agents = sorted(self.agents, key=lambda a: agent_loads[a['id']])
            for task in self.tasks:
                agent = sorted_agents[0]  # Assign to least loaded agent
                task_assignments.append({'task_id': task['id'], 'agent_id': agent['id']})
                agent_loads[agent['id']] += task['complexity']

        return task_assignments

@click.command()
@click.option('--config', type=click.Path(exists=True), required=True, help='Path to configuration file (YAML/JSON).')
@click.option('--output', type=click.Path(), required=True, help='Path to output file for task assignments.')
def main(config: str, output: str):
    """Multi-Agent Workload Balancer CLI."""
    try:
        with open(config, 'r') as f:
            if config.endswith('.yaml'):
                config_data = yaml.safe_load(f)
            elif config.endswith('.json'):
                config_data = json.load(f)
            else:
                raise ValueError('Unsupported configuration file format. Use YAML or JSON.')

        balancer = MultiAgentWorkloadBalancer(config_data)
        assignments = balancer.balance_workload()

        with open(output, 'w') as f:
            json.dump(assignments, f, indent=4)

        click.echo(f'Task assignments saved to {output}')

    except Exception as e:
        click.echo(f'Error: {e}', err=True)

if __name__ == '__main__':
    main()
