# Claude Skills Manager

## Overview
Claude Skills Manager is a CLI tool designed to help AI developers manage and deploy custom automation Skills to the Claude AI platform. It simplifies the process of defining, editing, validating, and uploading Skills configurations.

## Features
- **Validate Skill Configuration**: Ensure your YAML skill configuration files are properly structured.
- **Deploy Skill Configuration**: Upload your skill configuration to the Claude API for deployment.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Validate Skill Configuration
To validate a skill configuration file:
```bash
python claude_skills_manager.py validate --skill <path_to_skill_yaml>
```

### Deploy Skill Configuration
To deploy a skill configuration file:
```bash
python claude_skills_manager.py deploy --skill <path_to_skill_yaml> --api-url <claude_api_url>
```

## Requirements
- Python 3.7+
- `pyyaml`
- `requests`
- `pytest` (for testing)

## Testing
To run the tests:
```bash
pytest test_claude_skills_manager.py
```

## License
This project is licensed under the MIT License.