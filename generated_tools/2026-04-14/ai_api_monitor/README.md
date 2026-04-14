# AI API Traffic Monitor

AI API Traffic Monitor acts as a middleware that logs and inspects requests and responses between your application and AI APIs like Claude AI. It analyzes traffic for anomalies, including sensitive data leaks, unexpected API calls, or malicious payloads.

## Features

- Logs all incoming requests and outgoing responses.
- Detects sensitive information in the traffic.
- Saves logs to a specified file.
- Acts as a proxy server to forward requests to the target API.

## Installation

Install the required Python package:

```
pip install httpx
```

## Usage

Run the proxy server with the following command:

```
python ai_api_monitor.py --port <PORT> --logfile <LOGFILE> --target_url <TARGET_URL>
```

- `--port`: The port to run the proxy server on.
- `--logfile`: The file to save traffic logs.
- `--target_url`: The target URL of the AI API to forward requests to.

## Testing

To run the tests, install `pytest`:

```
pip install pytest
```

Run the tests using:

```
pytest test_ai_api_monitor.py
```

## Example

Start the proxy server:

```
python ai_api_monitor.py --port 8080 --logfile logs.json --target_url https://api.example.com
```

Send a POST request to the proxy server:

```
curl -X POST -d "{\"key\": \"value\"}" http://localhost:8080/test
```

Check the logs in `logs.json` for anomalies or traffic details.
