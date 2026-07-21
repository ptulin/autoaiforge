# AI Threat Simulator

AI Threat Simulator is a Python tool designed for developers to simulate and test common AI-driven attack vectors on their systems. It generates controlled, benign attacks such as spoofed API calls, brute force attempts, and data exfiltration simulations to help identify vulnerabilities in AI models.

## Features
- Simulate spoofed API call attacks
- Simulate brute force attacks
- Simulate data exfiltration attacks

## Installation

Install the required dependencies using pip:

```bash
pip install requests faker
```

## Usage

Run the simulator with the desired attack type and parameters:

```bash
python ai_threat_simulator.py --attack <spoof|brute|exfiltration> --target <URL> [--frequency <number>] [--payload_size <size>]
```

### Arguments
- `--attack`: Type of attack to simulate (`spoof`, `brute`, or `exfiltration`).
- `--target`: Target endpoint URL.
- `--frequency`: Number of attack attempts (default: 1).
- `--payload_size`: Payload size for data exfiltration (default: 100 characters).

## Testing

Run the tests using pytest:

```bash
pytest test_ai_threat_simulator.py
```

All tests are mocked and do not require network access.
