# MikroTik LLM Optimizer

## Description

A CLI tool to automate MikroTik router configuration for optimizing networking setups tailored to large language model (LLM) communication. This tool helps AI developers configure Quality of Service (QoS), bandwidth allocation, and port forwarding for efficient LLM data transmission, reducing latency.

## Installation

Install the required Python package:

```bash
pip install routeros-api
```

## Usage

Run the script with the following arguments:

```bash
python mikrotik_llm_optimizer.py --host <router_ip> --user <username> --password <password> --prioritize-ports <ports> [--bandwidth-limit <kbps>]
```

### Arguments

- `--host`: MikroTik router IP address (required)
- `--user`: MikroTik username (required)
- `--password`: MikroTik password (required)
- `--prioritize-ports`: Comma-separated list of ports to prioritize for LLM traffic (required)
- `--bandwidth-limit`: Bandwidth limit for LLM traffic in kbps (optional, e.g., 10000 for 10 Mbps)

## Example

```bash
python mikrotik_llm_optimizer.py --host 192.168.88.1 --user admin --password admin --prioritize-ports 8000,8001 --bandwidth-limit 10000
```

## Testing

Run the tests using pytest:

```bash
pytest test_mikrotik_llm_optimizer.py
```

## License

MIT License