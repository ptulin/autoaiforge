# Agent Workflow Designer

## Description
Agent Workflow Designer is a command-line tool that allows AI developers to design modular, reusable workflows for autonomous AI agents. By defining tasks and their interdependencies, developers can generate JSON or YAML blueprints to orchestrate agent behavior, making it easier to prototype and iterate on agentic AI systems.

## Features
- Interactive CLI for modular workflow design
- Supports adding/removing tasks and dependencies
- Generates agent workflow blueprints in JSON or YAML
- Easy-to-use interface for rapid prototyping

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/agent_workflow_designer.git
   cd agent_workflow_designer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using Python:
```bash
python agent_workflow_designer.py --output workflow.yaml
```

### Example Workflow
1. Add tasks:
   - Enter `add_task` and provide a task name.
2. Add dependencies:
   - Enter `add_dependency` and specify the source and target tasks.
3. Save the workflow:
   - Enter `save` to export the workflow as JSON or YAML.
4. Quit the tool:
   - Enter `quit` to exit.

## Example Output
```yaml
tasks:
  - Task1
  - Task2
dependencies:
  - [Task1, Task2]
```

## Testing
Run the tests using pytest:
```bash
pytest test_agent_workflow_designer.py
```
