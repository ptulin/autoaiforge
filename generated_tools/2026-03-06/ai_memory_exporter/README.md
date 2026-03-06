# AI Memory Exporter

AI Memory Exporter is a command-line tool that enables developers to extract and export memory data from AI systems like ChatGPT and Claude. It supports multiple output formats (JSON, YAML) and ensures compatibility with different APIs, making it easier to migrate or share AI context between systems.

## Features

- Extract memory data from AI systems via API.
- Export memory data in JSON or YAML formats.
- Pluggable architecture for compatibility with various AI APIs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_memory_exporter.git
   cd ai_memory_exporter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python ai_memory_exporter.py --api_endpoint <API_ENDPOINT> --api_key <API_KEY> --model <MODEL> --output <OUTPUT_FILE> [--format <FORMAT>]
```

### Example

```bash
python ai_memory_exporter.py --api_endpoint https://api.example.com/memory --api_key YOUR_API_KEY --model chatgpt --output memory.json
```

This will export the memory data from the ChatGPT model to a file named `memory.json` in JSON format.

## Supported Models

- ChatGPT
- Claude

## Supported Formats

- JSON
- YAML

## License

This project is licensed under the MIT License.