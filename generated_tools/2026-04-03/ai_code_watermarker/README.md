# AI Code Watermarker

## Description
AI Code Watermarker embeds invisible but detectable watermarks across source code files to trace code leaks. This tool is especially useful for companies distributing proprietary AI models and code to ensure accountability in case of unauthorized sharing.

## Features
- Embed invisible watermarks using comments.
- Generate unique watermarks based on identifiers.
- Process individual files or entire directories.
- Configurable output directory.

## Installation

```bash
pip install pygments==2.15.1
```

## Usage

### Example Command

```bash
python ai_code_watermarker.py --input ./source_code --output ./watermarked_code --identifier "unique_identifier"
```

### Arguments
- `--input`: Path to the input file or directory containing source code.
- `--output`: Path to the output directory where watermarked files will be saved.
- `--identifier`: Unique identifier for generating the watermark.

## License
This project is licensed under the MIT License.
