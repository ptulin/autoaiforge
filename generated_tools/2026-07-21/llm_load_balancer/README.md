# LLM Load Balancer

## Overview

The LLM Load Balancer is a Python-based tool designed to dynamically route requests to multiple Large Language Models (LLMs), whether they are local or cloud-based. It intelligently distributes requests based on response time, availability, and quota limits, ensuring optimal utilization of resources. If all local LLMs are unavailable, it falls back to a cloud-based LLM.

## Features

- Dynamically routes requests to the fastest available LLM.
- Handles quota limits for each LLM instance.
- Provides a fallback mechanism to cloud-based LLMs when local instances are unavailable.
- Exposes a REST API endpoint for querying LLMs.

## Requirements

- Python 3.7+
- Flask
- Requests
- Pytest (for testing)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Load Balancer

To start the load balancer server:

```bash
python llm_load_balancer.py
```

The server will start on `http://0.0.0.0:5000`. You can send POST requests to the `/query` endpoint with a JSON payload containing a `query` key.

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "What is the capital of France?"}' http://localhost:5000/query
```

### Command-Line Query

You can also send a query directly from the command line:

```bash
python llm_load_balancer.py --query "What is the capital of France?"
```

### Configuring LLM Instances

You can configure the LLM instances in the `setup_router` function. Replace the example URLs and quotas with your actual LLM endpoints and quotas.

## Testing

To run the tests:

1. Install pytest if not already installed:
   ```bash
   pip install pytest
   ```

2. Run the tests:
   ```bash
   pytest
   ```

The tests include:
- Successful routing to an available LLM instance.
- Handling of all instances failing due to network errors.
- Proper fallback when an instance exceeds its quota.

## License

This project is licensed under the MIT License. See the LICENSE file for details.