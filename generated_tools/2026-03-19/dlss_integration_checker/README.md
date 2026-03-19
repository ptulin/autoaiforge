# DLSS Integration Checker

## Description
The DLSS Integration Checker is a Python library designed to help developers verify the readiness of their game or visualization project for NVIDIA DLSS 5 integration. It evaluates rendering pipelines, checks for compatible APIs and GPUs, and provides detailed debugging tips for unsupported configurations.

## Features
- **Rendering Pipeline Evaluation**: Checks if your rendering pipeline is compatible with DLSS 5.
- **API Compatibility Check**: Verifies if the rendering API (DirectX 12 or Vulkan) is supported.
- **GPU Compatibility Check**: Ensures that your GPU is an NVIDIA GPU, which is required for DLSS.
- **Debugging Tips**: Provides detailed suggestions for resolving compatibility issues.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dlss_integration_checker.git
   cd dlss_integration_checker
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### As a Library
```python
from dlss_integration_checker import check_dlss_compatibility

result = check_dlss_compatibility('config.yaml')
print(result)
```

### As a CLI Tool
```bash
python dlss_integration_checker.py config.yaml
```

## Input Format
The tool accepts configuration files in YAML or JSON format. Below is an example YAML configuration file:
```yaml
rendering_api: directx12
gpu: nvidia rtx 3080
rendering_pipeline:
  type: deferred
```

## Output
The tool provides a compatibility assessment and debugging tips if issues are found. Example output:
```
DLSS Compatibility Check Results:
- rendering_api: Supported API: directx12.
- gpu: Supported GPU: nvidia rtx 3080.
- rendering_pipeline: Supported rendering pipeline: deferred.
```

## Testing
Run the tests using pytest:
```bash
pytest test_dlss_integration_checker.py
```

## License
MIT License