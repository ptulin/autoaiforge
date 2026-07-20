# LLM Quickstart

LLM Quickstart automates the setup, configuration, and deployment of large language models (LLMs) on local machines. It simplifies the process by detecting system capabilities, downloading model weights, and configuring an optimized runtime environment.

## Features
- Automatic hardware detection (CPU/GPU support)
- Download and setup of popular open-source LLMs like Llama or GPT-J
- Local inference server setup for easy interaction with deployed models

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Download and Setup a Model

```bash
python llm_quickstart.py --model EleutherAI/gpt-j-6B --precision fp16
```

### Start a Local Inference Server

```bash
python llm_quickstart.py --model EleutherAI/gpt-j-6B --precision fp16 --server
```

The server will start on `http://0.0.0.0:5000`. You can send POST requests to `/generate` with a JSON payload:

```json
{
  "prompt": "Once upon a time,"
}
```

## Requirements

- Python 3.8+
- torch==2.0.1
- transformers==4.33.3
- requests==2.31.0
- pyyaml==6.0
- Flask==2.3.3

## License

MIT License
