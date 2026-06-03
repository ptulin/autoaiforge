# IDE Agent Integrator

## Description
The IDE Agent Integrator is a lightweight Python library designed to help developers integrate AI coding agents into popular IDEs like Visual Studio Code, PyCharm, and JetBrains IntelliJ. It facilitates interaction between the IDE and the agent via a local server, enabling features like code suggestions, automated debugging, and refactoring.

## Features
- **Easy IDE Integration**: Seamlessly connect your IDE to an AI coding agent.
- **Supports Multiple IDEs**: Compatible with Visual Studio Code, PyCharm, IntelliJ, and more.
- **Real-time Communication**: Enables real-time suggestions, debugging, and refactoring.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Create a configuration YAML file (e.g., `config.yaml`) with the following structure:

```yaml
ide: "VSCode"
agent_url: "http://localhost:8000"
```

2. Start the server:

```python
from ide_agent_integrator import start_server
start_server('config.yaml')
```

3. Use your IDE to interact with the AI agent via the local server.

## Example Configuration
```yaml
ide: "PyCharm"
agent_url: "http://localhost:9000"
```

## License
MIT License
