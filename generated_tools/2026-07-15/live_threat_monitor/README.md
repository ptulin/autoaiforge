# Live Threat Monitor

Live Threat Monitor is a lightweight CLI tool designed to monitor live incoming network traffic or log streams and use AI to flag suspicious activity in real-time. It is ideal for developers simulating or testing network attacks in development environments.

## Features
- Monitors live network traffic on a specified interface.
- Uses a pre-trained AI model to detect suspicious activity.
- Logs detected threats to a JSON file (optional).

## Requirements
- Python 3.7+
- Required Python packages:
  - `scapy`
  - `tensorflow`
  - `colorama`

## Installation
Install the required Python packages:
```bash
pip install scapy tensorflow colorama
```

## Usage
Run the tool with the following command:
```bash
python live_threat_monitor.py --interface <network_interface> --model <path_to_model> [--log <log_file>]
```

### Arguments
- `--interface`: The network interface to monitor (e.g., `eth0`).
- `--model`: Path to the pre-trained AI model.
- `--log`: (Optional) Path to save JSON log of detected threats.

### Example
```bash
sudo python live_threat_monitor.py --interface eth0 --model anomaly_model.h5 --log threats.json
```

## Testing
To run the tests, install `pytest`:
```bash
pip install pytest
```
Run the tests using:
```bash
pytest test_live_threat_monitor.py
```

## Notes
- The tool requires root or sufficient privileges to monitor network traffic.
- Ensure the pre-trained AI model is compatible with TensorFlow and accepts the input format used in the tool.

## License
This project is licensed under the MIT License.