# Mesh Orchestration Helper

## Description
Mesh Orchestration Helper is a CLI tool designed to simplify the orchestration of distributed AI workloads using Mesh LLM. It provides utilities for configuring nodes, generating topology YAML files, and launching distributed training jobs with minimal manual setup.

## Features
- Parse node configurations in the format `IP:GPUs`.
- Generate YAML configuration files for distributed AI workloads.
- Validate node connectivity and resource availability.
- Launch distributed training jobs.

## Installation
Install the required dependencies using pip:

```bash
pip install pyyaml paramiko pytest
```

## Usage
Run the tool using the following command:

```bash
python mesh_orchestration_helper.py --nodes "192.168.1.1:4,192.168.1.2:8" --model gpt3 --script train.py --output mesh_config.yaml --validate --launch
```

### Arguments
- `--nodes`: Comma-separated list of nodes in the format `IP:GPUs`.
- `--model`: Model type (e.g., `gpt3`).
- `--script`: Path to the training script.
- `--output`: Output YAML configuration file (default: `mesh_config.yaml`).
- `--validate`: Validate node connectivity.
- `--launch`: Launch the distributed training job.

## Testing
Run the tests using pytest:

```bash
pytest test_mesh_orchestration_helper.py
```

The tests include:
- Parsing node configurations.
- Generating YAML configuration files.
- Validating node connectivity (mocked).

All tests should pass without requiring network access.
