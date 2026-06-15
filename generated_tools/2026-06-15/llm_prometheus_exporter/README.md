# LLM Prometheus Exporter

This tool is a lightweight Prometheus exporter that exposes metrics about LLM (Large Language Model) inference performance and resource usage. It monitors key metrics such as latency, token usage, memory consumption, and errors during LLM inference. These metrics can be integrated into Prometheus and visualized for monitoring and debugging purposes.

## Features
- Tracks LLM inference latency
- Monitors token usage and memory consumption
- Counts errors during LLM inference
- Exposes metrics on a configurable HTTP port for Prometheus scraping

## Installation

Install the required dependencies:

```bash
pip install prometheus_client psutil requests
```

## Usage

Run the exporter with the following command:

```bash
python llm_prometheus_exporter.py --llm-endpoint <LLM_ENDPOINT_URL> [--port <PORT>] [--refresh-interval <SECONDS>]
```

### Arguments
- `--llm-endpoint`: URL of the LLM endpoint to monitor (required)
- `--port`: Port to expose Prometheus metrics (default: 9090)
- `--refresh-interval`: Metrics refresh interval in seconds (default: 10)

### Example

```bash
python llm_prometheus_exporter.py --llm-endpoint http://localhost:8000 --port 9091 --refresh-interval 5
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_prometheus_exporter.py
```

## License

This project is licensed under the MIT License.