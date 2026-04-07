# Multi-Modal Model Router

## Overview

The Multi-Modal Model Router is a Python CLI tool that dynamically routes input data (text, image, or audio) to the appropriate AI model based on user-specified criteria or automatic content detection. This tool enables seamless integration of multi-modal AI models in applications, reducing the need for manual model switching.

## Features

- **Automatic Content Detection**: Automatically detects the type of input file (text, image, or audio).
- **Dynamic Routing**: Routes the input to the appropriate AI model for processing.
- **CLI Interface**: Easy-to-use command-line interface for specifying input files and options.

## Requirements

Install the required Python packages using pip:

```
pip install transformers torch Pillow librosa numpy
```

## Usage

Run the tool from the command line:

```
python multi_modal_model_router.py --input_file <path_to_file> [--content_type <text|image|audio>] [--debug]
```

- `--input_file`: Path to the input file.
- `--content_type`: (Optional) Specify the content type (text, image, or audio). If not provided, the tool will auto-detect it.
- `--debug`: (Optional) Enable debug mode for detailed logging.

## Testing

Run the tests using pytest:

```
pytest test_multi_modal_model_router.py
```

## License

This project is licensed under the MIT License.