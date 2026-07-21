# LLM Health-Aware Router

## Description
The LLM Health-Aware Router is a Python tool designed to intelligently route queries to the healthiest available Large Language Model (LLM) instances. It evaluates real-time health metrics such as latency, uptime, CPU usage, and memory usage to ensure optimal performance and reliability.

## Features
- **Health-based routing**: Automatically prioritizes instances based on health metrics.
- **Automatic exclusion**: Excludes unhealthy or overloaded instances.
- **Customizable thresholds**: Define health thresholds via a YAML configuration file.
- **Lightweight and efficient**: Designed for seamless integration into AI workflows.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/llm_health_router.git
   cd llm_health_router
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Create a YAML configuration file (e.g., `routing_config.yml`) with the following structure:
   ```yaml
   thresholds:
     latency: 100
     uptime: 95
     cpu_usage: 50
     memory_usage: 50
   instances:
     - name: Instance1
       health_url: http://instance1/health
       query_url: http://instance1/query
     - name: Instance2
       health_url: http://instance2/health
       query_url: http://instance2/query
   ```
2. Run the tool:
   ```bash
   python llm_health_router.py --config routing_config.yml --query 'Summarize this document'
   ```

## Example Output
```
Mocked response
```

## Testing
Run the test suite using pytest:
```bash
pytest test_llm_health_router.py
```

## License
MIT License