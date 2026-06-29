# Selixes Cluster Manager

## Overview
Selixes Cluster Manager is a lightweight CLI tool designed to orchestrate and manage clusters of local devices for distributed large language model (LLM) inference. It enables developers to split and assign tasks dynamically across multiple devices, improving performance and throughput.

## Features
- Load cluster configuration from a YAML file
- Load input data from a JSON file
- Initialize a Ray cluster for distributed computation
- Distribute inference tasks across multiple nodes
- Save aggregated results to a JSON file

## Installation

Install the required dependencies using pip:

```bash
pip install ray psutil transformers pyyaml pytest
```

## Usage

Run the tool from the command line:

```bash
python selixes_cluster_manager.py --config <path_to_config.yaml> --input <path_to_input.json> --output <path_to_output.json>
```

### Arguments
- `--config`: Path to the cluster configuration YAML file.
- `--input`: Path to the input data JSON file.
- `--output`: Path to save the aggregated results JSON file.

## Example

1. Create a YAML configuration file (e.g., `config.yaml`):

```yaml
nodes:
  - node1
  - node2
model: gpt2
```

2. Create an input JSON file (e.g., `input.json`):

```json
["Hello world", "How are you?"]
```

3. Run the tool:

```bash
python selixes_cluster_manager.py --config config.yaml --input input.json --output output.json
```

4. The results will be saved in `output.json`.

## Testing

Run the tests using pytest:

```bash
pytest test_selixes_cluster_manager.py
```

The tests include:
- Loading the cluster configuration from a YAML file
- Loading input data from a JSON file
- Distributing tasks across the cluster nodes

## License
MIT License
