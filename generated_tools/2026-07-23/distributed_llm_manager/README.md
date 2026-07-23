# Distributed LLM Manager

## Overview
This script simplifies the orchestration of distributed LLM inference across multiple devices. It sets up a collaborative network where devices can serve shards of a large language model and respond to inference requests as a collective. This is especially useful for running resource-heavy models in distributed environments.

## Installation

Install the required dependencies:

```bash
pip install ray grpcio pyyaml
```

## Usage

Run the script with the path to a configuration file:

```bash
python distributed_llm_manager.py --config /path/to/config.yaml
```

## Configuration File

The configuration file should be in YAML format and include the following keys:

```yaml
ray_address: "auto"
model:
  size: 1000
  shards: 4
```

- `ray_address`: The address of the Ray cluster.
- `model.size`: The total size of the model.
- `model.shards`: The number of shards to partition the model into.

## Testing

Run the tests using `pytest`:

```bash
pytest test_distributed_llm_manager.py
```

The tests include:
- Verifying Ray cluster setup.
- Ensuring the model is partitioned correctly.
- Mocking and testing the gRPC inference service setup.

## License

MIT License
