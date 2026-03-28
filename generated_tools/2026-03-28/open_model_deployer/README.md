# Open Model Deployer

## Overview
Open Model Deployer is a Python-based CLI and module utility for deploying open-source AI models like LLaMA, Falcon, or StableLM to local servers or cloud environments. It simplifies the process of setting up REST APIs around these models, with auto-configuration options for popular model hubs.

## Features
- Deploy AI models as REST APIs using FastAPI.
- Supports local model directories and model IDs from popular hubs.
- Mockable and extensible for testing and development.

## Installation
Install the required dependencies:
```bash
pip install fastapi uvicorn
```

## Usage
### CLI
Run the tool via the command line:
```bash
python open_model_deployer.py --model <model_path_or_id> --backend fastapi
```

### Module
Use the `deploy_model` function directly:
```python
from open_model_deployer import deploy_model

deploy_model("./local_model_dir", "fastapi")
```

## Testing
Run the tests using pytest:
```bash
pytest test_open_model_deployer.py
```

## License
MIT License