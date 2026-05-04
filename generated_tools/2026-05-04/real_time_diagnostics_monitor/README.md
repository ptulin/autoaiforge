# Real-Time Diagnostics Monitor

## Overview

The Real-Time Diagnostics Monitor is a Python library for monitoring and integrating real-time AI-powered diagnostics into healthcare applications. It processes a stream of patient data (e.g., vitals, imaging) and performs continuous analysis using AI models. Alerts are generated for abnormal conditions, enabling timely intervention.

## Features

- Real-time processing of patient data streams via WebSocket.
- Integration with pre-trained scikit-learn models.
- Customizable alert handling via callback functions.

## Installation

Install the required dependencies:

```bash
pip install websockets scikit-learn pytest
```

## Usage

Run the tool from the command line:

```bash
python real_time_diagnostics_monitor.py --model <path_to_model.pkl> --websocket <websocket_url>
```

- `--model`: Path to the pre-trained scikit-learn model file (in pickle format).
- `--websocket`: WebSocket URL to connect to for real-time data.

## Testing

Run the tests using pytest:

```bash
pytest test_real_time_diagnostics_monitor.py
```

The tests include:
- Model loading validation.
- Message processing with mocked data.
- WebSocket stream handling with mocked WebSocket server.

## License

This project is licensed under the MIT License.