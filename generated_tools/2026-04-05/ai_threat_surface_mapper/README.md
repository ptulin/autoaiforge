# AI Threat Surface Mapper

## Description
The AI Threat Surface Mapper is a command-line tool designed to scan AI model files, codebases, and configuration files for potential security vulnerabilities. It helps developers identify issues such as insecure API endpoints, hardcoded secrets, and weak encryption practices, enabling them to secure their AI systems before deployment.

## Features
- **Static Analysis**: Analyze AI model files, configuration files, and code for vulnerabilities.
- **Detect Common Vulnerabilities**: Identify issues like hardcoded keys, insecure HTTP usage, and weak encryption algorithms.
- **Security Reports**: Automatically generate detailed security reports highlighting risks and recommendations.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/ai-threat-surface-mapper.git
   cd ai-threat-surface-mapper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To scan a file or directory for vulnerabilities, run the following command:

```bash
python ai_threat_surface_mapper.py --path /path/to/scan
```

### Example

Scan a directory:
```bash
python ai_threat_surface_mapper.py --path /models/my_model
```

## Output
The tool will display a detailed security report in a tabular format, highlighting files with vulnerabilities and providing recommendations.

## Limitations
- This tool performs static analysis and may not detect runtime vulnerabilities.
- It is designed to identify common issues but may not catch all possible security flaws.

## License
This project is licensed under the MIT License.