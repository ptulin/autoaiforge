# Claude Subagent Orchestrator

## Description
The Claude Subagent Orchestrator is a Python-based automation tool designed to streamline and manage communication between multiple Claude subagents. It enables developers to define subagent roles, assign tasks, and track responses, making it easier to implement complex multi-agent workflows. The tool also provides logging and visualization of subagent communication for debugging purposes.

## Features
- Define and manage multiple Claude subagents with unique roles.
- Supports task prioritization and dependency resolution between subagents.
- Logs and visualizes communication between subagents for debugging.

## Installation
1. Clone the repository or download the `claude_subagent_orchestrator.py` file.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Create a JSON configuration file defining the subagents, their roles, and tasks. Example:
   ```json
   [
       {
           "name": "Agent1",
           "role": "Assistant",
           "tasks": ["Task1", "Task2"]
       },
       {
           "name": "Agent2",
           "role": "Helper",
           "tasks": ["Task3"]
       }
   ]
   ```
2. Run the tool using the following command:
   ```bash
   python claude_subagent_orchestrator.py --config subagents_config.json
   ```
3. View the task execution progress in the console and check the `subagent_communications.log` file for detailed logs.

## Example
```bash
python claude_subagent_orchestrator.py --config subagents_config.json
```

## Requirements
- Python 3.8+
- `openai==0.27.8`
- `rich==13.5.2`
- `pydantic==1.10.12`

## License
This project is licensed under the MIT License.
