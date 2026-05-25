# Auto Agent Deployer

## Overview

Auto Agent Deployer is a CLI tool designed to streamline the deployment of AI agents, such as Claude or Gemini Omni, for automation tasks. The tool allows developers to define workflows, configure agent settings, and deploy agents to cloud or local environments with minimal effort.

## Features

- Deploy AI agents using YAML configuration files.
- Support for AWS Lambda deployment.
- Logging for deployment status and errors.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd auto_agent_deployer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python auto_agent_deployer.py --config <path-to-yaml-config>
```

### Example YAML Configuration

```yaml
agents:
  - name: example_agent
    type: aws_lambda
    runtime: python3.8
    role: arn:aws:iam::123456789012:role/service-role/example-role
    handler: lambda_function.lambda_handler
    code_zip: !!binary |
      U29tZSBiaW5hcnkgZGF0YSBoZXJl
    description: Example Lambda Function
    timeout: 15
    memory_size: 128
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_auto_agent_deployer.py
```

## Requirements

- Python 3.7+
- boto3
- PyYAML

## License

This project is licensed under the MIT License.
