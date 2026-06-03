# Dynamic Context Packer

## Description
Dynamic Context Packer is a Python CLI tool designed to dynamically package mixed data types (e.g., text, metadata, tables) into a single context window for large language models. It uses adaptive formatting based on token limits and user-defined rules to optimize how information is presented. This is particularly useful for tasks requiring complex context, like generating multi-modal reports or providing detailed answers.

## Features
- Handles mixed data types (text, metadata, etc.)
- Adaptive formatting to fit token constraints
- User-defined packing rules and priorities

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python dynamic_context_packer.py --input data.json --max_tokens 4096 --output packed_context.txt
```

### Example

```bash
python dynamic_context_packer.py --input data1.json data2.json --max_tokens 2048 --output packed_context.json
```

## Requirements
- Python 3.8+
- pandas==1.5.3
- tiktoken==0.3.0

## License
MIT