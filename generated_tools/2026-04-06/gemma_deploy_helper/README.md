# Gemma Deploy Helper

## Description
Gemma Deploy Helper simplifies the deployment of Google Gemma 4 and other open-source AI models onto local hardware. It automatically detects the available hardware (CPU/GPU), configures model-specific settings for optimal performance, and launches the model server with minimal setup effort. This tool is ideal for developers seeking to quickly test and deploy AI models locally without diving into complex configuration details.

## Features
- **Automatic Hardware Detection**: Detects available hardware and optimizes settings for CPU or GPU.
- **Streamlined Model Download**: Automatically downloads the specified AI model and tokenizer.
- **Configurable Server Launch**: Allows customization of batch size and port for the server.

## Installation
To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage
Run the tool using the following command:

```bash
python gemma_deploy_helper.py --model gemma-4 --device gpu --batch-size 8 --port 8080
```

### Options
- `--model`: Name of the model to deploy (e.g., gemma-4).
- `--device`: Hardware preference (`auto`, `cpu`, `gpu`). Default is `auto`.
- `--batch-size`: Batch size for inference. Default is `1`.
- `--port`: Port to run the server on. Default is `8080`.

## Example
Deploy the Gemma-4 model on GPU with batch size 8 and port 8080:

```bash
python gemma_deploy_helper.py --model gemma-4 --device gpu --batch-size 8 --port 8080
```

## License
This project is licensed under the MIT License.